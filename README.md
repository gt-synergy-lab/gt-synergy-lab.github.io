# Synergy Lab website

This repository contains the deployable static copy of the Synergy Lab website at Georgia Tech. GitHub Pages hosts both the lab site and a separate preview site.

- **Lab website:** <https://gt-synergy-lab.github.io/>, published from <https://github.com/gt-synergy-lab/gt-synergy-lab.github.io>.
- **Preview website:** <https://gt-synergy-lab.github.io/synergy_lab_website_test/>, published from <https://github.com/gt-synergy-lab/synergy_lab_website_test>.

The editable/source repository and this deployment repository have different roles:

- `synergy_website`: source of truth for website edits and generation.
- `gt-synergy-lab.github.io` and `synergy_lab_website_test`: browser-ready static files and deployment configuration.

Do not store passwords, API keys, SSH keys, or server credentials in this repository.

## Local preview

Run from the repository root:

```bash
python3 -m http.server 8000
```

Then open <http://127.0.0.1:8000/>. Do not open the HTML through `file://`; the Publications page loads local data with `fetch()` and requires HTTP.

## GitHub Pages deployment

1. Review the staged files and test the site locally.
2. Commit and push the `main` branch.
3. Open the repository on GitHub and go to **Settings → Pages**.
4. Under **Build and deployment**, choose **GitHub Actions** as the source.
5. Open the **Actions** tab and confirm that **Deploy static content to Pages** succeeds.
6. Open the Pages URL shown by the deployment. The lab website is:

   `https://gt-synergy-lab.github.io/`

The included workflow publishes the repository's site after every push to `main`. It can also be run manually from the Actions tab. Pages settings are configured separately for each repository; copying the workflow alone does not enable Pages.

The existing local checkout retains `origin` for the preview repository and uses `production` for the lab website repository:

```bash
git push origin main      # Publish to the preview site.
git push production main  # Publish the reviewed version to the lab site.
```

If starting from a fresh clone, inspect `git remote -v` before publishing: a clone of the lab website repository uses `origin` for production by default. Git pushes include committed files and history; untracked local drafts are not migrated.

## Production domain later

Keep the existing `synergy.ece.gatech.edu` site in place until the new GitHub-hosted website is reviewed and the domain migration is approved.

After the lab website has been reviewed and Georgia Tech approves the hosting change:

1. Add `synergy.ece.gatech.edu` under **Settings → Pages → Custom domain**.
2. Ask the Georgia Tech/ECE DNS administrator to point the site's CNAME to `gt-synergy-lab.github.io` (without a repository path).
3. Wait for DNS and HTTPS provisioning to complete.
4. Recheck every page before retiring the WordPress version.

## Runtime contents

- `index.html`: homepage.
- `pages/`: content pages.
- `assets/css/`, `assets/js/`, and `assets/img/`: site presentation and media.
- `assets/scripts/pub_list/`: Publications data loaded at runtime.
- `assets/vendor/`: only the third-party browser files used by the pages.
- `.nojekyll`: prevents Jekyll processing of static asset paths.

## Refresh publication metadata

```bash
python3 scripts/refresh_publications.py
```

This uses Python's standard library to refresh `scholar_order.json` from the
faculty Google Scholar profile and `faculty_publications.json` from the faculty
publication page. It also refreshes `paper_abstracts.json` from the arXiv API,
matching exact normalized titles and preserving the original text and versioned
source link. It supplements these with OpenAlex indexed abstracts matched by
title, year and author, with both the index and publisher DOI linked. Only
unambiguous matches are displayed; other abstract buttons are hidden. An arXiv
abstract may differ from the final published version. Existing fragment summaries
are not used. Manually verified publisher abstracts are retained in
`reviewed_publisher_abstracts.json` and reapplied on refresh. Reviewed links for
papers whose source title or online year differs are recorded in
`reviewed_abstract_links.json` with their stable identifiers; the source title
and identifier must still match on each refresh.
The script parses data literals without executing remote JavaScript.
Incomplete fetches fail before replacing the data. Newly discovered faculty
titles are reported for review; adding a paper still requires updating its HTML
fragment, `papers.json`, and `papers.bundle.html` together.

The archive includes both published papers and preprints, with no publication
status filter. Multiple topics are combined with AND. Topics and search can be
combined and shared through the URL. Ordering is fixed to newest first.

Confirmed conference/journal dates take priority over an earlier arXiv/Scholar
date for both year groups and ordering. Papers are sorted newest first by year
and available presentation or publication month. Preprints use the first arXiv
posting date where available; otherwise the local/Scholar year is used. Records
without a reliable month appear after dated papers in the same year, with the
original order breaking ties. Full titles, venue names, authors, and available
months come from faculty metadata; venue month defaults can be approximate.
Every refresh also records original arXiv submission dates (not revision dates).
Verified event dates in `publication_versions.json` override recurring venue
defaults; their start day is used to order conferences within the same month.

Each refresh records exact title variants, reviewed aliases, and available
arXiv/DOI identifiers. When a preprint matches a published work, the archive shows
the published citation once and keeps old titles searchable and supplemental
links accessible. Conference and journal editions remain separate. Unmatched
renames are reported for review; similar wording alone is not a reliable match.
The Paper link can still point to an accessible arXiv copy when a publisher URL
is unavailable.

`publication_versions.json` stores reviewed title/version relationships, source
links, and publisher-confirmed corrections. The refresh script reapplies these
on every run, including the IMS 2022 correction. Aliases are scoped to a venue so
a conference preprint cannot silently relabel a separate journal edition.
See [the November 1 version audit](docs/publication-version-audit-2026-11-01.md)
for confirmed merges and the remaining preprints.

Award labels remain locally reviewed: the lab's MLSys no-Oral correction must
not be overwritten by a crawl.
Venue names are bold in the citation, with a colored short venue/year badge
beside the paper title; preprints have neutral badges.

Run the publication reconciliation checks with:

```bash
node --test tests/publication-metadata.test.js
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'
```
