#!/usr/bin/env python3
"""Refresh first-party publication metadata without executing remote JavaScript.

Run from any directory. Existing paper fragments and editorial topic assignments
stay intact. Newly discovered faculty titles are reported for human review.
"""
import argparse
from datetime import datetime
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import time
import xml.etree.ElementTree as ET
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'assets/scripts/pub_list'
FACULTY_URL = 'https://tushar-krishna.github.io/publications.html'
SCHOLAR_URL = 'https://scholar.google.com/citations?user=P__ztgcAAAAJ&hl=en&sortby=pubdate&pagesize=100'
ARXIV_API = 'https://export.arxiv.org/api/query?'
OPENALEX_API = 'https://api.openalex.org/works?'
OPENALEX_AUTHOR = 'A5034089074'  # ORCID 0000-0001-5738-6942 (Tushar Krishna)
ATOM = {'a': 'http://www.w3.org/2005/Atom', 'o': 'http://a9.com/-/spec/opensearch/1.1/'}

# Names absent from the faculty page's abbreviation map. Official sources:
# https://conferences.sigcomm.org/sigcomm/2026/
# https://www.glsvlsi.hosting.acm.org/archive/glsvlsi21/acm/tecs-cfp.pdf
# https://www.isfpga.org/
# https://jianmingtong.github.io/ (FastSwitch publication entry)
# https://ieeexplore.ieee.org/document/10740726/ (CODES+ISSS proceedings)
VENUE_NAMES = {
    'SIGCOMM': 'ACM SIGCOMM Conference',
    'ACM TECS': 'ACM Transactions on Embedded Computing Systems',
    'FPGA': 'ACM/SIGDA International Symposium on Field-Programmable Gate Arrays',
    'ACSMD@ISCA': 'Architecture, Compiler, and System Support for Multi-model DNN Workloads Workshop at ISCA',
    'CODES+ISSS': 'International Conference on Hardware/Software Codesign and System Synthesis',
}

# Reviewed title variants of the same work; do not fuzzy-match different papers.
ALIASES = {
    'NSFlow:': 'paper_scholar2025_nsflow-an-end-to-end-fpga-framework-with-scalable-da.html',
    'TurboAttention:': 'paper_scholar2025_turboattention-efficient-attention-approximation-for.html',
    'Axon:': 'paper_nayan2025axon.html',
    'MicroEdge:': 'paper_yoomicroedge.html',
    'DiGamma:': 'paper_scholar2022_digamma-domain-aware-genetic-algorithm-for-hw-mappin.html',
    'DUB:': 'paper_scholar2021_dub-dynamic-underclocking-and-bypassing-in-nocs-for.html',
    'Union:': 'paper_scholar2021_union-a-unified-hw-sw-co-design-ecosystem-in-mlir-fo.html',
    'Enabling Compute-Communication Overlap': 'paper_scholar2021_enabling-compute-communication-overlap-in-distribute.html',
    'E3:': 'paper_scholar2021_e3-a-hw-sw-co-design-neuroevolution-platform-for-aut.html',
    'Bridging the Frequency Gap': 'paper_scholar2021_bridging-the-frequency-gap-in-heterogeneous-3d-socs.html',
    'Understanding Reuse, Performance, and Hardware Cost of DNN Dataflows: A Data-Centric Approach': 'paper_scholar2019_understanding-reuse-performance-and-hardware-cost-of.html',
    'Scaling the Cascades:': 'paper_scholar2019_scaling-the-cascades-interconnect-aware-fpga-impleme.html',
    'mRNA:': 'paper_scholar2019_mrna-enabling-efficient-mapping-space-exploration-fo.html',
}


def fetch(url):
    with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30) as response:
        return response.read().decode('utf-8')


def literal(source, name):
    """Decode the page's JSON-like literals with bare keys, never eval its code."""
    match = re.search(r'\bconst\s+' + re.escape(name) + r'\s*=\s*', source)
    if not match:
        raise ValueError(f'Missing data block: {name}')

    def skip(i):
        while True:
            match = re.match(r'\s+|//[^\n]*(?:\n|$)|/\*[\s\S]*?\*/', source[i:])
            if not match:
                return i
            i += match.end()

    def parse(i):
        i = skip(i)
        char = source[i]
        if char == '"':
            value, length = json.JSONDecoder().raw_decode(source[i:])
            return value, i + length
        if char in '[{':
            end = ']' if char == '[' else '}'
            result = [] if char == '[' else {}
            i = skip(i + 1)
            while source[i] != end:
                if char == '{':
                    if source[i] == '"':
                        key, i = parse(i)
                    else:
                        key_match = re.match(r'[A-Za-z_$][\w$]*', source[i:])
                        if not key_match:
                            raise ValueError('Unsupported data key')
                        key = key_match.group()
                        i += key_match.end()
                    i = skip(i)
                    if source[i] != ':':
                        raise ValueError('Expected data property')
                    value, i = parse(i + 1)
                    result[key] = value
                else:
                    value, i = parse(i)
                    result.append(value)
                i = skip(i)
                if source[i] == ',':
                    i = skip(i + 1)
                elif source[i] != end:
                    raise ValueError('Unsupported literal syntax')
            return result, i + 1
        value, length = json.JSONDecoder().raw_decode(source[i:])
        return value, i + length

    return parse(match.end())[0]


def title_key(text):
    text = re.sub(r'<[^>]+>', '', unescape(text)).lower().replace('&', ' and ')
    text = re.sub(r'[^a-z0-9]+', ' ', text)
    text = re.sub(r'([a-z])(\d)', r'\1 \2', text)
    text = re.sub(r'(\d)([a-z])', r'\1 \2', text)
    text = re.sub(r'\btowards\b', 'toward', text)
    text = re.sub(r'\btinyml\b', 'tiny machine learning', text)
    return re.sub(r'\s+', ' ', re.sub(r'^special session\s+', '', text)).strip()


def work_ids(values):
    ids = set()
    for value in values:
        text = unescape(str(value or ''))
        for identifier in re.findall(r'(?:arxiv\.org/(?:abs|pdf)/|arxiv\s*:\s*)(\d{4}\.\d{4,5})(?:v\d+)?', text, re.I):
            ids.add('arxiv:' + identifier)
        for identifier in re.findall(r'(?:doi\.org/|doi\s*:\s*)(10\.\d{4,9}/[^\s"<>?#]+)', text, re.I):
            ids.add('doi:' + identifier.rstrip('.,;').lower())
    return ids


def read_local_papers(data_dir):
    papers = []
    for filename in json.loads((data_dir / 'papers.json').read_text()):
        path = data_dir / 'htmls' / filename
        source = path.read_text()
        def field(name):
            match = re.search(r'<span\b[^>]*class=[\'"]' + name + r'[\'"][^>]*>([\s\S]*?)</span>', source)
            return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]*>', '', match[1]))).strip() if match else ''
        title = field('paper-title')
        if not title:
            continue
        alias = re.search(r'data-search-aliases="([^"]*)"', source)
        venue = field('paper-conference')
        authors = field('paper-authors')
        date = re.search(r'id=[\'"]((?:19|20)\d{2})-\d{2}[\'"]', source)
        hrefs = re.findall(r'href=[\'"]([^\'"]+)', source)
        papers.append({'filename': path.name, 'title': title,
                       'authors': authors, 'year': int(date[1]) if date else 0,
                       'alias': unescape(alias[1]) if alias else '',
                       'ids': work_ids([venue, *hrefs]),
                       'preprint': not venue or bool(re.search(r'\barxiv\b|^corr\b|\bpreprint\b', venue, re.I))})
    return papers


def match_publication(pub, local, previous, review=None):
    """Link versions only through exact titles, reviewed aliases, or identifiers."""
    titles = [pub['title'], *(review or {}).get('matchTitles', [])]
    identities = work_ids([pub.get('url'), pub.get('pdf'), pub.get('doi'), pub.get('arxiv')])
    identities.update((review or {}).get('identityKeys', []))
    for old in previous:
        if title_key(old['title']) == title_key(pub['title']) and old.get('venue') == pub.get('v'):
            titles.extend(old.get('matchTitles', []))
            identities.update(old.get('identityKeys', []))
    for prefix, filename in ALIASES.items():
        if pub['title'].startswith(prefix):
            titles.extend(paper['title'] for paper in local if paper['filename'] == filename)
    keys = {title_key(title) for title in titles}
    matched = [paper for paper in local if title_key(paper['title']) in keys
               or paper['alias'] and title_key(paper['alias']) in keys]
    for paper in matched:
        identities.update(paper['ids'])
    # Do not absorb a distinct journal/workshop paper just because it reuses a PDF.
    matched += [paper for paper in local if paper not in matched and paper['preprint']
                and identities.intersection(paper['ids'])]
    for paper in matched:
        titles.extend([paper['title'], paper['alias']])
        identities.update(paper['ids'])
    return list(dict.fromkeys(title for title in titles if title)), sorted(identities), bool(matched)


class ScholarRows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.row = None
        self.field = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get('class', '').split()
        if tag == 'tr' and 'gsc_a_tr' in classes:
            self.row = {'title': '', 'year': ''}
        if self.row is not None:
            if tag == 'a' and 'gsc_a_at' in classes:
                self.field = 'title'
            elif tag == 'td' and 'gsc_a_y' in classes:
                self.field = 'year'

    def handle_data(self, data):
        if self.row is not None and self.field:
            self.row[self.field] += data

    def handle_endtag(self, tag):
        if (tag == 'a' and self.field == 'title') or (tag == 'td' and self.field == 'year'):
            self.field = None
        if tag == 'tr' and self.row is not None:
            self.row = {key: re.sub(r'\s+', ' ', value).strip() for key, value in self.row.items()}
            if self.row['title']:
                self.rows.append(self.row)
            self.row = None
            self.field = None


def refresh_faculty(source, data_dir=DATA):
    pubs = literal(source, 'PUBS')
    names = literal(source, 'VENUE_FULL')
    months = literal(source, 'VENUE_MONTH')
    if len(pubs) < 100 or not isinstance(names, dict):
        raise ValueError('Incomplete faculty data; leaving existing metadata intact')
    names = {**VENUE_NAMES, **names}
    local = read_local_papers(data_dir)
    previous_path = data_dir / 'faculty_publications.json'
    previous = json.loads(previous_path.read_text()).get('papers', []) if previous_path.exists() else []
    review_path = data_dir / 'publication_versions.json'
    reviews = json.loads(review_path.read_text()) if review_path.exists() else {}
    names.update(reviews.get('venueNames', {}))
    pubs.extend(reviews.get('additionalPublications', []))
    records = []
    unmatched = []
    for pub in pubs:
        if pub['y'] < 2015:
            continue
        review = next((item for item in reviews.get('reconciliations', [])
                       if title_key(item['title']) == title_key(pub['title']) and item['venue'] == pub['v']), {})
        # Reviewed publisher evidence wins over a typo in an upstream faculty list.
        pub = {**pub, 'y': review.get('year', pub['y'])}
        titles, identities, matched = match_publication(pub, local, previous, review)
        record = {
            'title': pub['title'], 'matchTitles': titles, 'identityKeys': identities,
            'authors': pub['a'], 'year': pub['y'], 'venue': pub['v'], 'type': pub['t'],
            'month': int(pub.get('m', months.get(pub['v'], 0))),
        }
        if pub.get('si'):
            record['specialIssue'] = pub['si']
        if review.get('sources') or pub.get('sources'):
            record['reviewSources'] = review.get('sources', pub.get('sources'))
        # Do not import award notes. The lab's MLSys no-Oral correction wins.
        records.append(record)
        if not matched:
            unmatched.append(f"{pub['y']} · {pub['v']} · {pub['title']}")
    return {'source': FACULTY_URL, 'checkedOn': datetime.now(ZoneInfo('America/Los_Angeles')).date().isoformat(),
            'venueNames': names, 'papers': records}, unmatched


def refresh_scholar(first_page=None):
    entries = []
    for offset in range(0, 1000, 100):
        source = first_page if offset == 0 and first_page else fetch(SCHOLAR_URL + f'&cstart={offset}')
        parser = ScholarRows()
        parser.feed(source)
        if not parser.rows and not entries:
            raise ValueError('Scholar did not return publication rows; existing ordering preserved')
        if not parser.rows and 'captcha' in source.lower():
            raise ValueError('Scholar requested verification; existing ordering preserved')
        entries.extend(parser.rows)
        if len(parser.rows) < 100:
            break
    else:
        raise ValueError('Scholar pagination limit reached; existing ordering preserved')
    previous = json.loads((DATA / 'scholar_order.json').read_text())
    if len(entries) < len(previous) * 0.9:
        raise ValueError('Scholar result appears incomplete; existing ordering preserved')
    return entries


def parse_arxiv_feed(source):
    """Keep only source-provided abstracts with an explicit, versioned arXiv URL."""
    root = ET.fromstring(source)
    if root.tag != '{http://www.w3.org/2005/Atom}feed':
        raise ValueError('Invalid arXiv feed')
    records = []
    for entry in root.findall('a:entry', ATOM):
        url = (entry.findtext('a:id', default='', namespaces=ATOM)).strip()
        match = re.fullmatch(r'https?://arxiv\.org/abs/(\d{4}\.\d{4,5}v\d+)', url)
        title = ' '.join(entry.findtext('a:title', default='', namespaces=ATOM).split())
        abstract = ' '.join(entry.findtext('a:summary', default='', namespaces=ATOM).split())
        if match and title and abstract and not abstract.lower().startswith('withdrawn'):
            records.append({'title': title, 'text': abstract,
                            'source': 'https://arxiv.org/abs/' + match.group(1)})
    return records


def refresh_abstracts(faculty, data_dir=DATA, feeds=None):
    """Match exact titles only; ambiguous records stay hidden for manual review."""
    local = read_local_papers(data_dir)
    titles = {title_key(p['title']) for p in local} | {title_key(p['title']) for p in faculty['papers']}
    alias_path = data_dir / 'reviewed_abstract_links.json'
    reviewed = json.loads(alias_path.read_text()) if alias_path.exists() else []
    titles.update(title_key(item['sourceTitle']) for item in reviewed if item['kind'] == 'arxiv')
    if feeds is None:
        query = urlencode({'search_query': 'au:"Tushar Krishna"', 'start': 0, 'max_results': 1000})
        author_feed = fetch(ARXIV_API + query)
        root = ET.fromstring(author_feed)
        total = int(root.findtext('o:totalResults', default='-1', namespaces=ATOM))
        if total < 1 or total > 1000 or len(root.findall('a:entry', ATOM)) != total:
            raise ValueError('Incomplete arXiv author feed; existing abstracts preserved')
        ids = sorted({identity[6:] for paper in local for identity in paper['ids'] if identity.startswith('arxiv:')}
                     | {identity[6:] for paper in faculty['papers'] for identity in paper.get('identityKeys', []) if identity.startswith('arxiv:')})
        ids = sorted(set(ids) | {item['id'] for item in reviewed if item['kind'] == 'arxiv'})
        feeds = [author_feed]
        for offset in range(0, len(ids), 100):
            time.sleep(3)  # arXiv API request pacing
            feeds.append(fetch(ARXIV_API + urlencode({'id_list': ','.join(ids[offset:offset+100]), 'max_results': 100})))
    candidates = {}
    for feed in feeds:
        for record in parse_arxiv_feed(feed):
            key = title_key(record['title'])
            if key in titles:
                candidates.setdefault(key, {})[record['source'].rsplit('v', 1)[0]] = record
    # Multiple distinct arXiv works with the same title are not safe to assign.
    records = [next(iter(items.values())) for items in candidates.values() if len(items) == 1]
    return {'source': 'arXiv API', 'papers': sorted(records, key=lambda item: title_key(item['title']))}


def parse_openalex_abstract(inverted):
    """Reconstruct complete text only when every word position is present once."""
    positions = {}
    if not isinstance(inverted, dict):
        return ''
    for word, indexes in inverted.items():
        if not isinstance(word, str) or not isinstance(indexes, list):
            return ''
        for pos in indexes:
            if not isinstance(pos, int) or pos < 0 or pos in positions:
                return ''
            positions[pos] = word
    if not positions or set(positions) != set(range(len(positions))):
        return ''
    return ' '.join(positions[i] for i in range(len(positions)))


def refresh_openalex(faculty, arxiv, works, data_dir=DATA):
    """Supplement arXiv with uniquely matched published works in OpenAlex."""
    local = read_local_papers(data_dir)
    faculty_titles = {title_key(p['title']) for p in faculty['papers']}
    targets = [(p['title'], p['year'], p['authors']) for p in faculty['papers']]
    targets += [(p['title'], p['year'], p['authors']) for p in local
                if not p['preprint'] and title_key(p['title']) not in faculty_titles]
    existing = {title_key(p['title']) for p in arxiv['papers']}
    candidates = {}
    for work in works:
        title = work.get('title') or ''
        key = title_key(title)
        if key in existing or work.get('type') not in ('article', 'conference-paper', 'book-chapter'):
            continue
        identifier, doi = work.get('id') or '', work.get('doi') or ''
        text = parse_openalex_abstract(work.get('abstract_inverted_index'))
        if not re.fullmatch(r'https://openalex\.org/W\d+', identifier) or not re.fullmatch(r'https://doi\.org/10\.\d{4,9}/[^\s]+', doi, re.I) or not text:
            continue
        names = [a.get('author', {}).get('display_name', '') for a in work.get('authorships', [])]
        matches = [t for t in targets if title_key(t[0]) == key and t[1] == work.get('publication_year')
                   and any(len(name.split()) > 1 and name.split()[-1].casefold() in t[2].casefold() for name in names)]
        if not matches:
            continue
        candidates.setdefault(key, {})[doi.lower()] = {'title': matches[0][0], 'text': text,
                                                       'source': identifier, 'publisher': doi}
    records = [next(iter(group.values())) for group in candidates.values() if len(group) == 1]
    combined = {title_key(p['title']): p for p in arxiv['papers'] + records}
    alias_path = data_dir / 'reviewed_abstract_links.json'
    reviewed = json.loads(alias_path.read_text()) if alias_path.exists() else []
    by_work_id = {work.get('id'): work for work in works}
    for item in reviewed:
        key = title_key(item['title'])
        if item['kind'] == 'arxiv':
            matches = [p for p in arxiv['papers'] if title_key(p['title']) == title_key(item['sourceTitle'])
                       and re.fullmatch(r'https://arxiv\.org/abs/' + re.escape(item['id']) + r'v\d+', p['source'])]
            if len(matches) == 1:
                combined[key] = {**matches[0], 'title': item['title']}
        elif item['kind'] == 'openalex':
            work = by_work_id.get('https://openalex.org/' + item['id'])
            if not work or title_key(work.get('title') or '') != title_key(item['sourceTitle']) or (work.get('doi') or '').lower() != item['doi'].lower():
                continue
            text = parse_openalex_abstract(work.get('abstract_inverted_index'))
            if text and re.fullmatch(r'https://doi\.org/10\.\d{4,9}/[^\s]+', item['doi'], re.I):
                combined[key] = {'title': item['title'], 'text': text, 'source': work['id'], 'publisher': item['doi']}
    reviewed_path = data_dir / 'reviewed_publisher_abstracts.json'
    if reviewed_path.exists():
        for item in json.loads(reviewed_path.read_text()):
            key = title_key(item.get('title', ''))
            source = item.get('source', '')
            valid_source = (re.fullmatch(r'https://ieeexplore\.ieee\.org/document/\d+', source)
                            or re.fullmatch(r'https://proceedings\.mlsys\.org/paper_files/paper/\d{4}/hash/[a-f0-9]+-Abstract-Conference\.html', source)
                            or source == 'https://anands09.github.io/papers/maeri_asplos2018.pdf')
            if key in {title_key(t[0]) for t in targets} and item.get('text') and valid_source:
                combined[key] = item
    return {'source': 'arXiv, OpenAlex and reviewed publisher pages',
            'papers': sorted(combined.values(), key=lambda item: title_key(item['title']))}


def fetch_openalex(data_dir=DATA):
    works = []
    for page in range(1, 11):
        query = urlencode({'filter': f'authorships.author.id:{OPENALEX_AUTHOR},from_publication_date:2015-01-01',
                           'per-page': 100, 'page': page})
        payload = json.loads(fetch(OPENALEX_API + query))
        batch = payload['results']
        works.extend(batch)
        if len(works) >= payload['meta']['count']:
            alias_path = data_dir / 'reviewed_abstract_links.json'
            reviewed = json.loads(alias_path.read_text()) if alias_path.exists() else []
            ids = [item['id'] for item in reviewed if item['kind'] == 'openalex']
            if ids:
                time.sleep(1)
                extra = json.loads(fetch(OPENALEX_API + urlencode({'filter': 'openalex_id:' + '|'.join(ids), 'per-page': 100})))
                works.extend(extra['results'])
            return works
        if len(batch) != 100:
            break
        time.sleep(1)
    raise ValueError('Incomplete OpenAlex results; existing abstracts preserved')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--faculty-html', type=Path, help='Use a saved first-party page for a reproducible refresh')
    parser.add_argument('--scholar-html', type=Path, help='Use a saved first page; remaining pages are fetched')
    parser.add_argument('--skip-scholar', action='store_true')
    parser.add_argument('--arxiv-feed', type=Path, action='append', help='Use saved arXiv Atom feed(s) for a reproducible refresh')
    parser.add_argument('--openalex-json', type=Path, help='Use saved OpenAlex results for a reproducible refresh')
    args = parser.parse_args()
    source = args.faculty_html.read_text() if args.faculty_html else fetch(FACULTY_URL)
    faculty, unmatched = refresh_faculty(source)
    scholar = None if args.skip_scholar else refresh_scholar(args.scholar_html.read_text() if args.scholar_html else None)
    abstracts = refresh_abstracts(faculty, feeds=[path.read_text() for path in args.arxiv_feed] if args.arxiv_feed else None)
    works = json.loads(args.openalex_json.read_text()) if args.openalex_json else fetch_openalex()
    abstracts = refresh_openalex(faculty, abstracts, works)
    (DATA / 'faculty_publications.json').write_text(json.dumps(faculty, ensure_ascii=False, indent=2) + '\n')
    (DATA / 'paper_abstracts.json').write_text(json.dumps(abstracts, ensure_ascii=False, indent=2) + '\n')
    if scholar is not None:
        (DATA / 'scholar_order.json').write_text(json.dumps(scholar, ensure_ascii=False, indent=2) + '\n')
    print(f"Faculty: {len(faculty['papers'])} records; {len(unmatched)} unmatched titles require review")
    print(f"Verified matches: {len(abstracts['papers'])} abstracts from arXiv and OpenAlex")
    for title in unmatched:
        print('Unmatched:', title)
    if scholar is not None:
        print(f'Scholar: {len(scholar)} records in source order')


if __name__ == '__main__':
    main()
