"""Course acronym set from one TSV: Moodle glossary, printable glossary, matching drills and flashcards.

python3 tools/build_acronyms.py extras/acronyms.tsv OUTDIR [--back extras/acronyms_back.md]
TSV columns (header row): acronym, meaning, note, session. Write the meanings and notes yourself from the
exam objectives; CompTIA's own acronym list is copyrighted, so it is a checklist, not a source to copy.

Writes into OUTDIR:
  <PREFIX>_Acronym_Glossary.moodle.xml   Moodle glossary import (Glossary, Import entries)
  <PREFIX>_Acronym_Glossary.md           printable source (build_extras.sh turns it into the PDF)
  <PREFIX>_Acronym_Drills.gift.txt       matching questions, 6 acronyms each, category "<course>/Acronym Drills"
  <PREFIX>_Acronym_Flashcards.csv        two columns, for flashcard apps
The optional back page (--back) is appended after a page break: use it for the interest-list call to action.
"""
import csv, html, os, sys, argparse, collections, random

ap = argparse.ArgumentParser(); ap.add_argument('tsv'); ap.add_argument('out'); ap.add_argument('--back')
a = ap.parse_args()
P = os.environ.get('PREFIX', 'Course'); NAME = os.environ.get('COURSE_NAME', 'Course'); EXAM = os.environ.get('EXAM', '')
COURSE = 'DevLeague ' + NAME
rows = [r for r in csv.DictReader(open(a.tsv, encoding='utf-8'), delimiter='\t') if r.get('acronym')]
for r in rows:
    for k in ('acronym', 'meaning'):
        assert r[k].strip(), f'empty {k}: {r}'
os.makedirs(a.out, exist_ok=True)
def key(r): return (r['acronym'].lstrip('0123456789.').upper() or r['acronym'], r['acronym'])
rows.sort(key=key)

# 1. Moodle glossary XML
E = []
for r in rows:
    d = f"<p><strong>{html.escape(r['meaning'])}</strong></p>"
    if r.get('note'): d += f"<p>{html.escape(r['note'])}</p>"
    if r.get('session'): d += f"<p><em>Session {html.escape(r['session'])}</em></p>"
    E.append(f"<ENTRY><CONCEPT>{html.escape(r['acronym'])}</CONCEPT><DEFINITION>{html.escape(d)}</DEFINITION><FORMAT>1</FORMAT>"
             "<USEDYNALINK>0</USEDYNALINK><CASESENSITIVE>1</CASESENSITIVE><FULLMATCH>1</FULLMATCH><TEACHERENTRY>1</TEACHERENTRY></ENTRY>")
xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<GLOSSARY><INFO>'
       f'<NAME>{html.escape(NAME)} Acronyms</NAME><INTRO>{html.escape("<p>Every acronym the course uses, with a plain-language note and the session that teaches it.</p>")}</INTRO>'
       '<INTROFORMAT>1</INTROFORMAT><ALLOWDUPLICATEDENTRIES>1</ALLOWDUPLICATEDENTRIES><DISPLAYFORMAT>dictionary</DISPLAYFORMAT>'
       '<SHOWSPECIAL>1</SHOWSPECIAL><SHOWALPHABET>1</SHOWALPHABET><SHOWALL>1</SHOWALL><ALLOWCOMMENTS>0</ALLOWCOMMENTS>'
       '<USEDYNALINK>0</USEDYNALINK><DEFAULTAPPROVAL>0</DEFAULTAPPROVAL><GLOBALGLOSSARY>0</GLOBALGLOSSARY><ENTBYPAGE>20</ENTBYPAGE>'
       '<ENTRIES>' + ''.join(E) + '</ENTRIES></INFO></GLOSSARY>\n')
open(os.path.join(a.out, f'{P}_Acronym_Glossary.moodle.xml'), 'w', encoding='utf-8').write(xml)

# 2. Printable glossary (markdown for build_docx.py), grouped by first letter
L = [f'# {NAME} Acronym Glossary', '',
     f'*{EXAM} · {len(rows)} acronyms the course uses, each with a one-line note and the session that teaches it · DevLeague*', '']
groups = collections.OrderedDict()
for r in rows:
    k = key(r)[0][0]; k = k if k.isalpha() else '#'
    groups.setdefault(k, []).append(r)
for k, rs in groups.items():
    L += [f'## {k if k != "#" else "Numbers"}', '', '| Acronym | Stands for | What to remember | Session |', '|---|---|---|---|']
    L += [f"| **{r['acronym']}** | {r['meaning']} | {r.get('note', '')} | {r.get('session', '')} |" for r in rs]
    L.append('')
if a.back and os.path.exists(a.back):
    L += ['---', '', open(a.back, encoding='utf-8').read().strip(), '']
open(os.path.join(a.out, f'{P}_Acronym_Glossary.md'), 'w', encoding='utf-8').write('\n'.join(L))

# 3. Matching drills (GIFT), 6 per question, one meaning per acronym (duplicate acronyms skipped)
esc = lambda t: ''.join('\\' + c if c in '\\~=#{}:' else c for c in t)
seen, pool = set(), []
for r in rows:
    if r['acronym'] in seen: continue
    seen.add(r['acronym']); pool.append(r)
rnd = random.Random(7); rnd.shuffle(pool)
G = [f'$CATEGORY: $course$/top/{COURSE}/Acronym Drills', '']
n = 0
for i in range(0, len(pool) - len(pool) % 6, 6):
    grp = pool[i:i + 6]; n += 1
    assert len({g['meaning'] for g in grp}) == 6
    G.append(f'::Acronym Drill {n:02d}::Match each acronym to what it stands for. {{')
    G += [f"\t={esc(g['acronym'])} -> {esc(g['meaning'])}" for g in grp]
    G += ['}', '']
open(os.path.join(a.out, f'{P}_Acronym_Drills.gift.txt'), 'w', encoding='utf-8').write('\n'.join(G))

# 4. Flashcards CSV
with open(os.path.join(a.out, f'{P}_Acronym_Flashcards.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    for r in rows: w.writerow([r['acronym'], r['meaning'] + (f" ({r['note']})" if r.get('note') else '')])
print(f'acronyms: {len(rows)} entries, {n} matching drills')
