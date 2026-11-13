"""python3 build_docx.py input.md output.docx [--logo] [--compact | --tight]
--tight: one-page reference sheets (cheat sheets): narrower margins, 9 pt body, 8 pt tables."""
import sys, re, os
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
TEAL = RGBColor(0x1B, 0x7A, 0x8A); DARK = RGBColor(0x2B, 0x2F, 0x33); GRAY = RGBColor(0x6B, 0x72, 0x78)
def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr(); s = OxmlElement('w:shd')
    s.set(qn('w:val'), 'clear'); s.set(qn('w:color'), 'auto'); s.set(qn('w:fill'), hexcolor); tcPr.append(s)
def add_runs(p, text, color=DARK, size=None, italic=False):
    """**bold**, `code` (Consolas, no backticks) and *italic* inline."""
    for part in re.split(r'(\*\*[^*]+\*\*|`[^`]+`|(?<![\w*])\*[^*\s][^*]*\*(?![\w*]))', text):
        if not part: continue
        if part.startswith('`') and part.endswith('`') and len(part) > 1:
            r = p.add_run(part[1:-1]); r.font.name = 'Consolas'; r._element.rPr.rFonts.set(qn('w:hAnsi'), 'Consolas')
            r.font.color.rgb = RGBColor(0x12, 0x4E, 0x58); r.italic = italic
            if size: r.font.size = Pt(size - 0.5)
            continue
        bold = part.startswith('**'); ital = not bold and len(part) > 2 and part[0] == '*' and part[-1] == '*'
        r = p.add_run(part[2:-2] if bold else part[1:-1] if ital else part)
        r.bold = bold; r.italic = italic or ital; r.font.color.rgb = color
        if size: r.font.size = Pt(size)
def new_list(d):
    # each numbered list restarts at 1
    numbering = d.part.numbering_part.element
    sid = d.styles['List Number']._element.pPr.numPr.numId.val
    abstract = numbering.num_having_numId(sid).abstractNumId.val
    num = numbering.add_num(abstract); num.add_lvlOverride(ilvl=0).add_startOverride(1)
    return num.numId
def build(md, out, logo=False, compact=False, tight=False):
    compact = compact or tight
    d = Document(); sec = d.sections[0]
    for side in ('left_margin', 'right_margin'): setattr(sec, side, Inches(0.6 if tight else 0.9 if compact else 1))
    sec.top_margin = sec.bottom_margin = Inches(0.5 if tight else 0.7 if compact else 1)
    st = d.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(9 if tight else 10 if compact else 11)
    st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Calibri')
    st.paragraph_format.space_after = Pt(2 if tight else 4 if compact else 8); st.paragraph_format.line_spacing = 1.0 if tight else 1.1 if compact else 1.2
    for i, sz in ((1, 15 if compact else 18), (2, 12 if compact else 14), (3, 11 if compact else 12)):
        h = d.styles[f'Heading {i}']; h.font.name = 'Calibri'; h.font.size = Pt(sz); h.font.bold = True
        h.font.color.rgb = TEAL if i < 3 else DARK
        h.paragraph_format.space_before = Pt(5 if tight else 8 if compact else 14); h.paragraph_format.space_after = Pt(3 if compact else 6)
    if logo:
        p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        lp = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'logo_light.png')
        if os.path.exists(lp): p.add_run().add_picture(lp, width=Inches(1.4 if tight else 2.0))
    lines = open(md, encoding='utf-8').read().split('\n'); i = 0; in_list = False; num_id = None
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln: i += 1; continue
        if not re.match(r'^\d+\. ', ln): in_list = False
        if ln == '---': d.add_page_break(); i += 1; continue
        if ln.startswith('```'):
            buf = []; i += 1
            while i < len(lines) and not lines[i].startswith('```'): buf.append(lines[i].rstrip()); i += 1
            i += 1
            t = d.add_table(rows=1, cols=1); t.style = 'Table Grid'
            c = t.rows[0].cells[0]; shade(c, 'F2F4F5'); c.paragraphs[0].text = ''
            for k, b in enumerate(buf):
                p = c.paragraphs[0] if k == 0 else c.add_paragraph()
                p.paragraph_format.space_after = Pt(0); p.paragraph_format.line_spacing = 1.0
                r = p.add_run(b if b else ' '); r.font.name = 'Consolas'; r.font.size = Pt(7.5 if compact else 8.5)
            d.add_paragraph(); continue
        m = re.match(r'^(#{1,3}) (.*)', ln)
        if m:
            h = d.add_heading(m.group(2), level=len(m.group(1)))
            if logo and len(m.group(1)) == 1 and i < 3: h.alignment = WD_ALIGN_PARAGRAPH.CENTER
            i += 1; continue
        m = re.match(r'^!\[([^\]]*)\]\(([^)\s]+)\)(?:\{width=([\d.]+)\})?$', ln)
        if m:  # ![caption](path){width=5}: picture centred, caption under it; path relative to the .md file
            ip = m.group(2) if os.path.isabs(m.group(2)) else os.path.join(os.path.dirname(os.path.abspath(md)), m.group(2))
            p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.keep_with_next = True
            if os.path.exists(ip): p.add_run().add_picture(ip, width=Inches(float(m.group(3) or 5.5)))
            else: r = p.add_run(f'[screenshot missing: {m.group(2)}]'); r.bold = True; r.font.color.rgb = RGBColor(0xC0, 0x39, 0x2B)
            if m.group(1):
                c = d.add_paragraph(); c.alignment = WD_ALIGN_PARAGRAPH.CENTER; add_runs(c, m.group(1), GRAY, 9, True)
            i += 1; continue
        if re.match(r'^\[SLIDE [\w.]+\]$', ln):
            p = d.add_paragraph(); r = p.add_run(ln); r.bold = True; r.font.color.rgb = TEAL; r.font.size = Pt(9)
            p.paragraph_format.space_after = Pt(2); i += 1; continue
        if re.match(r'^\*[^*].*\*$', ln):
            add_runs(d.add_paragraph(), ln.strip('*'), GRAY, 9, True); i += 1; continue
        if re.match(r'^- \[[ xX]\] ', ln):  # checklist item: box, no bullet
            p = d.add_paragraph(); p.paragraph_format.left_indent = Inches(0.25); p.paragraph_format.first_line_indent = Inches(-0.25)
            r = p.add_run('\u2611  ' if ln[3] in 'xX' else '\u2610  '); r.font.color.rgb = TEAL; add_runs(p, ln[6:]); i += 1; continue
        if ln.startswith('- '): add_runs(d.add_paragraph(style='List Bullet'), ln[2:]); i += 1; continue
        if re.match(r'^\d+\. ', ln):
            p = d.add_paragraph(style='List Number'); add_runs(p, re.sub(r'^\d+\. ', '', ln))
            if not in_list: num_id = new_list(d)
            in_list = True; npr = p._p.get_or_add_pPr().get_or_add_numPr(); npr.get_or_add_ilvl().val = 0; npr.get_or_add_numId().val = num_id
            i += 1; continue
        if ln.startswith('>'):
            buf = []
            while i < len(lines) and lines[i].startswith('>'): buf.append(lines[i][1:].strip()); i += 1
            t = d.add_table(rows=1, cols=1); t.style = 'Table Grid'
            c = t.rows[0].cells[0]; shade(c, 'EEF6F6'); c.paragraphs[0].text = ''
            for k, b in enumerate(buf): add_runs(c.paragraphs[0] if k == 0 else c.add_paragraph(), b)
            d.add_paragraph(); continue
        if ln.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                if not re.match(r'^\|[\s:|-]*-[\s:|-]*$', lines[i].rstrip()): rows.append([c.strip() for c in lines[i].strip('|').split('|')])
                i += 1
            t = d.add_table(rows=len(rows), cols=len(rows[0])); t.style = 'Table Grid'
            for tr in t.rows:  # a row never splits across a page break; the header row repeats
                trPr = tr._tr.get_or_add_trPr(); trPr.append(OxmlElement('w:cantSplit'))
            hdr = t.rows[0]._tr.get_or_add_trPr(); hdr.append(OxmlElement('w:tblHeader'))
            # column widths by content: average text length, never narrower than the longest word
            sec = d.sections[-1]; avail = sec.page_width - sec.left_margin - sec.right_margin
            plain = lambda v: re.sub(r'[*`]', '', v)
            need = []
            for ci in range(len(rows[0])):
                col = [plain(r[ci]) for r in rows if ci < len(r)]
                avg = sum(len(v) for v in col) / len(col)
                longest = max((len(w) for v in col for w in v.split()), default=1)
                need.append(max(avg, longest * 1.6, len(col[0]) * 1.3, 4) ** 0.8)
            t.autofit = False
            grid = t._tbl.tblGrid.findall(qn('w:gridCol'))
            for ci, n in enumerate(need):
                w = int(avail * n / sum(need))
                if ci < len(grid): grid[ci].set(qn('w:w'), str(int(w / 635)))  # EMU to twips
                for tr in t.rows:
                    if ci < len(tr.cells): tr.cells[ci].width = w
            for ri, row in enumerate(rows):
                for ci, val in enumerate(row):
                    c = t.rows[ri].cells[ci]; c.paragraphs[0].text = ''
                    add_runs(c.paragraphs[0], val, DARK, 8 if tight else 9 if compact else 10)
                    if ri == 0:
                        shade(c, '1B7A8A')
                        for r in c.paragraphs[0].runs: r.bold = True; r.font.color.rgb = RGBColor(255, 255, 255)
            d.add_paragraph(); continue
        add_runs(d.add_paragraph(), ln); i += 1
    d.save(out)
if __name__ == '__main__':
    a = sys.argv; build(a[1], a[2], logo='--logo' in a, compact='--compact' in a, tight='--tight' in a)
