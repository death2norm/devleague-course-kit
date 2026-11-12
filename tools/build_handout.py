"""Student handout builder with a designed layout.

python3 build_handout.py handout.md out.docx --style A|B|C [--course "Network+ N10-009"] [--session 7]

A  Polished: header band, accent headings, inline commands as code chips, footer.
B  Cheat sheet: same header, each section as a card, two columns.
C  Study guide: A plus a "Check yourself" box built from the section headings, and the homework as a footer bar.
All three read the same handout_SNN.md, so no content changes are needed.
"""
import sys, re, os, argparse
from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

TEAL = RGBColor(0x1B, 0x7A, 0x8A); DARK = RGBColor(0x2B, 0x2F, 0x33); GRAY = RGBColor(0x6B, 0x72, 0x78)
WHITE = RGBColor(255, 255, 255)
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'assets')


def el(tag, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn('w:' + k), str(v))
    return e


def shade(cell, fill):
    cell._tc.get_or_add_tcPr().append(el('w:shd', val='clear', color='auto', fill=fill))


def borders(cell, left=None, others='none', lcolor='1B7A8A', lsize=24, ocolor='D5DEE0'):
    tcPr = cell._tc.get_or_add_tcPr(); b = el('w:tcBorders')
    for side in ('top', 'left', 'bottom', 'right'):
        if side == 'left' and left:
            b.append(el('w:left', val='single', sz=lsize, color=lcolor))
        elif others == 'none':
            b.append(el('w:' + side, val='nil'))
        else:
            b.append(el('w:' + side, val='single', sz=4, color=ocolor))
    tcPr.append(b)


def cell_margins(cell, top=80, bottom=80, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr(); m = el('w:tcMar')
    for k, v in (('top', top), ('bottom', bottom), ('left', left), ('right', right)):
        m.append(el('w:' + k, w=v, type='dxa'))
    tcPr.append(m)


def width(t, inches_list, keep=True):
    tbl = t._tbl; tblPr = tbl.tblPr
    tw = sum(inches_list)
    for e in tblPr.findall(qn('w:tblW')): tblPr.remove(e)
    tblPr.append(el('w:tblW', w=int(tw * 1440), type='dxa'))
    tblPr.append(el('w:tblLayout', type='fixed'))
    grid = tbl.tblGrid
    for k, gc in enumerate(grid.findall(qn('w:gridCol'))):
        gc.set(qn('w:w'), str(int(inches_list[k] * 1440)))
    for row in t.rows:
        for k, c in enumerate(row.cells):
            c.width = Inches(inches_list[k])
        if keep:
            trPr = row._tr.get_or_add_trPr(); trPr.append(el('w:cantSplit'))


def runs(p, text, color=DARK, size=None, italic=False, keycolor=None):
    """**bold** and `code` inline."""
    for part in re.split(r'(\*\*[^*]+\*\*|`[^`]+`)', text):
        if not part:
            continue
        if part.startswith('`'):
            r = p.add_run(' ' + part[1:-1] + ' '); r.font.name = 'Consolas'
            r._element.rPr.rFonts.set(qn('w:hAnsi'), 'Consolas')
            r.font.size = Pt((size or 10) - 1); r.font.color.rgb = RGBColor(0x12, 0x4E, 0x58)
            r._element.rPr.append(el('w:shd', val='clear', color='auto', fill='E8F1F2'))
            continue
        bold = part.startswith('**'); r = p.add_run(part[2:-2] if bold else part)
        r.bold = bold; r.italic = italic
        r.font.color.rgb = (keycolor or color) if bold else color
        if size:
            r.font.size = Pt(size)


def para_fmt(p, after=3, before=0, line=1.15):
    pf = p.paragraph_format; pf.space_after = Pt(after); pf.space_before = Pt(before); pf.line_spacing = line


def parse(md):
    """Returns title, subtitle, sections [(heading, [lines])]."""
    lines = open(md, encoding='utf-8').read().split('\n')
    title = sub = ''; secs = []; cur = None
    for ln in lines:
        ln = ln.rstrip()
        if ln.startswith('# '):
            title = ln[2:]; continue
        if re.match(r'^\*[^*].*\*$', ln) and not secs and not sub:
            sub = ln.strip('*'); continue
        m = re.match(r'^##+ (.*)', ln)
        if m:
            cur = [m.group(1), []]; secs.append(cur); continue
        if cur is None:
            if ln:
                cur = ['', []]; secs.append(cur)
            else:
                continue
        cur[1].append(ln)
    return title, sub, secs


def body(container, lines, size, keycolor):
    """Render one section's lines into a document or cell."""
    first = True; i = 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        if ln.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                if not re.match(r'^\|[\s:|-]*-[\s:|-]*$', lines[i]):
                    rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            t = container.add_table(rows=len(rows), cols=len(rows[0]))
            for ri, row in enumerate(rows):
                for ci, val in enumerate(row):
                    c = t.rows[ri].cells[ci]; c.paragraphs[0].text = ''; cell_margins(c, 40, 40, 80, 80)
                    borders(c, others='single')
                    runs(c.paragraphs[0], val, WHITE if ri == 0 else DARK, size - 1, keycolor=None if ri == 0 else keycolor)
                    para_fmt(c.paragraphs[0], 0)
                    if ri == 0:
                        shade(c, '1B7A8A')
                        for r in c.paragraphs[0].runs: r.bold = True
                    elif ri % 2 == 0:
                        shade(c, 'F4F8F8')
            sp = container.add_paragraph(); para_fmt(sp, 2); first = False
            continue
        if ln.startswith('>'):
            buf = []
            while i < len(lines) and lines[i].startswith('>'):
                buf.append(lines[i][1:].strip()); i += 1
            t = container.add_table(rows=1, cols=1); c = t.rows[0].cells[0]; c.paragraphs[0].text = ''
            shade(c, 'FFF6E5'); borders(c, left=True, lcolor='E8A33D'); cell_margins(c)
            for k, b in enumerate(buf):
                p = c.paragraphs[0] if k == 0 else c.add_paragraph(); runs(p, b, DARK, size); para_fmt(p, 1)
            sp = container.add_paragraph(); para_fmt(sp, 2)
            continue
        if ln.startswith('- '):
            p = container.add_paragraph(style='List Bullet'); runs(p, ln[2:], DARK, size, keycolor=keycolor); para_fmt(p, 1.5, line=1.1)
        elif re.match(r'^\d+\. ', ln):
            p = container.add_paragraph(style='List Number'); runs(p, re.sub(r'^\d+\. ', '', ln), DARK, size, keycolor=keycolor); para_fmt(p, 2)
        else:
            p = container.add_paragraph()
            runs(p, ln, DARK, size, keycolor=keycolor); para_fmt(p, 3)
        first = False; i += 1


def header_band(d, title, sub, course, session):
    t = d.add_table(rows=1, cols=2); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    a, b = t.rows[0].cells
    for c in (a, b):
        shade(c, '1B7A8A'); borders(c); cell_margins(c, 120, 120, 200, 200)
    width(t, [5.5, 1.6])
    kind = re.sub(r'^.*Session \d+:\s*', '', title) or 'Study Handout'
    p = a.paragraphs[0]; r = p.add_run(course.upper() + (f'  //  SESSION {session:02d}' if session else '') + '  //  ' + kind.upper())
    r.font.size = Pt(8); r.bold = True; r.font.color.rgb = RGBColor(0xBF, 0xE3, 0xE7); para_fmt(p, 2)
    big, small = (sub, '') if sub and len(sub) <= 90 else (kind, sub)
    p = a.add_paragraph(); r = p.add_run(big); r.bold = True; r.font.size = Pt(15); r.font.color.rgb = WHITE; para_fmt(p, 0, line=1.05)
    if small:
        p = a.add_paragraph(); r = p.add_run(small); r.font.size = Pt(9); r.font.color.rgb = RGBColor(0xE4, 0xF2, 0xF4); para_fmt(p, 0, 3)
    lp = os.path.join(ASSETS, 'logo_dark.png')
    bp = b.paragraphs[0]; bp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if os.path.exists(lp):
        bp.add_run().add_picture(lp, width=Inches(1.25))
    sp = d.add_paragraph(); para_fmt(sp, 4)


def section_heading(container, text, size=12.5):
    p = container.add_paragraph(); para_fmt(p, 3, 8)
    pPr = p._p.get_or_add_pPr(); bd = el('w:pBdr')
    bd.append(el('w:left', val='single', sz=28, space=6, color='1B7A8A')); pPr.append(bd)
    pPr.append(el('w:keepNext'))
    r = p.add_run(text); r.bold = True; r.font.size = Pt(size); r.font.color.rgb = TEAL
    return p


def footer(d, course, session):
    for s in d.sections[:1]:
        p = s.footer.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(f'DevLeague  ·  {course}' + (f'  ·  Session {session}' if session else '') + '  ·  Page ')
        r.font.size = Pt(8); r.font.color.rgb = GRAY
        r2 = p.add_run(); r2.font.size = Pt(8); r2.font.color.rgb = GRAY
        for t, txt in (('begin', None), (None, 'PAGE'), ('end', None)):
            if t:
                r2._r.append(el('w:fldChar', fldCharType=t))
            else:
                it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = txt; r2._r.append(it)


def columns(section, n):
    sp = section._sectPr; c = sp.find(qn('w:cols'))
    if c is None:
        c = el('w:cols'); sp.append(c)
    c.set(qn('w:num'), str(n)); c.set(qn('w:space'), '360')


def build(md, out, style='A', course='Network+ N10-009', session=None):
    title, sub, secs = parse(md)
    if session is None:
        m = re.search(r'Session (\d+)', title); session = int(m.group(1)) if m else None
    d = Document(); s = d.sections[0]
    s.left_margin = s.right_margin = Inches(0.7); s.top_margin = Inches(0.55); s.bottom_margin = Inches(0.6)
    st = d.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(10)
    st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Calibri')
    header_band(d, title, sub, course, session)
    homework = [x for x in secs if x[0].lower().startswith('homework')]
    main = [x for x in secs if x not in homework] if style in 'BC' else secs
    size = 9.5 if style == 'B' else 10
    if style == 'B':
        new = d.add_section(0)  # continuous
        columns(new, 2)
        for h, lines in main:
            t = d.add_table(rows=1, cols=1); width(t, [3.4], keep=len([x for x in lines if x.strip()]) <= 8); c = t.rows[0].cells[0]
            shade(c, 'F6FAFA'); borders(c, left=True, others='single'); cell_margins(c, 90, 90, 150, 120)
            hp = c.paragraphs[0]; r = hp.add_run(h); r.bold = True; r.font.size = Pt(11); r.font.color.rgb = TEAL; para_fmt(hp, 3)
            body(c, lines, size, TEAL)
            sp = d.add_paragraph(); para_fmt(sp, 4, line=0.8)
        one = d.add_section(0); columns(one, 1)
    else:
        for h, lines in main:
            if h:
                section_heading(d, h)
            body(d, lines, size, TEAL)
    if style == 'C':
        t = d.add_table(rows=1, cols=1); width(t, [7.1]); c = t.rows[0].cells[0]
        shade(c, 'EEF6F6'); borders(c, left=True); cell_margins(c, 100, 100, 180, 140)
        p = c.paragraphs[0]; r = p.add_run('Check yourself before the quiz'); r.bold = True; r.font.color.rgb = TEAL; r.font.size = Pt(11); para_fmt(p, 3)
        p = c.add_paragraph(); runs(p, 'Can you explain each of these out loud, without notes, in two sentences?', GRAY, 9.5, True); para_fmt(p, 3)
        p = c.add_paragraph(); para_fmt(p, 1, line=1.4)
        runs(p, '     '.join('\u2610 ' + h for h, _ in main if h), DARK, 10)
        for h, lines in homework:
            p = c.add_paragraph(); para_fmt(p, 0, 4)
            r = p.add_run('Tonight\u2019s homework:  '); r.bold = True; r.font.size = Pt(10); r.font.color.rgb = TEAL
            runs(p, ' '.join(x.lstrip('- ') for x in lines if x.strip()), DARK, 10)
        sp = d.add_paragraph(); para_fmt(sp, 4)
    if style == 'B':
        for h, lines in homework:
            t = d.add_table(rows=1, cols=1); width(t, [7.1]); c = t.rows[0].cells[0]
            shade(c, '2B2F33'); borders(c); cell_margins(c, 90, 90, 180, 140)
            p = c.paragraphs[0]; r = p.add_run('TONIGHT’S HOMEWORK   '); r.bold = True; r.font.size = Pt(9); r.font.color.rgb = RGBColor(0x7F, 0xD1, 0xDB)
            runs(p, ' '.join(x.lstrip('- ') for x in lines if x.strip()), WHITE, 10, keycolor=WHITE)
        p = c.add_paragraph(); para_fmt(p, 0, 3)
        r = p.add_run('CHECK YOURSELF   '); r.bold = True; r.font.size = Pt(9); r.font.color.rgb = RGBColor(0x7F, 0xD1, 0xDB)
        runs(p, '    '.join('\u2610 ' + h for h, _ in main if h), WHITE, 9.5)
    footer(d, course, session)
    d.save(out)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('md'); ap.add_argument('out')
    ap.add_argument('--style', default='A'); ap.add_argument('--course', default='Network+ N10-009')
    ap.add_argument('--session', type=int)
    a = ap.parse_args(); build(a.md, a.out, a.style.upper(), a.course, a.session)
