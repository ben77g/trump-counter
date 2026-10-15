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

## Look
- Background bg.jpg (generated woodgrain with a flag burned in) and board.jpg (wooden leaderboard board), both made by
  make_assets.py. Leaderboard text is "burned in" with CSS (dark colour, scorch glow, SVG filter #burnrough, multiply).
- Heads: prof_head.png and trump_head.png are transparent cut-outs. prof_head.png was supplied by the owner (an uploaded
  head on a white background, processed by head_from_white_bg in make_assets.py: white touching the border becomes
  transparent, edge colours come from the nearest interior pixel, bottom fade cut). trump_head.png is cut with rembg
  (`u2net_human_seg`) from trump_mugshot.jpg.
- Do NOT re-run make_assets.py without moving prof_head.png aside; it rebuilds it from prof_upload.jpg.
- Rebuild: `nix-shell -p "python3.withPackages (p: [p.rembg p.pillow p.onnxruntime p.numpy p.scipy])" --run "python3 make_assets.py"`
  (first run downloads a 176 MB model to ~/.u2net).
- No heart behind the heads (removed 2026-10-15). Layout: main has padding-left 150px (290px under 1100px wide) and
  padding-top 12vh; the +1 button is pulled up with a negative margin in #add (0.2 of the block width).
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
