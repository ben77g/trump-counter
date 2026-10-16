# Trump Counter

Static one-page site (GitHub Pages, repo ben77g/trump-counter, https://trumpcounter.mooo.com/).
Two cut-out heads, a shared live counter with +1, a left board with the top 5 lectures, and a small notice. No login.

## How it works
- Lectures: every Tuesday and Thursday, Tue 2026-09-08 to Tue 2026-12-01 = 25 lectures (the first one, 2026-09-03, is
  dropped on the owner's request), so Thu 2026-10-15 is lecture 12. Add cancelled dates to NO_CLASS in index.html.
- ONE shared counter per lecture, stored on abacus.jasoncameron.dev (no account, no email), namespace
  `trumpcounter-mooo-site`, key `C-<date>`. +1 calls GET /hit/<ns>/<key> (atomic). Every page polls today's key
  every 3 s (POLL_MS), so viewers see the same number within about 3 seconds. A new date is a new key = daily reset.
- Leaderboard = top 5 lecture dates by count. Past lectures are fetched once per browser, 400 ms apart, and cached in
  localStorage `trumpCounterPast`. Reason: the API allows only 30 requests per 10 s per visitor and has no "list keys" call.
- On a day without class (Toronto time) the +1 button is disabled and the page shows the next lecture date.
- Files: index.html (everything), make_assets.py, make_thumb.py, images (see below).

## Non-obvious
- Tried and rejected: counterapi.dev (v1 gone, v2 needs account), jsonblob.com (bot check), kvdb.io (writes refused
  until email verified). Switched to abacus 2026-10-15.
- No security: the bucket id is in the page source, so anyone can write to it. There is no per-person click limit and
  no way to reset a count without the API admin key.
- Polling (not websockets) because the API has no push channel; 3 s is the live-update delay.

## Custom domain
- trumpcounter.mooo.com (FreeDNS/afraid.org). CNAME file in repo + Pages custom domain. DNS: CNAME record
  trumpcounter -> ben77g.github.io. HTTPS is enforced by GitHub once DNS resolves.
- The old ben77g.github.io/trump-counter/ address redirects to the custom domain.

## Input lock (soft)
- Only the owner can press +1, unless mode.json says {"open": true}. The owner's browser holds a key in localStorage
  (`tcOwner`); index.html contains only its SHA-256 (OWNER_HASH). To enrol a browser, open the site once with `#owner=<key>`
  appended; the key itself is kept outside the repo (~/agent/workspace/.counter-owner-key, mode 600). Never commit it.
- `./set_mode.sh exempt [date]` writes mode.json {"open_for": "<date>"}: the public +1 is open for ONE lecture day only
  (default today if it is a lecture day, else the next one) and closes by itself afterwards, because the page only opens
  when open_for equals today's date (Toronto time). It is an exemption notice, not a toggle. `./set_mode.sh clear` cancels it.
  The page re-reads mode.json every 30 s (cache-busted), so a change shows about 1 to 2 minutes after the push.
  If mode.json cannot be read the page stays closed.
- Limit: this is a client-side lock. Anyone who reads the page source can still call the counter API directly, because the
  namespace is public. It stops casual visitors, not someone determined. A real lock would need a server or secret keys.
- The assistant's own notes (outside the repo) hold the owner's trigger phrases for open/close.

## Look
- Background bg.jpg (generated woodgrain with a flag burned in) and board.jpg (wooden leaderboard board), both made by
  make_assets.py. Leaderboard text is "burned in" with CSS (dark colour, scorch glow, SVG filter #burnrough, multiply).
- Figure: trump_jesus_torso.png is a head-to-waist cut-out of an AI image (trump_jesus_src.jpg, public domain on
  Wikimedia Commons), built by make_jesus_torso.py with rembg (`u2net_human_seg`). It is centred in the box
  (.trump left:50%, translateX(-50%), width 46%). The page shows no photo of any real person other than that image.
  Earlier mugshot, portrait and head cut-outs were removed 2026-10-15.
- Rebuild the background and board: `nix-shell -p "python3.withPackages (p: [p.rembg p.pillow p.onnxruntime p.numpy p.scipy])" --run "python3 make_assets.py"`
  (first run downloads a 176 MB model to ~/.u2net).
- No heart behind the heads (removed 2026-10-15). Layout: main has padding-left 150px (290px under 1100px wide) and
  padding-top 12vh; there is no +1 button: the Trump picture (#add, an img) is the button for the owner (never greyed out; it does nothing for visitors when closed). A visible +1 button (#addbtn) appears under the picture only while mode.json exempts today, for visitors (2026-10-15).
- Preview screenshot: chromium --headless=new --no-sandbox --screenshot=out.png --window-size=1280,800 file://$PWD/index.html

## Link preview and discovery
- Link-preview thumbnail is og.png (white T on red, made by make_thumb.py), set with og:image / twitter:image tags
  (`og.png?v=2`; bump the number to force chat apps to refresh their cache).
- The site is deliberately kept out of search engines: noindex/nofollow/noarchive meta tags in index.html, a robots.txt
  that disallows everything, no names or institution in the page, the repo or the README. Do not add them back.
- Footer notice inside the white box: "Unofficial student-made counter. Not affiliated with any university or with the
  professor. Counts are entered by visitors and are unverified."

## History
- 2026-10-15: git history was rewritten twice (author email -> ben77g noreply address; then names scrubbed from files,
  filenames and commit messages). Anyone with an old clone must re-clone.
- 2026-10-15: the torso cut-out is the only figure; it is centred (.trump left:50%, width 46%).
- 2026-10-15: the photo of the professor was removed from the site on the owner's request (files prof*.jpg/png deleted from the repo).
- 2026-10-15: page title, heading and og:title now read "360 Trump Counter" (owner's request).
- Leaderboard board is 393px wide (1.5x the original 262px), fonts scaled 1.5x (2026-10-15).
