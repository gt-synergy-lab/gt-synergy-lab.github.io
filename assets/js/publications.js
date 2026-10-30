(function () {
  'use strict';

  const VERSION_SUFFIX = '?v=publications-20261030';

  const TOPICS = [
    {
      id: 'accelerators',
      label: 'AI/ML Accelerators',
      shortLabel: 'Accelerators',
      description: 'Microarchitecture, dataflows, mapping, sparsity, and quantization-aware hardware.',
      color: '#0d7a6b',
      tags: ['accelerators', 'accelerator', 'fpga', 'sparsity', 'quantization', 'dataflow'],
      keywords: [/\baccelerator/, /\bdataflow\b/, /\bdata reuse\b/, /\bgemm\b/, /\bsystolic\b/, /\bcompute[- ]in[- ]memory\b/, /\bcim\b/, /\bsparsity\b/, /\bquantization\b/, /\bfpga\b/, /\bnpu(s)?\b/, /\bdnn\b/, /\bcnn\b/, /\bcgra\b/, /\btensor (processing unit|algebra)\b/, /\bneural processing unit\b/, /\bspatial architecture/, /\bai architectures?\b/, /\bartificial intelligence focused architectures\b/]
    },
    {
      id: 'compositional',
      label: 'Compositional & Cognitive AI',
      shortLabel: 'Compositional AI',
      description: 'Neuro-symbolic, agentic, multi-model, and cognitive AI systems and hardware.',
      color: '#6d4ed6',
      tags: ['nsymbolic'],
      keywords: [/\bneuro[- ]symbolic\b/, /\bneurosymbolic\b/, /\bsymbolic\b/, /\bcognitive\b/, /\bcompositional\b/, /\bsystem[- ]2\b/, /\bvector[- ]symbolic\b/, /\bagentic\b/, /\bmulti[- ]agent\b/, /\bprobabilistic logical\b/, /\benergy[- ]based model/]
    },
    {
      id: 'distributed',
      label: 'Distributed AI Systems',
      shortLabel: 'Distributed AI',
      description: 'Training and inference platforms, collective communication, scheduling, and networks.',
      color: '#2563c9',
      tags: ['distributed'],
      keywords: [/\bdistributed\b/, /\bdatacenter\b/, /\bdata center\b/, /\bcluster\b/, /\bcollective\b/, /\bmulti[- ]node\b/, /\bscale[- ]up\b/, /\bscale[- ]out\b/, /\ball[- ]reduce\b/]
    },
    {
      id: 'llm',
      label: 'Efficient LLM & Model Inference',
      shortLabel: 'LLM & Inference',
      description: 'Model serving, attention optimization, quantization, and private inference.',
      color: '#c2410c',
      tags: ['llm'],
      keywords: [/\bllms?\b/, /\blanguage model/, /\btransformer\b/, /\battention\b/, /\bkv cache\b/, /\bvision transformer\b/, /\bvit\b/, /\bmamba\b/, /\bsmall language model/, /\blarge model inference/]
    },
    {
      id: 'ai-design',
      label: 'AI-Assisted Design',
      shortLabel: 'AI-Assisted Design',
      description: 'Learning-guided mapping, architecture search, and design-space optimization.',
      color: '#b3357a',
      tags: [],
      keywords: [/\bai[- ]assisted\b/, /\bml[- ]assisted\b/, /\breinforcement learning\b/, /\bevolutionary search\b/, /\bgenetic algorithm\b/, /\bdesign[- ]space (search|optimization|exploration)\b/, /\barchitecture search\b/, /\blearning[- ]based (mapping|design)\b/]
    },
    {
      id: 'noc',
      label: 'Interconnection & On-Chip Networks',
      shortLabel: 'Interconnects / NoC',
      description: 'NoCs, deadlock freedom, routers, traversal, topology, and link design.',
      color: '#3b4b8a',
      tags: ['noc'],
      keywords: [/\bnocs?\b/, /\bnetwork[- ]on[- ]chip\b/, /\bon[- ]chip network\b/, /\binterconnect/, /\bnetwork fabric\b/, /\brouting\b/, /\brouter\b/, /\btopolog/, /\bdeadlock\b/, /\bminimum[- ]cycle maximum[- ]hop network\b/, /\badaptive manycore\b/]
    },
    {
      id: 'simulation',
      label: 'Simulation & Benchmarking',
      shortLabel: 'Simulation',
      description: 'Simulators, analytical models, workload characterization, and benchmarks.',
      color: '#b08400',
      tags: ['simulation', 'mlhw'],
      keywords: [/\bsimulat/, /\bbenchmark/, /\bmodeling\b/, /\bmodelling\b/, /\bcharacteriz/, /\bworkload analysis\b/, /\bworkload trace/, /\banalytical model/, /\bdesign[- ]space exploration\b/, /\bdse\b/]
    },
    {
      id: 'emerging',
      label: 'Emerging Tech & Packaging',
      shortLabel: 'Emerging Tech',
      description: 'Compute-in-memory, chiplets, 3D integration, and novel interconnects.',
      color: '#2e8b57',
      tags: ['emerging'],
      keywords: [/\bcompute[- ]in[- ]memory\b/, /\b3d[- ]stack/, /\b3-d[- ]stack/, /\b2\.5d\b/, /\bchiplet/, /\binterposer\b/, /\bphotonic\b/, /\bwireless (network|interconnect)/, /\brf (network|interconnect)/, /\brram\b/, /\bmemrist/, /\bmonolithic/, /\badvanced packaging\b/]
    },
    {
      id: 'memory',
      label: 'Memory & Virtual-Memory Systems',
      shortLabel: 'Memory Systems',
      description: 'TLBs, translation coherence, caches, and stacked memory systems.',
      color: '#8a5a2b',
      tags: [],
      keywords: [/\btlb\b/, /\becotlb\b/, /\bvipt\b/, /\bvirtual memory\b/, /\bunified[- ]memory\b/, /\btranslation coherence\b/, /\bcache\b/, /\bcaches\b/, /\bmemory hierarchy\b/, /\bstacked memory\b/, /\bhybrid memory cube\b/, /\bhbm\b/]
    },
    {
      id: 'edge',
      label: 'Edge & Embodied Computing',
      shortLabel: 'Edge & Embodied',
      description: 'On-device learning, edge platforms, neuroevolution, and autonomous systems.',
      color: '#c0392b',
      tags: [],
      keywords: [/\bedge computing\b/, /\bedge cluster\b/, /\bedge[- ]centric\b/, /\bon[- ]device\b/, /\bembodied\b/, /\bautonomous system/, /\brobot/, /\bvirtual reality\b/, /\bneuroevolution\b/, /\bneural network evolution\b/, /\bcontinuous learning\b/, /\btinyml\b/, /\btiny machine learning\b/, /\bmobile (graphics|platform|device)/]
    },
    {
      id: 'security',
      label: 'Privacy & Security',
      shortLabel: 'Privacy & Security',
      description: 'Cryptographic acceleration, confidential computing, and secure computation.',
      color: '#475569',
      tags: ['memoryauthentication'],
      keywords: [/\bprivacy\b/, /\bprivate inference\b/, /\bprivacy[- ]preserving\b/, /\bsecurity\b/, /\bsecure\b/, /\bcryptograph/, /\bhomomorphic\b/, /\bfhe\b/, /\bzero[- ]knowledge\b/, /\bzkp\b/, /\bconfidential\b/, /\bauthentication\b/, /\badversarial\b/, /\bside[- ]channel\b/]
    }
  ];

  const TOPIC_ALIASES = {
    ai: 'llm',
    agentic: 'compositional',
    nsymbolic: 'compositional'
  };

  const VERIFIED_META = [
    { pattern: /^polestar: drift-aware/i, venue: 'NeurIPS 2026' },
    { pattern: /^mist:/i, venue: 'SC 2026' },
    { pattern: /^dynamoserve:/i, venue: 'SIGCOMM 2026' },
    { pattern: /^scalable synthesis of distributed llm workloads/i, venue: 'ISCA 2026' },
    { pattern: /^scale-sim tpu:/i, venue: 'IEEE CAL 2026' },
    { pattern: /^cross-layer design of vector-symbolic computing/i, venue: 'ACM TECS 2026' },
    { pattern: /demystifying ai platform design for distributed inference/i, venue: 'ICCAD 2026' },
    { pattern: /enabling ai asics for zero knowledge proof/i, venue: 'DAC 2026' },
    { pattern: /closing the efficiency gap/i, venue: 'ICS 2026' },
    { pattern: /thunderagent/i, venue: 'ICML 2026', note: 'Spotlight' },
    { pattern: /^quarch:/i, venue: 'ICML 2026' },
    // Lab correction (2026-10-29): these MLSys papers have no Oral designation.
    { pattern: /mlcommons chakra/i, venue: 'MLSys 2026' },
    { pattern: /privatar/i, venue: 'MLSys 2026' },
    { pattern: /slm-mux/i, venue: 'ICLR 2026' },
    { pattern: /thinn?kv/i, venue: 'ICLR 2026', note: 'Oral' },
    { pattern: /minisa/i, venue: 'ISPASS 2026', note: 'Distinguished Artifact Honorable Mention' },
    { pattern: /evaluating cross-architecture performance/i, venue: 'ISPASS 2026' },
    { pattern: /towards system-2 ai/i, venue: 'ISPASS 2026' },
    { pattern: /algorithm.hardware co-design of digital compute-in-memory/i, venue: 'IEEE TVLSI 2026' },
    { pattern: /compositional ai beyond llms/i, venue: 'ASPLOS 2026' },
    { pattern: /fortisky/i, venue: 'DATE 2026' },
    { pattern: /^reason:/i, venue: 'HPCA 2026' },
    { pattern: /leveraging asic ai chips/i, venue: 'HPCA 2026' },
    { pattern: /^scale: tackling communication/i, venue: 'HPCA 2026' },
    { pattern: /boosting scalability and performance: macro placement/i, venue: 'ASP-DAC 2026' },
    { pattern: /40-nm programmable heterogeneous soc/i, venue: 'IEEE JSSC 2026' },
    { pattern: /demystifying the cost versus benefits of sparse (llm|large language model) acceleration/i, venue: 'IEEE Micro 2026' },
    { pattern: /win fast or lose slow/i, venue: 'NeurIPS 2025', note: 'Spotlight' }
  ];

  const ARTIFACT_TITLES = new Set([
    'Buffer Hierarchies',
    'Dataflow and Data Reuse',
    'Flow Control',
    'Interface with System Architecture',
    'Introduction to Data Orchestration',
    'Modeling Accelerator Design Space',
    'Modeling and Evaluation',
    'Networks-on-Chip',
    'On-chip Networks',
    'Orchestrating Compressed-Sparse Data',
    'Putting it Together: Architecting a DNN Accelerator',
    'Router Microarchitecture',
    'Routing',
    'Proceedings of the 15th IEEE/ACM International Symposium on Networks-on-chip',
    'ARIAA: Progress ReportMay 2020.'
  ].map(normalizeTitleKey));

  const state = {
    papers: [],
    scholarOrder: new Map(),
    facultyPapers: new Map(),
    venueNames: {},
    activeTopics: new Set(),
    query: ''
  };

  window.expand_abstract = function (id) {
    window.closeAbstract();
    const overlay = document.getElementById('publicationAbstractOverlay');
    const target = document.getElementById(id);
    if (!overlay || !target) return;
    overlay.style.display = 'block';
    target.style.display = 'block';
    document.body.classList.add('publication-modal-open');
    const closeButton = target.querySelector('.close-btn');
    if (closeButton) closeButton.focus();
  };

  window.closeAbstract = function () {
    document.querySelectorAll('.abstract-section').forEach(section => {
      section.style.display = 'none';
    });
    document.querySelectorAll('.abstract-overlay').forEach(overlay => {
      overlay.style.display = 'none';
    });
    document.body.classList.remove('publication-modal-open');
  };

  window.toggleTags = function () {};

  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') window.closeAbstract();
  });

  document.addEventListener('DOMContentLoaded', initializePublications);

  async function initializePublications() {
    const container = document.getElementById('paper-container');
    if (!container) return;

    wireControls(container);

    try {
      const [elements, scholarOrder, faculty] = await Promise.all([
        loadBundledPapers().catch(loadPaperFiles),
        loadScholarOrder(),
        loadFacultyMetadata()
      ]);
      state.scholarOrder = prepareScholarOrder(scholarOrder);
      state.facultyPapers = prepareFacultyMetadata(faculty.papers || []);
      state.venueNames = faculty.venueNames || {};
      state.papers = preparePapers(elements);
      initializeFiltersFromUrl();
      renderTopicFilters();
      renderPublications();
    } catch (error) {
      container.innerHTML = '<div class="publication-error"><strong>Publications could not be loaded.</strong><span>Refresh the page or confirm that the site is running through a local server.</span></div>';
      console.error(error);
    }
  }

  async function loadBundledPapers() {
    const response = await fetch(`../assets/scripts/pub_list/papers.bundle.html${VERSION_SUFFIX}`);
    if (!response.ok) throw new Error('Could not load papers.bundle.html');
    return parsePaperElements(await response.text());
  }

  async function loadPaperFiles() {
    const response = await fetch(`../assets/scripts/pub_list/papers.json${VERSION_SUFFIX}`);
    if (!response.ok) throw new Error('Could not load papers.json');
    const files = await response.json();
    const htmlFiles = await Promise.all(files.map(async file => {
      const paperResponse = await fetch(`../assets/scripts/pub_list/htmls/${file}${VERSION_SUFFIX}`);
      if (!paperResponse.ok) return '';
      return paperResponse.text();
    }));
    return htmlFiles.flatMap(parsePaperElements);
  }

  async function loadScholarOrder() {
    try {
      const response = await fetch(`../assets/scripts/pub_list/scholar_order.json${VERSION_SUFFIX}`);
      if (!response.ok) return [];
      const entries = await response.json();
      return Array.isArray(entries) ? entries : [];
    } catch (error) {
      console.warn('Google Scholar order could not be loaded; using publication dates.', error);
      return [];
    }
  }

  function prepareScholarOrder(entries) {
    const order = new Map();
    entries.forEach((entry, rank) => {
      const titleKey = normalizeTitleKey(entry && entry.title);
      if (!titleKey || order.has(titleKey)) return;
      order.set(titleKey, {
        rank,
        year: /^20\d{2}$/.test(String(entry.year || '')) ? String(entry.year) : ''
      });
    });
    return order;
  }

  async function loadFacultyMetadata() {
    try {
      const response = await fetch(`../assets/scripts/pub_list/faculty_publications.json${VERSION_SUFFIX}`);
      if (!response.ok) throw new Error('Could not load faculty publication metadata');
      return await response.json();
    } catch (error) {
      console.warn('Faculty metadata unavailable; using local citations.', error);
      return {};
    }
  }

  function prepareFacultyMetadata(papers) {
    const metadata = new Map();
    papers.forEach(paper => {
      (paper.matchTitles || [paper.title]).forEach(title => {
        const key = normalizeTitleKey(title);
        if (!metadata.has(key)) metadata.set(key, []);
        metadata.get(key).push(paper);
      });
    });
    return metadata;
  }

  function findScholarMetadata(title, aliases, faculty) {
    // Known title variants in Scholar; keep its original rank after a rename.
    const variants = [
      [/^serving agentic workflows with a physical-plan compiler/i, 'A Workflow-Aware Serving Layer for Agentic Applications'],
      [/^thunderagent:/i, 'Thunderagent: A simple, fast and program-aware agentic inference system'],
      [/^demystifying the cost versus benefits of sparse/i, 'Demystifying the cost versus benefits of sparse LLM acceleration']
    ];
    const variant = variants.find(([pattern]) => pattern.test(title));
    const matches = [title, aliases, faculty && faculty.title, variant && variant[1]]
      .map(candidate => state.scholarOrder.get(normalizeTitleKey(candidate))).filter(Boolean);
    // Scholar can include an undated duplicate of a dated paper under its new title.
    return matches.find(match => match.year) || matches[0] || null;
  }

  function parsePaperElements(html) {
    const wrapper = document.createElement('div');
    wrapper.innerHTML = html.trim();
    const papers = Array.from(wrapper.querySelectorAll('.paper'));
    if (!papers.length && html.trim()) return [];
    return papers;
  }

  function preparePapers(elements) {
    const recordsByTitle = new Map();

    elements.forEach((element, originalIndex) => {
      const record = preparePaper(element, originalIndex);
      if (!record || ARTIFACT_TITLES.has(record.titleKey)) return;

      const existing = recordsByTitle.get(record.titleKey);
      if (!existing || record.quality > existing.quality) {
        recordsByTitle.set(record.titleKey, record);
      }
    });

    return Array.from(recordsByTitle.values());
  }

  function preparePaper(element, originalIndex) {
    const titleElement = element.querySelector('.paper-title');
    const authorsElement = element.querySelector('.paper-authors');
    if (!titleElement || !authorsElement) return null;

    const title = cleanText(titleElement.textContent);
    const rawAuthors = cleanText(authorsElement.textContent);
    const titleKey = normalizeTitleKey(title);
    if (!titleKey) return null;

    const date = getPaperDate(element);
    const verified = VERIFIED_META.find(item => item.pattern.test(title));
    const conferenceElement = element.querySelector('.paper-conference');
    const rawVenue = conferenceElement ? cleanText(conferenceElement.textContent) : '';
    const candidates = state.facultyPapers.get(titleKey) || [];
    const faculty = candidates.find(paper => String(paper.year) === date.year
      && normalizeVenueText(rawVenue, date.year, false, false).includes(paper.venue))
      || candidates.find(paper => String(paper.year) === date.year)
      || candidates[0];
    const authors = faculty ? cleanText(faculty.authors) : rawAuthors;
    const scholarMeta = findScholarMetadata(title, element.dataset.searchAliases, faculty);
    const links = element.querySelector('.paper-links');
    const paperLink = findPaperLink(links);
    const hasArxivLink = Boolean(links && links.querySelector('a[href*="arxiv.org"]'));
    const isPublished = Boolean(faculty || verified || (rawVenue && !/\barxiv\b|^corr\b|\bpreprint\b/i.test(rawVenue)));
    const isArxiv = !isPublished && (hasArxivLink || /\barxiv\b|^corr\b/i.test(rawVenue));
    const isPreprint = !isPublished;
    const venue = faculty ? `${faculty.venue} ${faculty.year}` : verified
      ? verified.venue
      : normalizeVenueText(rawVenue, date.year, isArxiv, isPreprint);
    const venueYearMatch = venue.match(/\b(20\d{2})\b/);
    const venueYear = venueYearMatch ? Number(venueYearMatch[1]) : 0;
    // Group and order by Scholar's date; the citation retains the actual venue year.
    const publicationYear = (scholarMeta && scholarMeta.year)
      || ((faculty || verified) && venueYear >= 2015 ? String(venueYear) : '')
      || date.year
      || (venueYear >= 2015 ? String(venueYear) : '');
    const publicationMonth = date.key ? date.key % 100 : 1;
    const publicationDateKey = publicationYear
      ? (Number(publicationYear) * 100) + publicationMonth
      : date.key;
    const rawTagIds = Array.from(element.querySelectorAll('paper-link.anchor[id]'))
      .map(anchor => anchor.id.trim().toLowerCase())
      .filter(id => !/^\d{4}-\d{2}$/.test(id));
    const curatedTopicIds = (element.dataset.topicIds || '').split(/\s+/).filter(Boolean);
    const topics = curatedTopicIds.length
      ? TOPICS.filter(topic => curatedTopicIds.includes(topic.id))
      : inferTopics(rawTagIds, `${title} ${authors} ${venue}`);

    titleElement.textContent = title;
    authorsElement.textContent = authors;
    element.classList.add('publication-record');
    element.classList.toggle('publication-record--preprint', isPreprint);
    element.classList.toggle('publication-record--arxiv', isArxiv);
    element.setAttribute('role', 'article');
    element.dataset.topics = topics.map(topic => topic.id).join(' ');
    element.dataset.publicationStatus = isPublished ? 'published' : 'preprint';

    const existingTitleRow = titleElement.closest('.paper-title-row');
    if (existingTitleRow) existingTitleRow.replaceWith(titleElement);
    const titleBreak = titleElement.nextElementSibling;
    if (titleBreak && titleBreak.tagName === 'BR') titleBreak.remove();
    element.querySelectorAll('.paper-visible-tags, .paper-year, .dropdown, .abstract-overlay').forEach(node => node.remove());

    decorateActionLinks(links);

    const content = element.querySelector('.paper-entry .col-12');
    if (!content) return null;

    const titleRow = document.createElement('div');
    titleRow.className = 'paper-title-row';
    content.insertBefore(titleRow, titleElement);
    titleRow.appendChild(titleElement);

    const venueRow = document.createElement('div');
    venueRow.className = 'paper-venue-row';
    const venueElement = conferenceElement || document.createElement('span');
    venueElement.className = 'paper-conference';
    if (isPreprint) venueElement.classList.add('paper-conference--preprint');
    if (isArxiv) venueElement.classList.add('paper-conference--arxiv');
    const citation = formatCitation(faculty, rawVenue, venue, venueYear || publicationYear, isArxiv, isPreprint, links);
    renderCitation(venueElement, citation, faculty, venue, isPreprint);
    titleRow.appendChild(createVenueBadge(venue, venueYear || publicationYear, isArxiv, isPreprint, citation));
    venueRow.appendChild(venueElement);
    if (verified && verified.note) {
      const note = document.createElement('span');
      note.className = 'paper-award-note';
      note.innerHTML = '<i class="fas fa-award" aria-hidden="true"></i>';
      note.appendChild(document.createTextNode(verified.note));
      venueRow.appendChild(note);
    }
    authorsElement.insertAdjacentElement('afterend', venueRow);

    if (topics.length) {
      const tagRow = document.createElement('div');
      tagRow.className = 'paper-visible-tags';
      topics.forEach(topic => tagRow.appendChild(createPaperTag(topic)));
      venueRow.insertAdjacentElement('afterend', tagRow);
    }

    const searchText = normalizeSearchText(`${title} ${element.dataset.searchAliases || ''} ${authors} ${venue} ${citation} ${topics.map(topic => topic.label).join(' ')}`);
    const quality = (isPreprint ? 0 : 4)
      + (paperLink ? 2 : 0)
      + (element.querySelector('.abstract-text') ? 1 : 0)
      + (links && /code/i.test(links.textContent) ? 1 : 0);

    return {
      element,
      title,
      titleKey,
      authors,
      authorsElement,
      venue,
      isArxiv,
      isPreprint,
      isPublished,
      topics,
      searchText,
      scholarRank: scholarMeta ? scholarMeta.rank : null,
      dateKey: publicationDateKey,
      year: publicationYear || 'Undated',
      originalIndex,
      quality
    };
  }

  function getPaperDate(element) {
    let newest = '';
    element.querySelectorAll('paper-link.anchor[id]').forEach(anchor => {
      const id = anchor.id.trim();
      if (/^\d{4}-\d{2}$/.test(id) && id > newest) newest = id;
    });
    if (!newest) return { label: '', year: '', key: 0 };
    const parts = newest.split('-').map(Number);
    return {
      label: newest,
      year: String(parts[0]),
      key: (parts[0] * 100) + parts[1]
    };
  }

  function formatCitation(faculty, rawVenue, venue, year, isArxiv, isPreprint, links) {
    const months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'];
    if (faculty) {
      const full = state.venueNames[faculty.venue] || faculty.venue;
      if (faculty.type === 'conf' || faculty.type === 'workshop') {
        const month = months[faculty.month] || '';
        return `In Proceedings of the ${full} (${faculty.venue}), ${month ? month + ' ' : ''}${faculty.year}.`;
      }
      const issue = faculty.specialIssue ? ` (${faculty.specialIssue})` : '';
      return `${full}${issue}, ${faculty.year}.`;
    }
    if (isArxiv) {
      const arxivLink = links && links.querySelector('a[href*="arxiv.org/"]');
      const identifier = `${rawVenue} ${arxivLink ? arxivLink.href : ''}`.match(/\b(\d{4}\.\d{4,5})(?:v\d+)?\b/);
      return `arXiv preprint${identifier ? ' arXiv:' + identifier[1] : ''}${year ? ', ' + year : ''}.`;
    }
    if (isPreprint) return `Preprint${year ? ', ' + year : ''}.`;
    const acronym = venue.replace(/\s+20\d{2}$/, '');
    const full = state.venueNames[acronym];
    const raw = cleanText(rawVenue).replace(/\\&/g, '&').replace(/\\textendash/g, '–').replace(/\{([^{}]+)\}/g, '$1');
    // Preserve volume, issue, and page details when the local citation has them.
    if (/\b(?:vol\.|pp\.|pages|volume)\b|\d+\s*\(\d+\)/i.test(raw)) return raw;
    if (full) return `${full}${full === acronym ? '' : ` (${acronym})`}${year ? ', ' + year : ''}.`;
    return `${raw.replace(/[.,\s]+$/, '')}${year && !raw.includes(year) ? ', ' + year : ''}.`;
  }

  function renderCitation(element, citation, faculty, venue, isPreprint) {
    element.replaceChildren();
    if (isPreprint) {
      element.textContent = citation;
      return;
    }
    const acronym = faculty ? faculty.venue : venue.replace(/\s+20\d{2}$/, '');
    const fullName = state.venueNames[acronym];
    const name = fullName && citation.includes(fullName) ? fullName : citation
      .replace(/^In Proceedings of the /, '')
      .replace(/,?\s+(?:(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+)?20\d{2}\.?$/, '')
      .replace(/^20\d{2}\s+/, '');
    const start = citation.indexOf(name);
    if (!name || start === -1) {
      element.textContent = citation;
      return;
    }
    const strong = document.createElement('strong');
    strong.textContent = name;
    element.append(document.createTextNode(citation.slice(0, start)), strong,
      document.createTextNode(citation.slice(start + name.length)));
  }

  function createVenueBadge(venue, year, isArxiv, isPreprint, citation) {
    let label = venue.replace(/\s+20\d{2}$/, '').replace(/^(?:IEEE\/ACM|ACM\/IEEE|IEEE|ACM)\s+/, '');
    if (/^IEEE Micro\b/.test(venue)) label = 'IEEE Micro';
    if (isPreprint) label = isArxiv ? 'arXiv' : 'Preprint';
    else if (label.length > 22 || label.split(/\s+/).length > 3) {
      label = /workshop/i.test(venue) ? 'Workshop' : /synthesis lectures|chapter/i.test(venue) ? 'Book' : 'Publication';
    }
    // Each venue keeps the same muted color across years; preprints remain neutral.
    const colors = ['#245b91', '#7046a2', '#16756b', '#846216', '#a03b63', '#9a4f22', '#405798', '#40712f'];
    const preferred = { SC: 0, NeurIPS: 1, MLSys: 2, ISCA: 3, MICRO: 4, HPCA: 5, ICML: 6, ICLR: 7 };
    const hash = Array.from(label).reduce((sum, char) => sum + char.charCodeAt(0), 0);
    const color = isPreprint ? '#627182' : colors[preferred[label] ?? hash % colors.length];
    const badge = document.createElement('span');
    badge.className = 'paper-venue-badge';
    badge.style.setProperty('--venue-color', color);
    badge.style.setProperty('--venue-tint', `${color}0d`);
    badge.style.setProperty('--venue-border', `${color}40`);
    badge.textContent = `${label}${year ? ' ' + String(year).slice(-2) : ''}`;
    badge.title = citation;
    return badge;
  }

  function inferTopics(rawTagIds, sourceText) {
    const tags = new Set(rawTagIds);
    const text = sourceText.toLowerCase();
    return TOPICS.filter(topic => (
      topic.tags.some(tag => tags.has(tag))
      || topic.keywords.some(pattern => pattern.test(text))
    ));
  }

  function normalizeVenueText(rawText, fallbackYear, isArxiv, isPreprint) {
    let text = cleanText(rawText)
      .replace(/\\?\{?\\&\}?/g, '&')
      .replace(/\\?\{?\\textendash\}?/g, '-')
      .trim();
    // An arXiv identifier such as 2007.03176 is not the publication year.
    const yearMatch = isArxiv || isPreprint ? null : text.match(/\b(20\d{2})\b/);
    const year = yearMatch ? yearMatch[1] : fallbackYear;
    if (isArxiv) return year ? `arXiv preprint \u00b7 ${year}` : 'arXiv preprint';
    if (isPreprint || !text) return year ? `Preprint \u00b7 ${year}` : 'Preprint';

    const venues = [
      ['ACSMD@ISCA', /architecture, compiler, and system support for multi-model dnn/i],
      ['ASP-DAC', /\basp-?dac\b/i],
      ['CODES+ISSS', /codes\+?\s*isss|hardware\/software codesign/i],
      ['HotInfra', /hot topics in system infrastructure|\bhotinfra\b/i],
      ['IEEE TVLSI', /transactions on very large scale integration|\btvlsi\b/i],
      ['IEEE JSSC', /journal of solid-state circuits|\bjssc\b/i],
      ['IEEE Micro', /\bieee micro\b/i],
      ['ACM TACO', /transactions on architecture and code optimization|\btaco\b/i],
      ['ISCA', /international symposium on computer architecture|annual international symposium on computer|\bisca\b/i],
      ['MICRO', /international symposium on microarchitecture|52nd annual ieee\/acm international symposium|\bmicro\b/i],
      ['HPCA', /high performance computer architecture|international symposium on high-perform|\bhpca\b/i],
      ['ASPLOS', /\basplos\b|architectural support for programming languages|international conference on architectural\s*(?:\u2026|\.\.\.)/i],
      ['MLSys', /machine learning (for|and) (computer architecture and )?systems|\bmlsys\b/i],
      ['ICML', /international conference on machine learning|\bicml\b/i],
      ['ICLR', /learning representations|\biclr\b/i],
      ['NeurIPS', /\bneurips\b|neural information processing systems/i],
      ['ICCV', /\biccv\b|international conference on computer vision/i],
      ['ICCAD', /computer-aided design|\biccad\b/i],
      ['ICS', /international conference on supercomputing|\bics\b/i],
      ['SC', /supercomputing|high performance com|high performance computing, networking, storage and analysis|\bsc\d{2}\b/i],
      ['ISPASS', /performance analysis of systems and software|international symposium on performance|\bispass\b/i],
      ['IISWC', /workload characterization|\biiswc\b/i],
      ['DAC', /design automation conference|\bdac\b/i],
      ['DATE', /design, automation (and|&) test in europe|\bdate\b/i],
      ['IPDPS', /parallel and distributed processing symposium|\bipdps\b/i],
      ['NOCS', /networks?[- ]on[- ]chip|workshop on network on chip|\bnocs\b/i],
      ['HotI', /hot interconnects|\bhoti\b/i],
      ['FPGA', /field[- ]programmable gate arrays|acm\/sigda international symposium on field|field progr/i],
      ['IEEE T-Radar', /\btradar\b/i],
      ['PACT', /parallel architectures and compilation|conference on parallel ar/i],
      ['ISCAS', /circuits and systems|\biscas\b/i],
      ['ISLPED', /low power electronics and design|\bislped\b/i],
      ['CPAL', /\bcpal\b/i],
      ['NeuS', /\bneus\b/i]
    ];

    for (const venue of venues) {
      if (venue[1].test(text)) return year ? `${venue[0]} ${year}` : venue[0];
    }

    const acronym = text.match(/\(([A-Z][A-Z0-9+.-]{2,})\)/);
    if (acronym) return year ? `${acronym[1]} ${year}` : acronym[1];

    text = text
      .replace(/^Proceedings of (the )?/i, '')
      .replace(/^Proc\.?\s+/i, '')
      .replace(/\s*\(Best Paper[^)]*\)\s*/i, '')
      .trim();
    if (text.length > 52) text = `${text.slice(0, 49).trim()}...`;
    if (year && !text.includes(year)) text = `${text} ${year}`;
    return text;
  }

  function highlightAuthorQuery(element, authors, query) {
    element.replaceChildren();
    if (!query) {
      element.textContent = authors;
      return;
    }

    const haystack = authors.toLowerCase();
    const needle = query.toLowerCase();
    let cursor = 0;
    let matchIndex = haystack.indexOf(needle);

    while (matchIndex !== -1) {
      element.appendChild(document.createTextNode(authors.slice(cursor, matchIndex)));
      const strong = document.createElement('strong');
      strong.className = 'paper-author-match';
      strong.textContent = authors.slice(matchIndex, matchIndex + needle.length);
      element.appendChild(strong);
      cursor = matchIndex + needle.length;
      matchIndex = haystack.indexOf(needle, cursor);
    }

    element.appendChild(document.createTextNode(authors.slice(cursor)));
  }

  function findPaperLink(links) {
    if (!links) return null;
    return Array.from(links.querySelectorAll('a[href]')).find(link => (
      /^(paper|pdf)$/i.test(cleanText(link.textContent))
      && !link.getAttribute('href').startsWith('javascript:')
    )) || null;
  }

  function decorateActionLinks(links) {
    if (!links) return;
    links.querySelectorAll('.dropdown').forEach(dropdown => dropdown.remove());
    links.querySelectorAll('.paper-action').forEach(link => {
      const label = cleanText(link.textContent).replace(/^(?:📄|📑|💻|🏷️)\s*/u, '');
      const lower = label.toLowerCase();
      let icon = 'fa-external-link-alt';
      if (lower.includes('abstract') || lower.includes('summary')) icon = 'fa-align-left';
      if (lower.includes('paper') || lower.includes('pdf')) icon = 'fa-file-alt';
      if (lower.includes('code')) icon = 'fa-code';
      link.replaceChildren();
      const iconElement = document.createElement('i');
      iconElement.className = `fas ${icon}`;
      iconElement.setAttribute('aria-hidden', 'true');
      const labelElement = document.createElement('span');
      labelElement.textContent = label;
      link.append(iconElement, labelElement);
      if (link.target === '_blank') link.rel = 'noopener';
    });
  }

  function createPaperTag(topic) {
    const tag = document.createElement('button');
    tag.type = 'button';
    tag.className = 'paper-tag';
    tag.dataset.topic = topic.id;
    tag.style.color = topic.color;
    tag.style.borderColor = `${topic.color}55`;
    tag.style.backgroundColor = `${topic.color}12`;
    tag.textContent = topic.shortLabel || topic.label;
    return tag;
  }

  function wireControls(container) {
    const search = document.getElementById('publication-search-input');
    if (search) {
      search.addEventListener('input', event => {
        state.query = normalizeSearchText(event.target.value);
        refreshFilters();
      });
    }

    container.addEventListener('click', event => {
      const tag = event.target.closest('.paper-tag[data-topic]');
      if (tag) toggleTopic(tag.dataset.topic);
    });

    document.getElementById('publication-topic-filters').addEventListener('click', event => {
      const button = event.target.closest('.filter-button[data-topic]');
      if (button) toggleTopic(button.dataset.topic);
    });
  }

  function toggleTopic(id) {
    if (!id) state.activeTopics.clear();
    else if (state.activeTopics.has(id)) state.activeTopics.delete(id);
    else state.activeTopics.add(id);
    refreshFilters();
  }

  function refreshFilters() {
    updateFiltersInUrl();
    renderTopicFilters();
    renderPublications();
  }

  function initializeFiltersFromUrl() {
    const params = new URLSearchParams(window.location.search);
    const requestedTopics = params.getAll('topic').flatMap(value => value.split(','));
    state.activeTopics = new Set(requestedTopics.map(id => TOPIC_ALIASES[id] || id)
      .filter(id => TOPICS.some(topic => topic.id === id)));
    // Retired controls must not leave hidden filters or ordering in shared URLs.
    if (params.has('status') || params.has('sort')) {
      const url = new URL(window.location.href);
      url.searchParams.delete('status');
      url.searchParams.delete('sort');
      window.history.replaceState({}, '', url);
    }
    const requestedQuery = cleanText(params.get('q') || params.get('author'));
    state.query = normalizeSearchText(requestedQuery);
    const search = document.getElementById('publication-search-input');
    if (search) search.value = requestedQuery;
  }

  function matchesBaseFilters(paper) {
    return !state.query || paper.searchText.includes(state.query);
  }

  function matchesTopics(paper, topics = state.activeTopics) {
    return [...topics].every(id => paper.topics.some(topic => topic.id === id));
  }

  function renderTopicFilters() {
    const filters = document.getElementById('publication-topic-filters');
    if (!filters) return;
    const options = [{ id: '', label: 'All topics', color: '#64748b' }, ...TOPICS];
    if (!filters.children.length) {
      options.forEach(topic => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'filter-button';
        button.dataset.topic = topic.id;
        button.style.setProperty('--topic-color', topic.color);
        const swatch = document.createElement('span');
        swatch.className = 'filter-button__swatch';
        swatch.setAttribute('aria-hidden', 'true');
        const label = document.createElement('strong');
        label.className = 'filter-button__label';
        label.textContent = topic.label;
        const count = document.createElement('span');
        count.className = 'filter-button__count';
        button.append(swatch, label, count);
        filters.appendChild(button);
      });
    }
    const base = state.papers.filter(matchesBaseFilters);
    filters.querySelectorAll('.filter-button').forEach(button => {
      const id = button.dataset.topic;
      const active = id ? state.activeTopics.has(id) : state.activeTopics.size === 0;
      button.classList.toggle('active-filter', active);
      button.setAttribute('aria-pressed', String(active));
      const selected = new Set([...state.activeTopics, id]);
      const count = id ? base.filter(paper => matchesTopics(paper, selected)).length : base.length;
      button.querySelector('.filter-button__count').textContent = String(count);
      button.title = id ? `${count} papers match this topic and all selected topics` : 'Clear topic selections';
    });
  }

  function updateFiltersInUrl() {
    const url = new URL(window.location.href);
    if (state.activeTopics.size) url.searchParams.set('topic', [...state.activeTopics].join(','));
    else url.searchParams.delete('topic');
    url.searchParams.delete('status');
    if (state.query) url.searchParams.set('q', state.query);
    else url.searchParams.delete('q');
    url.searchParams.delete('sort');
    url.searchParams.delete('author');
    window.history.replaceState({}, '', url);
  }

  function renderPublications() {
    const container = document.getElementById('paper-container');
    const title = document.getElementById('publication-results-title');
    const count = document.getElementById('publication-count');
    if (!container || !state.papers.length) return;

    const visible = state.papers.filter(paper => matchesBaseFilters(paper) && matchesTopics(paper));

    visible.sort((a, b) => {
      const yearA = Number(a.year) || 0;
      const yearB = Number(b.year) || 0;
      if (yearA !== yearB) {
        return yearB - yearA;
      }

      const aHasScholarRank = Number.isInteger(a.scholarRank);
      const bHasScholarRank = Number.isInteger(b.scholarRank);
      if (aHasScholarRank && bHasScholarRank && a.scholarRank !== b.scholarRank) {
        return a.scholarRank - b.scholarRank;
      }
      if (aHasScholarRank !== bHasScholarRank) return aHasScholarRank ? -1 : 1;

      return b.dateKey - a.dateKey || a.originalIndex - b.originalIndex;
    });

    const activeTopics = TOPICS.filter(topic => state.activeTopics.has(topic.id));
    visible.forEach(paper => {
      highlightAuthorQuery(paper.authorsElement, paper.authors, state.query);
      paper.element.querySelectorAll('.paper-tag').forEach(tag => {
        tag.setAttribute('aria-pressed', String(state.activeTopics.has(tag.dataset.topic)));
      });
    });
    if (title) {
      title.textContent = activeTopics.length > 1 ? 'Topic intersection'
        : activeTopics.length === 1 ? activeTopics[0].label
        : state.query ? 'Search results' : 'All papers';
    }
    const selection = document.getElementById('publication-active-topics');
    if (selection) {
      selection.hidden = activeTopics.length < 2;
      selection.textContent = activeTopics.map(topic => topic.shortLabel || topic.label).join(' ∩ ');
    }
    if (count) {
      count.textContent = visible.length === state.papers.length
        ? `${visible.length} papers`
        : `${visible.length} of ${state.papers.length} papers`;
    }

    if (!visible.length) {
      container.innerHTML = '<div class="publication-empty"><i class="fas fa-search" aria-hidden="true"></i><strong>No publications found</strong><span>Try removing a topic or changing the search.</span></div>';
      return;
    }

    const fragment = document.createDocumentFragment();
    const papersByYear = new Map();
    visible.forEach(paper => {
      if (!papersByYear.has(paper.year)) papersByYear.set(paper.year, []);
      papersByYear.get(paper.year).push(paper);
    });

    papersByYear.forEach((papers, year) => {
      const section = document.createElement('section');
      section.className = 'publication-year-group';
      section.setAttribute('aria-labelledby', `publication-year-${year}`);

      const heading = document.createElement('header');
      heading.className = 'publication-year-heading';
      const yearElement = document.createElement('h3');
      yearElement.id = `publication-year-${year}`;
      yearElement.textContent = year;
      const line = document.createElement('span');
      line.className = 'publication-year-heading__line';
      line.setAttribute('aria-hidden', 'true');
      const yearCount = document.createElement('span');
      yearCount.className = 'publication-year-heading__count';
      yearCount.textContent = `${papers.length} ${papers.length === 1 ? 'paper' : 'papers'}`;
      heading.append(yearElement, line, yearCount);

      const list = document.createElement('div');
      list.className = 'publication-year-list';
      papers.forEach(paper => list.appendChild(paper.element));
      section.append(heading, list);
      fragment.appendChild(section);
    });

    container.replaceChildren(fragment);
  }

  function cleanText(value) {
    return (value || '').replace(/\s+/g, ' ').trim();
  }

  function normalizeTitleKey(value) {
    return cleanText(value)
      .toLowerCase()
      .replace(/&/g, ' and ')
      .replace(/[^a-z0-9]+/g, ' ')
      .replace(/([a-z])(\d)/g, '$1 $2')
      .replace(/(\d)([a-z])/g, '$1 $2')
      .replace(/\btowards\b/g, 'toward')
      .replace(/\btinyml\b/g, 'tiny machine learning')
      .replace(/^special session\s+/, '')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function normalizeSearchText(value) {
    return cleanText(value).toLowerCase();
  }
}());
