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
