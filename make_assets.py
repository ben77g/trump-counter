"""Builds the woodgrain+burned-flag background (bg.jpg) and the leaderboard board (board.jpg).
Run (NixOS):  nix-shell -p "python3.withPackages (p: [p.pillow p.numpy])" --run "python3 make_assets.py"
The figure itself is built by make_jesus_torso.py (needs rembg). Head cut-outs were removed 2026-10-15."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
rng = np.random.default_rng(0x168)
import os

# ---------- 2. wood + burned flag ----------  (fade = soft bottom edge so the neck does not end in a hard line)
W, H = 1920, 1080
def noise(w, h, sx, sy):               # smooth random field, stretched by (sx, sy) cells
    small = rng.random((max(2, h // sy), max(2, w // sx))).astype(np.float32)
    return np.array(Image.fromarray(small).resize((w, h), Image.BICUBIC))
# grain: long streaks along x
g = noise(W, H, 400, 6) * 0.5 + noise(W, H, 150, 3) * 0.3 + noise(W, H, 60, 2) * 0.2
yy = np.arange(H)[:, None].astype(np.float32)
rings = np.sin((yy * 0.09) + g * 34) * 0.5 + 0.5
fine = noise(W, H, 30, 1)
tone = 0.55 * rings + 0.25 * g + 0.20 * fine
# planks: 8 horizontal boards with their own tint and dark seams
plank_h = H // 8
tint = np.zeros((H, W, 3), np.float32)
base = np.array([196, 142, 84], np.float32)
for i in range(9):
    y0, y1 = i * plank_h, min(H, (i + 1) * plank_h)
    jitter = 1 + rng.uniform(-0.12, 0.12)
    shift = rng.uniform(-18, 18, 3)
    tint[y0:y1] = base * jitter + shift
    # per-plank offset of the grain pattern is already random through the noise fields
wood = tint * (0.55 + 0.75 * tone[:, :, None])
for i in range(1, 8):                   # seams
    y = i * plank_h
    wood[y - 1:y + 2] *= 0.35
# knots
for _ in range(5):
    cx, cy, r = rng.integers(100, W - 100), rng.integers(60, H - 60), rng.integers(18, 40)
    Y, X = np.ogrid[:H, :W]
    d = np.sqrt(((X - cx) / 1.8) ** 2 + (Y - cy) ** 2)
    ring = (np.sin(d * 0.55) * 0.5 + 0.5) * np.exp(-d / (r * 2.2))
    wood *= (1 - 0.45 * np.exp(-(d / r) ** 2))[:, :, None]
    wood *= (1 - 0.25 * ring)[:, :, None]

# flag mask: 1 = burned dark, 0 = left as bare wood
FW, FH = 1300, 683                      # 1.9:1 flag
flag = Image.new("L", (FW, FH), 0)
d = ImageDraw.Draw(flag)
sh = FH / 13
for i in range(13):
    if i % 2 == 0:                       # red stripes are burned
        d.rectangle([0, int(i * sh), FW, int((i + 1) * sh)], fill=255)
cw, ch = int(FW * 0.4), int(sh * 7)
d.rectangle([0, 0, cw, ch], fill=255)    # canton burned...
import math
def star(cx, cy, R, fill):
    pts = []
    for k in range(10):
        r = R if k % 2 == 0 else R * 0.382
        ang = -math.pi / 2 + k * math.pi / 5
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=fill)
for row in range(9):                     # ...with 50 stars left unburned
    n = 6 if row % 2 == 0 else 5
    for col in range(n):
        x = cw / 12 * (1 + col * 2 + (0 if row % 2 == 0 else 1))
        y = ch / 10 * (1 + row)
        star(x, y, ch / 10 * 0.62, 0)
# wave and a slight tilt
fa = np.array(flag, np.float32) / 255
xs = np.arange(FW)[None, :]
wave = (np.sin(xs / FW * 2 * math.pi * 1.5) * 16).astype(int)
wavy = np.zeros_like(fa)
for x in range(FW):
    wavy[:, x] = np.roll(fa[:, x], wave[0, x])
img = Image.fromarray((wavy * 255).astype(np.uint8)).rotate(-4, expand=True, resample=Image.BICUBIC)
canvas = Image.new("L", (W, H), 0)
canvas.paste(img, ((W - img.width) // 2, (H - img.height) // 2))
burn = np.array(canvas.filter(ImageFilter.GaussianBlur(1.6)), np.float32) / 255
# uneven burn: patchy intensity and flaked edges
patch = noise(W, H, 40, 40) * 0.6 + noise(W, H, 8, 8) * 0.4
burn = np.clip(burn * (0.55 + 0.9 * patch), 0, 1)
burn = np.where(burn > 0.18, burn, 0)
halo = np.array(Image.fromarray((burn * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14)), np.float32) / 255
char = np.array([28, 14, 6], np.float32)
out = wood * (1 - 0.35 * halo[:, :, None])           # scorched glow around the burn
out = out * (1 - burn[:, :, None] * 0.93) + char * burn[:, :, None] * 0.93
# soft vignette
Y, X = np.ogrid[:H, :W]
vig = 1 - 0.28 * (((X - W / 2) / (W / 2)) ** 2 + ((Y - H / 2) / (H / 2)) ** 2) / 2
out *= vig[:, :, None]
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save("bg.jpg", quality=82, optimize=True)
print("bg done")

# ---------- 3. leaderboard board: a single piece of wood, grain running up and down ----------
def board_wood(w, h):                       # w x h, grain along the long (vertical) side
    gw, gh = h, w                            # build with horizontal grain, then rotate
    g = noise(gw, gh, 300, 5) * 0.5 + noise(gw, gh, 120, 3) * 0.3 + noise(gw, gh, 50, 2) * 0.2
    yy = np.arange(gh)[:, None].astype(np.float32)
    rings = np.sin(yy * 0.11 + g * 30) * 0.5 + 0.5
    tone = 0.55 * rings + 0.25 * g + 0.20 * noise(gw, gh, 25, 1)
    col = np.array([205, 154, 96], np.float32)
    img = col * (0.55 + 0.75 * tone[:, :, None])
    Y, X = np.ogrid[:gh, :gw]
    for _ in range(2):                       # a couple of knots
        cx, cy, r = rng.integers(60, gw - 60), rng.integers(40, gh - 40), rng.integers(14, 26)
        dd = np.sqrt(((X - cx) / 1.8) ** 2 + (Y - cy) ** 2)
        img *= (1 - 0.45 * np.exp(-(dd / r) ** 2))[:, :, None]
        img *= (1 - 0.22 * (np.sin(dd * 0.6) * 0.5 + 0.5) * np.exp(-dd / (r * 2.2)))[:, :, None]
    # darker, worn edges
    edge = np.minimum(np.minimum(X, gw - 1 - X), np.minimum(Y, gh - 1 - Y)).astype(np.float32)
    img *= (0.72 + 0.28 * np.clip(edge / 28, 0, 1))[:, :, None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).rotate(90, expand=True)
board_wood(560, 1100).save("board.jpg", quality=84, optimize=True)
print("board done")
