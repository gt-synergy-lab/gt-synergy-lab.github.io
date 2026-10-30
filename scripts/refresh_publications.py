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
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'assets/scripts/pub_list'
FACULTY_URL = 'https://tushar-krishna.github.io/publications.html'
SCHOLAR_URL = 'https://scholar.google.com/citations?user=P__ztgcAAAAJ&hl=en&sortby=pubdate&pagesize=100'

# Names absent from the faculty page's abbreviation map. Official sources:
# https://conferences.sigcomm.org/sigcomm/2026/
# https://www.glsvlsi.hosting.acm.org/archive/glsvlsi21/acm/tecs-cfp.pdf
# https://www.isfpga.org/
# https://jianmingtong.github.io/ (FastSwitch publication entry)
VENUE_NAMES = {
    'SIGCOMM': 'ACM SIGCOMM Conference',
    'ACM TECS': 'ACM Transactions on Embedded Computing Systems',
    'FPGA': 'ACM/SIGDA International Symposium on Field-Programmable Gate Arrays',
    'ACSMD@ISCA': 'Architecture, Compiler, and System Support for Multi-model DNN Workloads Workshop at ISCA',
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


def refresh_faculty(source):
    pubs = literal(source, 'PUBS')
    names = literal(source, 'VENUE_FULL')
    months = literal(source, 'VENUE_MONTH')
    if len(pubs) < 100 or not isinstance(names, dict):
        raise ValueError('Incomplete faculty data; leaving existing metadata intact')
    names = {**VENUE_NAMES, **names}
    local = {}
    for filename in json.loads((DATA / 'papers.json').read_text()):
        path = DATA / 'htmls' / filename
        match = re.search(r'<span class="paper-title">([\s\S]*?)</span>', path.read_text())
        if match:
            local[path.name] = re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]*>', '', match[1]))).strip()
    local_keys = {title_key(title) for title in local.values()}
    records = []
    unmatched = []
    for pub in pubs:
        if pub['y'] < 2015:
            continue
        titles = [pub['title']]
        for prefix, filename in ALIASES.items():
            if pub['title'].startswith(prefix) and filename in local:
                titles.append(local[filename])
        record = {
            'title': pub['title'], 'matchTitles': list(dict.fromkeys(titles)),
            'authors': pub['a'], 'year': pub['y'], 'venue': pub['v'], 'type': pub['t'],
            'month': int(pub.get('m', months.get(pub['v'], 0))),
        }
        if pub.get('si'):
            record['specialIssue'] = pub['si']
        # Do not import award notes. The lab's MLSys no-Oral correction wins.
        records.append(record)
        if not any(title_key(title) in local_keys for title in titles):
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--faculty-html', type=Path, help='Use a saved first-party page for a reproducible refresh')
    parser.add_argument('--scholar-html', type=Path, help='Use a saved first page; remaining pages are fetched')
    parser.add_argument('--skip-scholar', action='store_true')
    args = parser.parse_args()
    source = args.faculty_html.read_text() if args.faculty_html else fetch(FACULTY_URL)
    faculty, unmatched = refresh_faculty(source)
    scholar = None if args.skip_scholar else refresh_scholar(args.scholar_html.read_text() if args.scholar_html else None)
    (DATA / 'faculty_publications.json').write_text(json.dumps(faculty, ensure_ascii=False, indent=2) + '\n')
    if scholar is not None:
        (DATA / 'scholar_order.json').write_text(json.dumps(scholar, ensure_ascii=False, indent=2) + '\n')
    print(f"Faculty: {len(faculty['papers'])} records; {len(unmatched)} unmatched titles require review")
    for title in unmatched:
        print('Unmatched:', title)
    if scholar is not None:
        print(f'Scholar: {len(scholar)} records in source order')


if __name__ == '__main__':
    main()
