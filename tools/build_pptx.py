"""DevLeague deck builder v2: python3 build_pptx.py slides.md out.pptx [--script script.md] [--course "NETWORK+ N10-009" (default: $DECK_LABEL)] [--session 01] [--instructor "Peter Dunn"]"""
import re, os, argparse
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
C = lambda h: RGBColor.from_string(h.lstrip('#'))
CHAR, TEAL, BLUE, BLUE_D = C('#3A3B3D'), C('#1B7A8A'), C('#3AA6D0'), C('#2C5F7C')
AMBER, WHITE, MUTED = C('#C98A1B'), C('#FFFFFF'), C('#6B7A82')
TEAL_T, AMBER_T, BORDER, PAPER = C('#E6F3F5'), C('#FBF1DE'), C('#DCE4E8'), C('#F6F9FA')
ICE, DIM = C('#A9C4CF'), C('#1E4A5C')
SANS, MONO = 'Aptos', 'Consolas'
def rect(s, x, y, w, h, fill=None, line=None, shape=MSO_SHAPE.RECTANGLE, lw=1.0):
    sh = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None: sh.fill.background()
    else: sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if line is None: sh.line.fill.background()
    else: sh.line.color.rgb = line; sh.line.width = Pt(lw)
    sh.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE: sh.adjustments[0] = 0.08
    return sh
def grad_rule(s, x, y, w, h=0.05):
    sh = rect(s, x, y, w, h); sh.fill.gradient(); sh.fill.gradient_angle = 0
    st = sh.fill.gradient_stops; st[0].color.rgb = TEAL; st[1].color.rgb = BLUE
def txt(s, x, y, w, h, paras, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0.02)
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.space_after = Pt(para.get('after', 4)); p.line_spacing = para.get('ls', 1.05)
        for (t, size, color, bold, font) in para['runs']:
            r = p.add_run(); r.text = t; f = r.font; f.name = font; f.size = Pt(size); f.color.rgb = color; f.bold = bold
    return tb
R = lambda t, size, color=CHAR, bold=False, font=SANS: (t, size, color, bold, font)
def pic(s, path, x, y, w=None, h=None):
    if not os.path.exists(path): return None
    return s.shapes.add_picture(path, Inches(x), Inches(y), Inches(w) if w else None, Inches(h) if h else None)
def icon(s, name, color, x, y, size): return pic(s, os.path.join(A, 'icons', f'{name}_{color}.png'), x, y, size, size)
def icon_badge(s, name, x, y, d, tint, color):
    rect(s, x, y, d, d, fill=tint, shape=MSO_SHAPE.OVAL); icon(s, name, color, x + d * 0.22, y + d * 0.22, d * 0.56)
def kv(lines): return [(m.group(1), m.group(2)) for m in (re.match(r'- \*\*(.+?):\*\*\s*(.*)', l) for l in lines) if m]
def field(lines, key):
    for l in lines:
        if l.lower().startswith(key + ':'): return l.split(':', 1)[1].strip()
def light_frame(s, sid, a):
    s.background.fill.solid(); s.background.fill.fore_color.rgb = WHITE
    pic(s, os.path.join(A, 'shield.png'), 0.55, 0.38, h=0.42)
    txt(s, 1.02, 0.43, 6, 0.35, [{'runs': [R(f'{a.course}  //  SESSION {a.session}', 10, TEAL, True, MONO)]}])
    txt(s, 9.8, 0.43, 3.0, 0.35, [{'runs': [R(sid, 10, MUTED, False, MONO)]}], align=PP_ALIGN.RIGHT)
    rect(s, 0.55, 7.0, 12.23, 0.012, fill=BORDER); pic(s, os.path.join(A, 'logo_light.png'), 0.55, 7.1, h=0.22)
def headline(s, t):
    txt(s, 0.55, 0.95, 12.2, 0.8, [{'runs': [R(t, 30, CHAR, True)]}], anchor=MSO_ANCHOR.MIDDLE); grad_rule(s, 0.57, 1.78, 1.3)
def dark_frame(s): pic(s, os.path.join(A, 'bg_dark.png'), 0, 0, 13.333, 7.5)
def L_title(s, lines, a):
    dark_frame(s); pic(s, os.path.join(A, 'logo_dark.png'), 0.8, 0.75, h=0.75)
    h2 = next((l[3:] for l in lines if l.startswith('## ')), ''); h3 = next((l[4:] for l in lines if l.startswith('### ')), ''); b = dict(kv(lines))
    txt(s, 0.8, 2.55, 11, 0.4, [{'runs': [R(f'{a.course}  //  SESSION {a.session}', 14, BLUE, True, MONO)]}])
    txt(s, 0.8, 3.0, 11.5, 1.3, [{'runs': [R(h2, 50, WHITE, True)]}])
    txt(s, 0.8, 4.3, 10.5, 1.0, [{'runs': [R(h3, 20, ICE)]}])
    grad_rule(s, 0.82, 5.55, 1.6, 0.06)
    txt(s, 0.8, 5.75, 8, 0.4, [{'runs': [R('INSTRUCTOR  ', 11, BLUE, True, MONO), R(b.get('Instructor', a.instructor), 16, WHITE, True)]}])
def L_divider(s, lines, a):
    dark_frame(s); pic(s, os.path.join(A, 'logo_dark.png'), 0.8, 0.6, h=0.42)
    num = next((l[4:] for l in lines if l.startswith('### ')), ''); title = next((l[3:] for l in lines if l.startswith('## ')), ''); b = dict(kv(lines))
    txt(s, 0.65, 1.55, 6, 2.4, [{'runs': [R(num, 170, DIM, True)]}])
    txt(s, 0.8, 3.95, 11, 0.4, [{'runs': [R(f'BLOCK {num}  //  {a.course}', 13, BLUE, True, MONO)]}])
    txt(s, 0.8, 4.35, 11.8, 1.5, [{'runs': [R(title, 38, WHITE, True)]}])
    x = 0.8
    for obj in [o.strip() for o in b.get('Objectives', '').split(',') if o.strip()]:
        w = 0.25 + 0.12 * len(obj) + 0.5
        rect(s, x, 6.15, w, 0.42, line=TEAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE, lw=1.25)
        txt(s, x, 6.15, w, 0.42, [{'runs': [R(f'OBJ {obj}', 12, BLUE, True, MONO)]}], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        x += w + 0.18
def L_two(s, body, a):
    left, right = body.split(':right-column'); left = left.replace(':left-column', '')
    for x, part, tint, color, acc, tag, di in ((0.55, left, TEAL_T, 'teal', TEAL, '// THE CONCEPT', 'shield-check'), (6.78, right, AMBER_T, 'amber', AMBER, '// THE EXAM TRAP', 'triangle-exclamation-point')):
        lines = [l.strip() for l in part.strip().split('\n') if l.strip()]
        title = next((l[4:] for l in lines if l.startswith('### ')), ''); ic = field(lines, 'icon') or di; w = 6.0
        rect(s, x, 2.1, w, 4.6, fill=PAPER, line=BORDER, lw=0.75); rect(s, x, 2.1, w, 0.07, fill=acc)
        icon_badge(s, ic, x + 0.35, 2.45, 0.85, tint, color)
        txt(s, x + 1.4, 2.45, w - 1.6, 0.3, [{'runs': [R(tag, 11, acc, True, MONO)]}])
        txt(s, x + 1.4, 2.72, w - 1.6, 0.7, [{'runs': [R(title, 21, CHAR, True)]}])
        paras = []
        for k, v in kv(lines):
            paras.append({'runs': [R(k.upper(), 10.5, acc, True, MONO)], 'after': 3}); paras.append({'runs': [R(v, 19, CHAR)], 'after': 16, 'ls': 1.1})
        txt(s, x + 0.4, 3.85, w - 0.8, 2.75, paras)
def L_flow(s, body, a):
    lines = [l.strip() for l in body.strip().split('\n') if l.strip()]
    steps = re.findall(r'\[([^\]]+)\]', ' '.join(l for l in lines if not l.lower().startswith('icons:')))
    ics = [i.strip() for i in (field(lines, 'icons') or '').split(',') if i.strip()]
    n = len(steps); gap = 0.35 if n < 6 else 0.18; w = (12.23 - gap * (n - 1)) / n; y = 2.75; h = 3.55
    big = 22 if n < 5 else 18 if n < 7 else 15; small = 17 if n < 5 else 14 if n < 7 else 12
    ln = rect(s, 0.55 + w / 2, y + 0.42, 12.23 - w, 0.04); ln.fill.gradient(); ln.fill.gradient_angle = 0
    st = ln.fill.gradient_stops; st[0].color.rgb = TEAL; st[1].color.rgb = BLUE
    for i, step in enumerate(steps):
        head, _, rest = step.partition(':'); x = 0.55 + i * (w + gap); last = i == n - 1
        rect(s, x, y + 0.42, w, h, fill=TEAL if last else PAPER, line=None if last else BORDER, lw=0.75)
        d = 0.84; rect(s, x + w / 2 - d / 2, y, d, d, fill=WHITE, line=BLUE if last else TEAL, shape=MSO_SHAPE.OVAL, lw=2)
        if i < len(ics): icon(s, ics[i], 'teal', x + w / 2 - 0.26, y + 0.16, 0.52)
        else: txt(s, x + w / 2 - d / 2, y, d, d, [{'runs': [R(f'{i+1:02d}', 18, TEAL, True, MONO)]}], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        fg = WHITE if last else CHAR; ac = WHITE if last else TEAL
        txt(s, x + 0.2, y + 1.15, w - 0.4, 2.7, [{'runs': [R(f'STEP {i+1:02d}', 10.5, ac, True, MONO)], 'after': 4}, {'runs': [R(head.strip(), big, fg, True)], 'after': 10}, {'runs': [R(rest.strip(), small, fg)], 'ls': 1.1}])
def L_stat(s, body, a):
    lines = [l.strip() for l in body.strip().split('\n') if l.strip()]
    big = next((l[4:] for l in lines if l.startswith('### ')), ''); b = dict(kv(lines)); ic = field(lines, 'icon') or 'shield-check'
    rect(s, 0.55, 2.1, 12.23, 4.6, fill=PAPER, line=BORDER, lw=0.75); rect(s, 0.55, 2.1, 0.07, 4.6, fill=TEAL)
    icon_badge(s, ic, 1.2, 3.25, 2.2, TEAL_T, 'teal')
    txt(s, 3.9, 2.55, 8.6, 1.5, [{'runs': [R(big, 60 if len(big) <= 16 else 46 if len(big) <= 26 else 34, BLUE_D, True)]}], anchor=MSO_ANCHOR.BOTTOM)
    grad_rule(s, 3.93, 4.15, 1.2)
    txt(s, 3.9, 4.3, 8.6, 0.6, [{'runs': [R(b.get('Label', '').upper(), 15, TEAL, True, MONO)]}])
    if 'Context' in b: txt(s, 3.9, 4.85, 8.4, 1.5, [{'runs': [R(b['Context'], 19, CHAR)], 'ls': 1.15}])
def script_notes(path):
    if not path: return {}
    s = open(path, encoding='utf-8').read(); parts = re.split(r'\[SLIDE ([\w.]+)\]', s); out = {}
    for sid, t in zip(parts[1::2], parts[2::2]): out[sid] = re.sub(r'\n{2,}', '\n\n', re.split(r'\n# ', t)[0].strip())
    return out
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('out'); ap.add_argument('--script')
    ap.add_argument('--course', default=__import__('os').environ.get('DECK_LABEL','DEVLEAGUE')); ap.add_argument('--session', default='01'); ap.add_argument('--instructor', default='Instructor')
    a = ap.parse_args(); notes = script_notes(a.script)
    prs = Presentation(); prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
    chunks = re.split(r'<!-- SLIDE ([\w.]+) -->', open(a.src, encoding='utf-8').read())[1:]
    for sid, body in zip(chunks[::2], chunks[1::2]):
        s = prs.slides.add_slide(prs.slide_layouts[6])
        m = re.search(r':::([\w-]+)\n(.*?)\n:::', body, re.S); kind, inner = m.group(1), m.group(2)
        lines = [l.strip() for l in inner.split('\n') if l.strip()]
        if kind == 'title': L_title(s, lines, a)
        elif kind == 'divider': L_divider(s, lines, a)
        else:
            light_frame(s, sid, a); h = re.search(r'^## (.+)$', body, re.M); headline(s, h.group(1) if h else '')
            {'two-column': L_two, 'stat-callout': L_stat, 'horizontal-flow': L_flow}[kind](s, inner, a)
        n = notes.get(sid)
        if not n and kind == 'divider':
            t = next((l[3:] for l in lines if l.startswith('## ')), ''); n = f'[Divider] {t}. Advance to the next slide when you begin this section.'
        if n: s.notes_slide.notes_text_frame.text = n
    prs.save(a.out)
if __name__ == '__main__': main()
