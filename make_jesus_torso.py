"""Builds trump_jesus_torso.png from trump_jesus_src.jpg (an AI image, public domain on Wikimedia Commons, posted by the subject
on 2026-04-12). rembg removes the background, then the figure is cut at the waist; the right edge is cut before the second
person in the picture. The boxes (x0, x1, y0, y1) come from the silhouette of the rembg output, not from eyeballing.
Run: nix-shell -p "python3.withPackages (p: [p.rembg p.pillow p.onnxruntime p.numpy])" --run "python3 make_jesus_torso.py" """
import numpy as np
from PIL import Image
from rembg import remove, new_session
im = Image.open("trump_jesus_src.jpg").convert("RGB")
a = np.array(remove(im, session=new_session("u2net_human_seg")))
x0, x1, y0, y1 = 150, 690, 280, 800
r = a[y0:y1, x0:x1].copy()
al = r[:, :, 3].astype(float)
H, W = al.shape
fb, fr = 50, 18                                   # soft fade at the waist and at the cut right edge
al[H - fb:H] *= np.linspace(1, 0, fb)[:, None]
al[:, W - fr:W] *= np.linspace(1, 0, fr)[None, :]
r[:, :, 3] = al.astype(np.uint8)
out = Image.fromarray(r)
out = out.crop(out.getbbox())
out.save("trump_jesus_torso.png", optimize=True)
print(out.size)
