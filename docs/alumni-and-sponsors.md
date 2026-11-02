# Alumni and sponsor maintenance

## Alumni

The Team page retains the original member layout and complete alumni list.
Alumni Spotlights were removed at the lab's request on September 20, 2026.

On October 29, 2026, the lab chose to show **in-group year ranges for postdocs
only**. Other alumni retain their existing graduation years; do not infer missing
start years from degree enrollment or publication dates. Postdoc ranges and first
jobs were pulled from the lab's update in commit `906772e`:

- Hesam Shabani: 2024–2025, IMEC.
- Joongun Park: 2023–2025, Apple.
- Taekyung Heo: 2022–2023, NVIDIA.

Difei Cao was removed from the current Ph.D. roster at the lab's request. The
Past Visitors group is the final subgroup of Alumni, after B.S., and reproduces
the seven historical visitors and their
visit periods from <https://synergy.ece.gatech.edu/members/> (checked October 29,
2026). The older site's current-postdoc list must not override the newer alumni
updates in this repository.

## Publication update — October 29, 2026

The lab explicitly confirmed that its MLSys 2026 papers, MLCommons Chakra and
PRIVATAR, have **no Oral designation**. Remove the inherited Oral badges and
the “2 Orals” news claim. This correction overrides the `note: "Oral"` entries
in the faculty publication data fetched earlier that day; do not reintroduce
those labels during future synchronization.

The publication archive was checked against the faculty publication list at
<https://tushar-krishna.github.io/publications.html> and Google Scholar profile
`P__ztgcAAAAJ`. Eight missing records were added: CoCoSys, ACE, DynamoServe, LLMET,
ORACLE, SCALE-Sim EVA, Dyserve, and Polestar. Current arXiv metadata supplies the
updated titles and authors for ORACLE (formerly TRACE-Router, `2607.22465`) and
Dyserve (formerly A Workflow-Aware Serving Layer, `2607.02942`).

STAGE (`2511.10480`) and MIST (`2504.09775`) replace their earlier preprint entries;
they are not additional papers. The faculty list confirms ISCA 2026 for STAGE,
SC 2026 for MIST, NeurIPS 2026 for Polestar, IEEE CAL 2026 for SCALE-Sim TPU, and
ACM TECS 2026 for Cross-Layer Design of Vector-Symbolic Computing. Confirmed venue
years are displayed in citations. Stable fragment
filenames may therefore retain an earlier year. New or replaced records label
their editorial descriptions as “Summary”; full abstracts are available via
their Paper links. Keep `papers.json`, `papers.bundle.html`, and the individual
HTML fragments synchronized.

New entries use explicit `data-topic-ids` to avoid confusing agent model routing
with NoC routing, or symbolic tensor graphs with neuro-symbolic AI. Renamed
entries retain old names in `data-search-aliases`. Homepage news keeps the latest
eight items; older items remain in `pages/news.html`. The October news item is
the date this site reports the confirmed acceptances, not a claimed decision date.

### October 30, 2026 follow-up

The lab requested chronological Google Scholar ordering, including its year
groups, instead of reordering by conference month or acceptance status. The year
grouping policy was subsequently corrected on November 1 (below). The
archive supports intersecting topic selections. At the lab's request, the
publication-status controls were removed; published papers and preprints are
both included, and old status-filter URLs no longer hide preprints.

The refreshed faculty list contains 176 records from 2015 onward; all 27 of its
2026 papers already exist in the archive, including MIST (SC, November) and
Polestar (NeurIPS, December). No duplicate entries were added. The Scholar crawl
contains 337 rows, including undated duplicates and non-paper artifacts; these
are an ordering reference, not 337 distinct papers to import.

Four older faculty entries remain unmatched and require editorial review before
adding: SmartPAF (MLSys 2024), Application Benchmarking (IRDS chapter, 2020), the
SysML 2018 MAERI workshop variant, and On-Chip Networks, Second Edition (2017).
`scripts/refresh_publications.py` reports these rather than conflating them with
similarly titled records. The live archive still contains 248 deduplicated items.

### November 1, 2026: publication years and preprint replacement

Confirmed venue years now determine year groups as well as citations and badges.
MIST (SC 2026) and Demystifying AI Platform Design (ICCAD 2026) therefore appear
under 2026 instead of their earlier preprint years. Scholar ordering is retained
within each year; unaccepted preprints still use their Scholar dates.

Every run of `scripts/refresh_publications.py` preserves known title aliases and
available arXiv/DOI identifiers. The archive uses them to replace a matching
preprint with the published citation, retaining searchable old titles and
supplemental links. Same-title conference and journal editions remain distinct;
ambiguous identifier matches or unrecognized renames require review.

Deduplication checks also identified two labels for the same 2024 Neuro-Symbolic
Architecture paper. Its local ESWEEK label was corrected to CODES+ISSS, as listed
in the [IEEE proceedings](https://ieeexplore.ieee.org/document/10740726/), so it
continues to appear once. Fragment filenames may retain earlier years; the
displayed publication year comes from the resolved citation metadata.

The subsequent full-archive audit reconciled 19 redundant preprint records with
18 published works and collapsed one duplicate SCALE-Sim preprint. The archive
now displays 228 records, including 29 retained preprints. Reviewed mappings and
source corrections are stored in `publication_versions.json` and survive refreshes.
See [the full audit](publication-version-audit-2026-11-01.md) for the evidence,
workshop/poster/keynote labels, and cases intentionally kept separate.

## Sponsor roster

Keep the `.sponsor-roster` lists in `index.html` and `pages/sponsors.html` in sync.
Agencies/programs and industry are separate groups. DARPA and SRC use typeset
names. Company logos use local image assets; do not substitute ordinary text.

Google, Meta, and TSMC logos were refreshed on October 29, 2026 using these
first-party sources, preserving the original artwork and colors:

- `google.webp`: [Google Brand Resource Center](https://about.google/brand-resource-center/guidance/), the 2x Google wordmark used in its header.
- `meta.svg`: [Meta Brand Resource Center](https://www.meta.com/brand/resources/meta/company-brand/), `Meta_Company-Lockup.zip` → `1 Positive Primary/RGB/Meta_lockup_positive primary_RGB.svg`.
- `tsmc.png`: [TSMC's website](https://www.tsmc.com/english), the header logo at `/themes/custom/bootstrap_sass/images/logo.png`.

Keep the aspect ratios and brand colors intact. Meta's SVG contains generous
clear space, so its image box is larger to align the visible mark with its peers.

The lab explicitly confirmed on September 20, 2026 that it does not receive
IARPA or DOE funding. Neither organization belongs in this website's sponsor
roster. Faculty-wide funding statements must not override the lab's correction.
The agency/program group currently lists NSF, DARPA, and SRC (JUMP 2.0).

## Footer fix

The inherited `.footer::before` covered the entire footer and intercepted clicks.
`layout.css` removes this pseudo-element for `.synergy-footer` and restores automatic
footer height. Shared navigation lives in `assets/js/synergy-site.js`.
Contact opens the local contact page, which includes the faculty email.
