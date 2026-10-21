# Alumni and sponsor maintenance

## Alumni

The Team page retains the original member layout and complete alumni list.
Alumni Spotlights were removed at the lab's request on September 20, 2026.

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
