#!/usr/bin/env python3
"""Validate a monthly Publications and Research News update before release."""

import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess


DATA = Path('assets/scripts/pub_list')
NEWS_PAGES = {Path('index.html'), Path('pages/news.html')}
SNAPSHOTS = {
    DATA / name for name in (
        'papers.json', 'papers.bundle.html', 'faculty_publications.json',
        'scholar_order.json', 'paper_abstracts.json', 'publication_versions.json',
        'reviewed_abstract_links.json', 'reviewed_publisher_abstracts.json',
    )
}
FRAGMENT = re.compile(r'synergy_\d{4}/[\w.-]+\.html', re.ASCII)
NEWS_LIST = re.compile(r'(<div class="lab-news-list">)(.*?)(</div>\s*</section>)', re.S)
NEWS_ITEM = re.compile(r'<article\b[^>]*>.*?</article>', re.S)
STATIC_TAGS = set('a article b br button div em i li ol p paper-link small span strong sub sup time ul'.split())


def git(*args):
    return subprocess.check_output(['git', *args], text=True, encoding='utf-8')


def changed_paths():
    tracked = git('diff', '--name-only', '-z', '--no-renames', 'HEAD')
    untracked = git('ls-files', '--others', '--exclude-standard', '-z')
    return {Path(path) for path in (tracked + untracked).split('\0') if path}


def base_html(path):
    if not git('ls-tree', '-r', '--name-only', 'HEAD', '--', str(path)):
        return ''
    return git('show', f'HEAD:{path}')


def active_markup(source):
    """Flag newly introduced executable markup while preserving legacy handlers."""
    class Markup(HTMLParser):
        def __init__(self):
            super().__init__()
            self.active = Counter()

        def handle_starttag(self, tag, attrs):
            if tag not in STATIC_TAGS:
                self.active[(tag,)] += 1
            for name, value in attrs:
                if name.startswith('on') or name in {'style', 'src', 'srcset', 'action', 'formaction'}:
                    self.active[(tag, name, value)] += 1
                if name == 'href' and not re.match(r'^(?:https://|\./|\.\./|#)', value or ''):
                    self.active[(tag, name, value)] += 1

    parser = Markup()
    parser.feed(source)
    parser.close()
    return parser.active


def split_news(source):
    matches = list(NEWS_LIST.finditer(source))
    if len(matches) != 1:
        raise ValueError('Expected one Research News list')
    start, end = matches[0].span(2)
    return source[:start], source[start:end], source[end:]


def news_items(news, *, papers):
    return [item for item in NEWS_ITEM.findall(news) if ('lab-news-kind--paper' in item) == papers]


def validate_changes(paths):
    for path in paths:
        is_fragment = path.is_relative_to(DATA / 'htmls') and FRAGMENT.fullmatch(
            path.relative_to(DATA / 'htmls').as_posix())
        if path not in SNAPSHOTS and path not in NEWS_PAGES and not is_fragment:
            raise ValueError(f'Unexpected changed file: {path}')
        if not path.is_file() or path.is_symlink():
            raise ValueError(f'Expected a regular file: {path}')
        if path in NEWS_PAGES:
            before_head, before, before_tail = split_news(base_html(path))
            after_head, after, after_tail = split_news(path.read_text(encoding='utf-8'))
            if (before_head, before_tail) != (after_head, after_tail):
                raise ValueError(f'Edit outside the Research News list: {path}')
            if news_items(before, papers=False) != news_items(after, papers=False):
                raise ValueError(f'Non-publication news was changed: {path}')
        elif is_fragment:
            before, after = base_html(path), path.read_text(encoding='utf-8')
        else:
            continue
        if active_markup(after) - active_markup(before):
            raise ValueError(f'Unexpected new active HTML: {path}')


def prepare(cache_key):
    paths = changed_paths()
    validate_changes(paths)
    if paths & NEWS_PAGES:
        def paper_news(source):
            _, news, _ = split_news(source)
            return {re.sub(r'\s+', ' ', item.replace('./pages/publication.html', './publication.html'))
                    for item in news_items(news, papers=True)}

        home = Path('index.html')
        archive = Path('pages/news.html')
        archive_items = paper_news(archive.read_text(encoding='utf-8'))
        previous_home = paper_news(base_html(home))
        new_home = paper_news(home.read_text(encoding='utf-8')) - previous_home
        if new_home - archive_items:
            raise ValueError('New homepage paper news must also appear on the Research News page')
    faculty_path = DATA / 'faculty_publications.json'
    if faculty_path in paths:
        before = base_html(faculty_path)
        old, new = json.loads(before), json.loads(faculty_path.read_text(encoding='utf-8'))
        new['checkedOn'] = old['checkedOn']
        if new == old:
            faculty_path.write_text(before, encoding='utf-8')

    for path in SNAPSHOTS:
        if path.suffix == '.json':
            json.loads(path.read_text(encoding='utf-8'))
    manifest = json.loads((DATA / 'papers.json').read_text(encoding='utf-8'))
    htmls = DATA / 'htmls'
    files = {path.relative_to(htmls).as_posix() for path in htmls.rglob('*.html')}
    if (not isinstance(manifest, list) or not manifest
            or not all(isinstance(name, str) and FRAGMENT.fullmatch(name) for name in manifest)
            or len(manifest) != len(set(manifest)) or set(manifest) != files):
        raise ValueError('Publication manifest must list each paper fragment exactly once')
    fragments = [(htmls / name).read_text(encoding='utf-8').strip() for name in manifest]
    if any('class="paper-title"' not in fragment or 'class="paper-authors"' not in fragment for fragment in fragments):
        raise ValueError('A publication fragment is missing its title or authors')
    (DATA / 'papers.bundle.html').write_text('\n'.join(fragments) + '\n', encoding='utf-8')

    if cache_key and any(path.is_relative_to(DATA) for path in changed_paths()):
        if not re.fullmatch(r'publication-refresh-\d+-\d+', cache_key):
            raise ValueError('Unexpected publication release version')
        for path, pattern, expected in (
            (Path('assets/js/publications.js'), r'(const VERSION_SUFFIX = \'\?v=)[^\']+', 1),
            (Path('pages/publication.html'), r'((?:papers\.bundle\.html|/publications\.js)\?v=)[^"]+', 2),
        ):
            text, count = re.subn(pattern, lambda match: match[1] + cache_key, path.read_text(encoding='utf-8'))
            if count != expected:
                raise ValueError(f'Expected {expected} publication cache versions in {path}')
            path.write_text(text, encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache-key')
    args = parser.parse_args()
    try:
        prepare(args.cache_key)
    except (OSError, ValueError) as error:
        parser.exit(1, f'{error}\n')
