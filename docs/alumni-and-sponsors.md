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
years take precedence over a preprint's older Scholar year. Stable fragment
filenames may therefore retain an earlier year. New or replaced records label
their editorial descriptions as “Summary”; full abstracts are available via
their Paper links. Keep `papers.json`, `papers.bundle.html`, and the individual
HTML fragments synchronized.

New entries use explicit `data-topic-ids` to avoid confusing agent model routing
with NoC routing, or symbolic tensor graphs with neuro-symbolic AI. Renamed
entries retain old names in `data-search-aliases`. Homepage news keeps the latest
eight items; older items remain in `pages/news.html`. The October news item is
the date this site reports the confirmed acceptances, not a claimed decision date.

## Sponsor roster

Keep the `.sponsor-roster` lists in `index.html` and `pages/sponsors.html` in sync.
Agencies/programs and industry are separate groups. Existing local logo files are
retained; newly added organizations use typeset names, not invented logos.

The lab explicitly confirmed on September 20, 2026 that it does not receive
IARPA or DOE funding. Neither organization belongs in this website's sponsor
roster. Faculty-wide funding statements must not override the lab's correction.
The agency/program group currently lists NSF, DARPA, and SRC (JUMP 2.0).

## Footer fix

The inherited `.footer::before` covered the entire footer and intercepted clicks.
`layout.css` removes this pseudo-element for `.synergy-footer` and restores automatic
footer height. Shared navigation lives in `assets/js/synergy-site.js`.
Contact opens the local contact page, which includes the faculty email.
