import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('refresh', Path(__file__).resolve().parents[1] / 'scripts/refresh_publications.py')
refresh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(refresh)


class PublicationRefreshTest(unittest.TestCase):
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
