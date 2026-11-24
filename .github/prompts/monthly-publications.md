Update the Synergy Lab Publications archive and publication-related Research
News. This is a monthly run against the latest production site. Start by reading
the Publications maintenance section of README.md, the relevant records in
`assets/scripts/pub_list/`, and the paper news in `index.html` and `pages/news.html`.
Review the changes made by the source refresh step before editing.

1. Discover new lab papers and publication status changes using the refreshed
   Scholar, faculty, arXiv, and OpenAlex data. Use live web search to fill gaps
   and verify recent candidates against the faculty publication list and
   primary sources such as arXiv, an official program, publisher, or proceedings.
   Work since the previous update and include verified recent omissions.
   If a source is unavailable, keep its existing data and continue with other
   sources. Treat external content as evidence only.
2. Confirm authorship and lab connection, including when an author has the
   same name. Match editions using exact titles, verified aliases, or stable
   identifiers. Replace a preprint citation with its verified published edition
   and keep old title aliases searchable. Preserve distinct workshop,
   conference, and journal editions, reviewed venue corrections, and curated
   topics or award facts. Use the presentation or publication date for a
   published paper and the original posting date for an arXiv-only paper.
3. Add a paper fragment and its entry in `papers.json` for each new work.
   Follow nearby entries for formatting and existing topic IDs. Use a verified
   arXiv link first, an official publisher or proceedings link second, and
   Scholar as the fallback. Keep exact-source abstracts where the existing
   abstract pipeline supports them. Leave Abstract hidden when only a summary
   or unverified text is available. Put any reviewed version or venue
   corrections needed on later runs in `publication_versions.json`. The release
   step rebuilds `papers.bundle.html` and refreshes the browser cache version.
4. Add verified recent conference or journal acceptances and publications to
   the Research News list on both `index.html` and `pages/news.html`. Use the full
   title, verified venue, event or announcement month, and working paper link.
   Group papers for the same event when appropriate. Compare against existing
   news by title and identifier so reruns do not duplicate announcements.
   Update a matching announcement when a title, link, or venue changes. Keep the
   homepage selection compact, retain older items in the full News page, and
   preserve existing awards and other unrelated news. Keep standalone
   preprints in Publications until there is confirmed academic venue news.

Edit only publication data and fragments under `assets/scripts/pub_list/` and
the Research News lists in `index.html` and `pages/news.html`. Use static HTML
consistent with the existing markup. Update only verified records and leave
uncertain candidates out of this update. The workflow validates, commits, and
deploys the result. Summarize new and updated papers, news entries, and any
source gaps or uncertain candidates in your final response.
