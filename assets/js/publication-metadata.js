(function (root) {
  'use strict';

  function titleKey(value) {
    return String(value || '').toLowerCase().replace(/&/g, ' and ')
      .replace(/[^a-z0-9]+/g, ' ').replace(/([a-z])(\d)/g, '$1 $2')
      .replace(/(\d)([a-z])/g, '$1 $2').replace(/\btowards\b/g, 'toward')
      .replace(/\btinyml\b/g, 'tiny machine learning').replace(/^special session\s+/, '')
      .replace(/\s+/g, ' ').trim();
  }

  function workIds(values) {
    const ids = new Set();
    values.forEach(value => {
      const text = String(value || '');
      for (const match of text.matchAll(/(?:arxiv\.org\/(?:abs|pdf)\/|arxiv\s*:\s*)(\d{4}\.\d{4,5})(?:v\d+)?/gi)) {
        ids.add(`arxiv:${match[1]}`);
      }
      for (const match of text.matchAll(/(?:doi\.org\/|doi\s*:\s*)(10\.\d{4,9}\/[^\s"<>?#]+)/gi)) {
        ids.add(`doi:${match[1].replace(/[.,;]+$/, '').toLowerCase()}`);
      }
    });
    return [...ids];
  }

  function buildIndex(papers) {
    const titles = new Map();
    const ids = new Map();
    const add = (map, key, paper) => {
      if (!key) return;
      if (!map.has(key)) map.set(key, new Set());
      map.get(key).add(paper);
    };
    papers.forEach(paper => {
      (paper.matchTitles || [paper.title]).forEach(title => add(titles, titleKey(title), paper));
      (paper.identityKeys || []).forEach(id => add(ids, id, paper));
    });
    return { titles, ids };
  }

  function findFaculty(index, paper) {
    const byTitle = new Set();
    [paper.title, ...(paper.aliases || [])].forEach(title => {
      (index.titles.get(titleKey(title)) || []).forEach(record => byTitle.add(record));
    });
    const byId = new Set();
    (paper.ids || []).forEach(id => (index.ids.get(id) || []).forEach(record => byId.add(record)));
    let candidates = [...(byTitle.size ? byTitle : byId)];
    // A reused identifier alone cannot choose between different published works.
    if (!byTitle.size && candidates.length > 1) return null;
    if (!candidates.length) return null;
    if (paper.publishedVenue) {
      const sameVenue = candidates.filter(record => `${record.venue} ${record.year}`.toLowerCase() === paper.publishedVenue.toLowerCase());
      if (sameVenue.length) return sameVenue[0];
      const venueOnly = paper.publishedVenue.replace(/\s+20\d{2}$/, '').toLowerCase();
      const sameSeries = candidates.filter(record => record.venue.toLowerCase() === venueOnly);
      if (sameSeries.length) candidates = sameSeries;
      // A unique faculty citation can correct an outdated local venue label.
      else if (new Set(candidates.map(record => record.venue)).size > 1) return null;
    }
    return candidates.sort((a, b) => b.year - a.year)[0];
  }

  function publicationYear({ facultyYear, verifiedYear, publishedYear, scholarYear, localYear }) {
    // Acceptance/publication metadata wins over the earlier arXiv posting year.
    return [facultyYear, verifiedYear, publishedYear, scholarYear, localYear]
      .map(value => String(value || '')).find(value => /^20\d{2}$/.test(value)) || '';
  }

  function publicationKey(title, venue, year, isPublished) {
    return isPublished ? `${titleKey(title)}|${String(venue).toLowerCase()}|${year}` : titleKey(title);
  }

  function deduplicate(records) {
    const published = records.filter(record => record.isPublished);
    const groups = new Map();
    records.forEach(record => {
      let key = record.publicationKey;
      if (!record.isPublished) {
        const matches = published.filter(candidate => candidate.titleKey === record.titleKey
          || record.identityKeys.some(id => candidate.identityKeys.includes(id)));
        const keys = new Set(matches.map(candidate => candidate.publicationKey));
        if (keys.size === 1) key = [...keys][0];
      }
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(record);
    });
    return [...groups.values()].map(group => {
      const best = group.reduce((winner, record) => record.quality > winner.quality ? record : winner);
      return { ...best, searchText: [...new Set(group.map(record => record.searchText))].join(' '), versions: group };
    });
  }

  const api = { titleKey, workIds, buildIndex, findFaculty, publicationYear, publicationKey, deduplicate };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.PublicationMetadata = api;
})(typeof window !== 'undefined' ? window : globalThis);
