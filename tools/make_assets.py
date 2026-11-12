"""python3 make_assets.py logo <logo.png> | texture | icons name1 name2 ..."""
import sys, os, random
from PIL import Image, ImageDraw, ImageFont
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
os.makedirs(os.path.join(A, 'icons'), exist_ok=True)
COLORS = {'teal': '#1B7A8A', 'white': '#FFFFFF', 'amber': '#C98A1B', 'blue': '#3AA6D0'}
def logo(src):
    im = Image.open(src).convert('RGBA'); im.save(os.path.join(A, 'logo_light.png'))
    px = im.load(); w, h = im.size; dark = im.copy(); dp = dark.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a > 0 and abs(r - g) < 12 and abs(g - b) < 12 and r < 140: dp[x, y] = (255, 255, 255, a)
    dark.save(os.path.join(A, 'logo_dark.png'))
    cols = [x for x in range(w) if any(px[x, y][3] > 0 for y in range(0, h, 4))]
    gap = next((x for i, x in enumerate(cols[1:], 1) if x - cols[i - 1] > 20), None)
    end = cols[cols.index(gap) - 1] if gap else min(w - 1, h)
    im.crop((0, 0, end + 2, h)).save(os.path.join(A, 'shield.png'))
def texture():
    W, H = 1920, 1080; img = Image.new('RGB', (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H; d.line([(0, y), (W, y)], fill=(int(11 + 6 * t), int(30 + 14 * t), int(40 + 18 * t)))
    try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 22)
    except Exception: f = ImageFont.load_default()
    random.seed(7); ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for row in range(0, H, 30):
        od.text((-10, row), ''.join(random.choice('01') for _ in range(140)), font=f, fill=(58, 166, 208, 10 + int(16 * row / H)))
    mask = Image.new('L', (W, H)); md = ImageDraw.Draw(mask)
    for x in range(W): md.line([(x, 0), (x, H)], fill=int(255 * max(0, (x - W * 0.35) / (W * 0.65)) ** 1.2))
    img.paste(ov, (0, 0), Image.composite(ov.split()[3], Image.new('L', (W, H), 0), mask))
    img.save(os.path.join(A, 'bg_dark.png'))
def icons(names):
    from playwright.sync_api import sync_playwright
    src = os.path.join(A, 'lucide', 'icons')
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 300, 'height': 300})
        for n in names:
            svg = open(os.path.join(src, n + '.svg')).read()
            for cname, hexc in COLORS.items():
                s = svg.replace('currentColor', hexc).replace('width="24"', 'width="256"').replace('height="24"', 'height="256"').replace('stroke-width="2"', 'stroke-width="1.6"')
                pg.set_content(f'<html><body style="margin:0;background:transparent"><div id=i style="width:256px;height:256px">{s}</div></body></html>')
                pg.locator('#i').screenshot(path=os.path.join(A, 'icons', f'{n}_{cname}.png'), omit_background=True)
        b.close()
if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'logo': logo(sys.argv[2])
    elif c == 'texture': texture()
    elif c == 'icons': icons(sys.argv[2:])
