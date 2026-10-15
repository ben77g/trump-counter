"""Builds og.png: the link-preview thumbnail (white letter T on red, 1200x630). Draws the T with rectangles, no font needed.
Run: nix-shell -p "python3.withPackages (p: [p.pillow])" --run "python3 make_thumb.py" """
from PIL import Image, ImageDraw
W, H = 1200, 630
im = Image.new("RGB", (W, H), "#b22222")
d = ImageDraw.Draw(im)
bar_w, bar_h, stem_w, stem_h = 560, 130, 170, 400
x0, y0 = (W - bar_w) // 2, (H - (bar_h + stem_h)) // 2
d.rectangle([x0, y0, x0 + bar_w, y0 + bar_h], fill="white")
d.rectangle([(W - stem_w) // 2, y0 + bar_h, (W + stem_w) // 2, y0 + bar_h + stem_h], fill="white")
im.save("og.png", optimize=True)
print(im.size)
