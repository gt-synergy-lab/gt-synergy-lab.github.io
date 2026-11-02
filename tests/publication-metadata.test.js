const test = require('node:test');
const assert = require('node:assert/strict');
const metadata = require('../assets/js/publication-metadata.js');
const snapshot = require('../assets/scripts/pub_list/faculty_publications.json');
const versions = require('../assets/scripts/pub_list/publication_versions.json');

test('every reviewed old title resolves to its confirmed publication and year', () => {
  const index = metadata.buildIndex(snapshot.papers);
  for (const review of versions.reconciliations) {
    const expected = snapshot.papers.find(p => p.title === review.title && p.venue === review.venue);
    assert.ok(expected, review.title);
    for (const title of review.matchTitles) {
      const found = metadata.findFaculty(index, { title });
      assert.equal(found.title, expected.title, title);
      assert.equal(found.venue, expected.venue, title);
      assert.equal(metadata.publicationYear({facultyYear: found.year, scholarYear: 2017}), String(expected.year), title);
    }
  }
});

test('the 2023 Chakra report is not treated as the distinct 2026 MLSys paper', () => {
  const index = metadata.buildIndex(snapshot.papers);
  assert.equal(metadata.findFaculty(index, {
    title: 'Chakra: Advancing performance benchmarking and co-design using standardized execution traces',
    ids: ['arxiv:2305.14516']
  }), null);
});

test('reviewed conference evidence corrects the upstream IMS year', () => {
  const paper = snapshot.papers.find(p => p.title.startsWith('A Configurable Architecture'));
  assert.equal(paper.year, 2022);
  assert.ok(paper.reviewSources.some(url => url.includes('IMS37962.2022')));
});

test('MIST and Demystifying use their conference year, not their preprint year', () => {
  const index = metadata.buildIndex(snapshot.papers);
  for (const [title, scholarYear, venue] of [
    ['Understanding and Optimizing Multi-Stage AI Inference Pipelines', '2025', 'SC'],
    ['Demystifying AI Platform Design for Distributed Inference of Next-Generation LLM Models', '2024', 'ICCAD']
  ]) {
    const faculty = metadata.findFaculty(index, { title });
    assert.equal(faculty.venue, venue);
    assert.equal(metadata.publicationYear({ facultyYear: faculty.year, scholarYear }), '2026');
  }
});

test('a newly accepted paper is upgraded without a title-specific frontend override', () => {
  const faculty = { title: 'New conference title', year: 2027, venue: 'SC', matchTitles: ['New conference title'], identityKeys: ['arxiv:2611.12345'] };
  const record = metadata.findFaculty(metadata.buildIndex([faculty]), {
    title: 'Earlier preprint title', ids: metadata.workIds(['https://arxiv.org/pdf/2611.12345v3.pdf'])
  });
  assert.equal(record, faculty);
  assert.equal(metadata.publicationYear({ facultyYear: record.year, scholarYear: 2026 }), '2027');
});

test('unpublished papers keep Scholar dates and local published citations override them', () => {
  assert.equal(metadata.publicationYear({ scholarYear: 2025, localYear: 2024 }), '2025');
  assert.equal(metadata.publicationYear({ publishedYear: 2026, scholarYear: 2024 }), '2026');
  assert.equal(metadata.publicationYear({ verifiedYear: 2026, scholarYear: 2025 }), '2026');
});

function record(title, venue, year, quality, identityKeys = []) {
  const isPublished = venue !== 'arXiv';
  return { title, titleKey: metadata.titleKey(title), isPublished, quality, identityKeys,
    publicationKey: metadata.publicationKey(title, venue, year, isPublished), searchText: title };
}

test('conference record replaces its differently named preprint and retains searchable aliases', () => {
  const preprint = record('Earlier title', 'arXiv', 2025, 3, ['arxiv:2504.09775']);
  const conference = record('MIST', 'SC', 2026, 20, ['arxiv:2504.09775']);
  const papers = metadata.deduplicate([preprint, conference]);
  assert.equal(papers.length, 1);
  assert.equal(papers[0].title, 'MIST');
  assert.match(papers[0].searchText, /Earlier title/);
});

test('conference and journal versions remain separate, and ambiguous identifiers are not guessed', () => {
  const conference = { title: 'Shared title', venue: 'SC', year: 2026, identityKeys: ['arxiv:2504.09775'] };
  const journal = { ...conference, venue: 'ACM TACO', year: 2027 };
  const index = metadata.buildIndex([conference, journal]);
  assert.equal(metadata.findFaculty(index, { title: 'Shared title', publishedVenue: 'SC 2026' }), conference);
  assert.equal(metadata.findFaculty(index, { title: 'Unrelated title', ids: ['arxiv:2504.09775'] }), null);
  assert.equal(metadata.deduplicate([record('Shared title', 'SC', 2026, 20), record('Shared title', 'ACM TACO', 2027, 20)]).length, 2);
});

test('nearby titles alone do not merge distinct papers', () => {
  const papers = metadata.deduplicate([record('Polestar: Calibration', 'NeurIPS', 2026, 20), record('Polestar-cache: Calibration', 'Workshop', 2025, 20)]);
  assert.equal(papers.length, 2);
});
