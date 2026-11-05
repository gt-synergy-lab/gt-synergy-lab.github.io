import importlib.util
from pathlib import Path
import json
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('refresh', Path(__file__).resolve().parents[1] / 'scripts/refresh_publications.py')
refresh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(refresh)


class PublicationRefreshTest(unittest.TestCase):
    def test_preprint_uses_original_posting_date_not_revision_date(self):
        xml = '''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
          <id>http://arxiv.org/abs/2504.09775v6</id><title>A Paper</title>
          <published>2025-04-14T00:00:00Z</published><updated>2026-10-01T00:00:00Z</updated>
          <summary>Original text.</summary></entry></feed>'''
        with patch.object(refresh, 'read_local_papers', return_value=[]):
            data = refresh.refresh_abstracts({'papers': []}, data_dir=Path('/nonexistent'), feeds=[xml])
        self.assertEqual(data['arxivDates']['2504.09775']['date'], '2025-04-14')

    def test_reviewed_abstract_alias_requires_exact_source_and_survives_refresh(self):
        faculty = {'papers': [{'title': 'Conference name', 'year': 2025, 'authors': 'Alice Smith'}]}
        arxiv = {'papers': [{'title': 'Earlier name', 'text': 'Original text',
                             'source': 'https://arxiv.org/abs/2504.09775v3'}]}
        alias = {'title': 'Conference name', 'sourceTitle': 'Earlier name',
                 'kind': 'arxiv', 'id': '2504.09775'}
        with tempfile.TemporaryDirectory() as folder, patch.object(refresh, 'read_local_papers', return_value=[]):
            path = Path(folder) / 'reviewed_abstract_links.json'
            path.write_text(json.dumps([alias]))
            output = refresh.refresh_openalex(faculty, arxiv, [], Path(folder))['papers']
            self.assertIn('Conference name', [paper['title'] for paper in output])
            alias['id'] = '2504.99999'
            path.write_text(json.dumps([alias]))
            output = refresh.refresh_openalex(faculty, arxiv, [], Path(folder))['papers']
            self.assertNotIn('Conference name', [paper['title'] for paper in output])

    def test_openalex_reconstructs_only_complete_positions(self):
        self.assertEqual(refresh.parse_openalex_abstract({'words': [1], 'Original': [0]}), 'Original words')
        self.assertEqual(refresh.parse_openalex_abstract({'Original': [0], 'words': [2]}), '')
        self.assertEqual(refresh.parse_openalex_abstract({'Original': [0], 'words': [0]}), '')

    def test_openalex_requires_matching_title_year_and_author(self):
        faculty = {'papers': [{'title': 'A Paper', 'year': 2024, 'authors': 'Alice Smith'}]}
        work = {'title': 'A Paper', 'publication_year': 2024, 'type': 'article',
                'id': 'https://openalex.org/W123', 'doi': 'https://doi.org/10.1234/test',
                'abstract_inverted_index': {'Original': [0], 'words': [1]},
                'authorships': [{'author': {'display_name': 'Alice Smith'}}]}
        with patch.object(refresh, 'read_local_papers', return_value=[]):
            result = refresh.refresh_openalex(faculty, {'papers': []}, [work])['papers']
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['text'], 'Original words')
            self.assertEqual(refresh.refresh_openalex(faculty, {'papers': []},
                [{**work, 'publication_year': 2023}])['papers'], [])
            self.assertEqual(refresh.refresh_openalex(faculty, {'papers': []},
                [{**work, 'authorships': [{'author': {'display_name': 'Bob Jones'}}]}])['papers'], [])

    def test_arxiv_feed_preserves_source_text_and_version(self):
        xml = '''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
          <id>http://arxiv.org/abs/2504.09775v6</id><title>A Paper</title>
          <summary>Original text &amp; details.\n Second sentence.</summary></entry></feed>'''
        self.assertEqual(refresh.parse_arxiv_feed(xml), [{'title': 'A Paper',
            'text': 'Original text & details. Second sentence.',
            'source': 'https://arxiv.org/abs/2504.09775v6'}])

    def test_arxiv_error_and_unversioned_ids_are_not_abstracts(self):
        xml = '''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
          <id>https://arxiv.org/abs/2504.09775</id><title>A Paper</title>
          <summary>Original text.</summary></entry></feed>'''
        self.assertEqual(refresh.parse_arxiv_feed(xml), [])
        with self.assertRaises(ValueError):
            refresh.parse_arxiv_feed('<html/>')

    def test_aliases_do_not_leak_between_journal_and_conference_editions(self):
        previous = [{'title': 'Same title', 'venue': 'IISWC',
                     'matchTitles': ['Same title', 'Preprint title'], 'identityKeys': ['arxiv:2006.07137']}]
        titles, ids, _ = refresh.match_publication({'title': 'Same title', 'v': 'IEEE CAL'}, [], previous)
        self.assertNotIn('Preprint title', titles)
        self.assertEqual(ids, [])

    def test_reviewed_alias_survives_a_refresh(self):
        local = [{'filename': 'old.html', 'title': 'Earlier title', 'alias': '',
                  'ids': set(), 'preprint': True}]
        review = {'matchTitles': ['Earlier title'], 'identityKeys': ['arxiv:2304.05301']}
        titles, ids, matched = refresh.match_publication({'title': 'Conference title', 'v': 'MICRO'}, local, [], review)
        self.assertTrue(matched)
        self.assertIn('Earlier title', titles)
        self.assertEqual(ids, ['arxiv:2304.05301'])

    def test_capture_old_title_and_stable_identifier(self):
        local = [{'filename': 'mist.html', 'title': 'MIST', 'alias': 'Earlier preprint title',
                  'ids': {'arxiv:2504.09775'}, 'preprint': False},
                 {'filename': 'old.html', 'title': 'Another preprint title', 'alias': '',
                  'ids': {'arxiv:2504.09775'}, 'preprint': True}]
        titles, ids, matched = refresh.match_publication({'title': 'MIST'}, local, [])
        self.assertTrue(matched)
        self.assertIn('Earlier preprint title', titles)
        self.assertIn('Another preprint title', titles)
        self.assertEqual(ids, ['arxiv:2504.09775'])
        # A later refresh retains the known alias after the old fragment disappears.
        next_titles, next_ids, _ = refresh.match_publication({'title': 'MIST'}, local[:1],
            [{'title': 'MIST', 'matchTitles': titles, 'identityKeys': ids}])
        self.assertIn('Another preprint title', next_titles)
        self.assertEqual(next_ids, ids)

    def test_shared_pdf_does_not_absorb_distinct_published_work(self):
        local = [{'filename': 'conference.html', 'title': 'Conference paper', 'alias': '',
                  'ids': {'arxiv:2504.09775'}, 'preprint': False},
                 {'filename': 'journal.html', 'title': 'Journal extension', 'alias': '',
                  'ids': {'arxiv:2504.09775'}, 'preprint': False}]
        titles, _, _ = refresh.match_publication({'title': 'Conference paper'}, local, [])
        self.assertNotIn('Journal extension', titles)

    def test_unknown_rename_is_reported_without_fuzzy_matching(self):
        local = [{'filename': 'old.html', 'title': 'Similar title with a different method',
                  'alias': '', 'ids': set(), 'preprint': True}]
        _, _, matched = refresh.match_publication({'title': 'Similar title with a new method'}, local, [])
        self.assertFalse(matched)

    def test_identifiers_ignore_arxiv_revisions(self):
        self.assertEqual(refresh.work_ids(['https://arxiv.org/pdf/2504.09775v3.pdf',
                                          'arXiv:2504.09775v2', 'https://doi.org/10.1145/ABC']),
                         {'arxiv:2504.09775', 'doi:10.1145/abc'})


if __name__ == '__main__':
    unittest.main()
