# Keke Long Lab — 2027 redesign

This version is developed on `redesign-2027` in the existing repository.
The public `main` branch remains at `42a6bff951278df4bdf6b1d256c9531dd5fb2fa0` when this draft is created.
Do not merge or replace the public website before January 1, 2027 (America/New_York).

## Editorial decisions

- Homepage order: original Safety & Mobility concept ring, three research directions in parallel, News.
- Header: Rutgers logo, Keke Long Lab, Rutgers University. No persistent portrait sidebar.
- Preserve the user's three directions and curated selection. No Publications page.
- Papers, datasets, and platforms belong to their research directions and have stable project pages.
- About holds the portrait, background, teaching experience, service, and Scholar link.
- Join Us preserves the original ten announcement image slices. Do not transcribe the application email, subject, or announcement into HTML, alt text, JSON, or structured metadata.
- Do not invent students, courses, an office address, a university email address, or a separate lab acronym.
- The existing webpage material is the source for all project titles, venues, links, and figures. Project summaries are concise editorial descriptions of that material, without new performance claims.

## Editing and building

Run `python site/build.py` with Python 3.12 or newer to regenerate the preview pages. No package installation is needed.
Edit `site/content.json` for projects, short descriptions, optional Chinese name, and future members/courses.
Edit `site/build.py` for shared page templates and the homepage News item; edit `style.css` for design.
Root HTML files are the GitHub Pages output. `dist/` contains the identical website for the owner-only Sites preview. Both are tracked so the source revision fully identifies the preview.

Preview pages carry `noindex` and `nofollow`. This does not make a public GitHub branch secret; the live preview is separately owner-private. The existing public website is unchanged.

## Public launch

On or after the launch date, run `python site/build.py --publish`. The command refuses to build public mode before January 1, 2027 in America/New_York.
Public mode switches About to the Rutgers Assistant Professor appointment, updates the copyright year, and enables indexing and the sitemap.
Before merging, inspect the current default branch and the latest redesign branch, retain all subsequent edits, and validate local links and generated files.
Commit the regenerated launch output to the redesign branch, then merge the redesign into `main` and verify the GitHub Pages result at `https://keke-long.github.io/`.
Do not enable auto-merge early. Do not use a browser-date redirect: GitHub Pages must serve the actual launch output.
Keep the prelaunch main revision available in Git history for rollback.

Chinese name is intentionally empty until the user provides its exact spelling. Once supplied, set `chineseName` in `site/content.json`; the visible About heading, titles, and Person metadata use it automatically.
New university contact details and courses can be added when known; their absence should not create empty public sections or invented content.

## Future sections

`people` is an empty list. Add records with `name`, `role`, optional local `image`, and optional `url` to enable People. The faculty entry links to the stable `/about/` page.
`courses` is an empty list. Add records with `title`, `term`, `description`, and `url` to enable Teaching.
When members exist, People replaces About in the primary navigation. The footer retains the personal About link.
The older homepage anchors and research direction URLs remain usable.

## Asset provenance

Research images, portrait, and recruitment slices come unchanged from the original repository.
`assets/brand/rutgers.svg` is the university artwork retrieved from `https://www.rutgers.edu/` on September 8, 2026.
`assets/brand/rutgers-r.svg` reuses the unchanged Rutgers R paths from that artwork, without the adjacent university wordmark. The header displays the R at 54 px wide (about 48 px tall) with clear space.
Scarlet is `#cc0033`, matching the official university SVG. Reference: `https://communications.rutgers.edu/brand-policies/visual-identity`.

## Validation

Static checks cover every generated HTML route, local image/style/script references, internal links and fragments, metadata, all eleven original projects and their links, and byte-for-byte preservation of the ten announcement slices. JavaScript is syntax-checked. Browser visual testing was not requested and was not run.
