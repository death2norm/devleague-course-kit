"""PBQ Practice Pack: drag-and-drop items for Moodle plus a printable copy and an instructor key, from one source file.

python3 tools/build_pbq_pack.py extras/pbq_pack.py OUTDIR
Writes <PREFIX>_PBQ_Practice_Pack.moodle.xml (category "<course>/PBQ Practice Pack", Moodle type ddwtos),
<PREFIX>_PBQ_Practice_Pack.md (student printable) and <PREFIX>_PBQ_Practice_Pack_Key.md (instructor key).

Source format (a Python file that calls add() once per PBQ):
  COMPANY = 'Harbor Point Logistics (fictional)'      # shown in the printable header
  add(id='P01', obj='1.7', title='Subnet the new branch', minutes=6,
      intro='What the student is told.',
      header=['Network', 'Hosts', 'Prefix'],            # table PBQ: rows are lists of cells
      rows=[['Sales', '100', '[[1:/25]]'], ...],
      lines=None,                                       # or sentence PBQ: lines=['The trunk carries ( [[1:802.1Q]] ).', ...]
      extras={'1': ['/24', '/29']},                     # unused choices per group
      explain='Why each answer is right (shown after submitting and in the key).')
A gap is [[group:answer]]; every gap in a group draws from the same choices. Reusing an answer is allowed.
"""
import os, re, sys, html, random, collections

GAP = re.compile(r'\[\[(\d+):([^\]]+)\]\]')
src, OUT = sys.argv[1], sys.argv[2]
P = os.environ.get('PREFIX', 'Course'); NAME = os.environ.get('COURSE_NAME', 'Course'); EXAM = os.environ.get('EXAM', '')
ITEMS = []; ns = {'add': lambda **k: ITEMS.append(k)}
exec(open(src, encoding='utf-8').read(), ns)
COMPANY = ns.get('COMPANY', 'a fictional company')
os.makedirs(OUT, exist_ok=True)
cdata = lambda s: '<![CDATA[' + s.replace(']]>', ']]]]><![CDATA[>') + ']]>'


def cells_text(q):
    return [c for r in q.get('rows') or [] for c in r] + list(q.get('lines') or [])


def boxes_for(q):
    boxes, index, uses = [], {}, collections.Counter()
    for t in cells_text(q):
        for g, ans in GAP.findall(t):
            uses[(int(g), ans)] += 1
            if (int(g), ans) not in index: index[(int(g), ans)] = len(boxes) + 1; boxes.append((ans, int(g)))
    for g, ex in (q.get('extras') or {}).items():
        for t in ex:
            assert (int(g), t) not in index, f"{q['id']}: extra '{t}' is also an answer"
            index[(int(g), t)] = len(boxes) + 1; boxes.append((t, int(g)))
    return boxes, index, uses


REUSE = ' Some choices are used more than once.'


def moodle_text(q, index, reuse=False):
    sub = lambda s: GAP.sub(lambda m: f"[[{index[(int(m.group(1)), m.group(2))]}]]", html.escape(s, quote=False).replace('&lt;', '<').replace('&gt;', '>'))
    h = f"<p>{html.escape(q['intro'] + (REUSE if reuse else ''))}</p>"
    if q.get('rows'):
        h += '<table border="1" cellpadding="4"><tr>' + ''.join(f'<th>{html.escape(c)}</th>' for c in q['header']) + '</tr>'
        h += ''.join('<tr>' + ''.join(f'<td>{sub(c)}</td>' for c in r) + '</tr>' for r in q['rows']) + '</table>'
    if q.get('lines'):
        h += '<ul>' + ''.join(f'<li>{sub(l)}</li>' for l in q['lines']) + '</ul>'
    return h


X = ['<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n',
     f'  <question type="category"><category><text>$course$/top/DevLeague {html.escape(NAME)}/PBQ Practice Pack</text></category></question>\n']
S = [f'# PBQ Practice Pack: {NAME}', '',
     f'*{len(ITEMS)} performance-based questions for practice outside class · {COMPANY} · About 6 minutes each, like the real exam\'s PBQs · Do them in Moodle if you can; this printable copy is the fallback*', '',
     'Name: ______________________________', '', '*Answers and explanations: take the same PBQs in Moodle (Session 17, PBQ Practice Pack); each one shows the right answer and why after you submit.*', '']
K = [f'# PBQ Practice Pack: {NAME} · Answer Key', '', '*Instructor and TA copy. Students see the same explanations in Moodle after they submit.*', '']
rnd = random.Random(11)
for n, q in enumerate(ITEMS, 1):
    boxes, index, uses = boxes_for(q)
    reuse = any(v > 1 for v in uses.values())
    X.append(f'  <question type="ddwtos">\n    <name><text>PBQ {n:02d} {html.escape(q["title"])}</text></name>\n'
             f'    <questiontext format="html"><text>{cdata(moodle_text(q, index, reuse))}</text></questiontext>\n'
             f'    <generalfeedback format="html"><text>{cdata("<p>" + html.escape(q["explain"]) + "</p>")}</text></generalfeedback>\n'
             f'    <defaultgrade>{q.get("marks", 1)}</defaultgrade><penalty>0</penalty><hidden>0</hidden><idnumber>{P}-PP-{q["id"]}</idnumber>\n'
             '    <shuffleanswers>1</shuffleanswers>\n'
             '    <correctfeedback format="html"><text>Your answer is correct.</text></correctfeedback>\n'
             '    <partiallycorrectfeedback format="html"><text>Your answer is partially correct.</text></partiallycorrectfeedback>\n'
             '    <incorrectfeedback format="html"><text>Your answer is incorrect.</text></incorrectfeedback>\n    <shownumcorrect/>\n'
             + ''.join(f'    <dragbox><text>{html.escape(t)}</text><group>{g}</group>{"<infinite/>" if uses[(g, t)] > 1 else ""}</dragbox>\n' for t, g in boxes)
             + f'    <tags><tag><text>{q["obj"]}</text></tag><tag><text>PBQ</text></tag></tags>\n  </question>\n')
    # printable
    S += ['---' if n > 1 else '', f'## PBQ {n}: {q["title"]}', '', f'*{q.get("minutes", 6)} minutes · {EXAM.replace("CompTIA ", "")} objective {q["obj"]}*', '', q['intro'] + (REUSE if reuse else ''), '']
    groups = collections.OrderedDict()
    for t, g in boxes: groups.setdefault(g, []).append(t)
    if q.get('rows'):
        for g, ch in groups.items():
            ch = sorted(set(ch), key=str.lower)
            lab = 'Choices' if len(groups) == 1 else f'Choices for column {g}'
            S += [f'**{lab}:** ' + ' · '.join(ch), '']
        S += ['| ' + ' | '.join(q['header']) + ' |', '|' + '---|' * len(q['header'])]
        S += ['| ' + ' | '.join(GAP.sub('________', c) for c in r) + ' |' for r in q['rows']]
        S.append('')
    if q.get('lines'):
        S += ['*Write the choice that completes each line.*', '']
        for l in q['lines']:
            def opts(m):
                ch = sorted(set(groups[int(m.group(1))]), key=str.lower); rnd.shuffle(ch)
                return '( ' + ' / '.join(ch) + ' )'
            S.append('- ' + GAP.sub(opts, l))
        S.append('')
    # key
    K += [f'## PBQ {n}: {q["title"]} (objective {q["obj"]})', '']
    if q.get('rows'):
        for r in q['rows']:
            ans = [m[1] for c in r for m in GAP.findall(c)]
            if ans: K.append(f"- **{r[0]}:** " + ' · '.join(ans))
    for l in q.get('lines') or []:
        K.append('- ' + GAP.sub(lambda m: f'**{m.group(2)}**', l))
    unused = [t for t, g in boxes if uses[(g, t)] == 0]
    if unused: K.append('- **Not used:** ' + ' · '.join(unused))
    K += ['', f"**Why:** {q['explain']}", '']
X.append('</quiz>\n')
open(os.path.join(OUT, f'{P}_PBQ_Practice_Pack.moodle.xml'), 'w', encoding='utf-8').write(''.join(X))
open(os.path.join(OUT, f'{P}_PBQ_Practice_Pack.md'), 'w', encoding='utf-8').write('\n'.join(S))
open(os.path.join(OUT, f'{P}_PBQ_Practice_Pack_Key.md'), 'w', encoding='utf-8').write('\n'.join(K))
print(f'PBQ pack: {len(ITEMS)} items')
