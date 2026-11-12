"""Automatic build checks for a DevLeague course workspace.

python3 tools/checks.py            # every session found in src/
python3 tools/checks.py 07 08      # only these sessions
Run from the workspace root (the folder that holds src/ and course.env).

FAIL items must be fixed before a package is sent. WARN items need a look and a decision.
Checks (each one exists because a review or audit had to fix the same problem by hand):
  1. cues      every [SLIDE x] cue in the script has a slide, and every non-divider slide has a cue, same order
  2. overlap   a nightly quiz question too close to that night's practice questions, lab files or another quiz
  3. answers   quiz keys that are the longest choice by a wide margin (test-wise students pick the longest)
  4. letters   spoken practice-question answers bunched on one letter (and right choices that are the longest)
  5. hedges    unhedged claims about what the exam will do ("the exam loves ...")
  6. facts     course-specific forbidden wording from course_lint.tsv (stale pass marks, old names, retired facts)
  7. keys      quiz JSON and quiz key agree on the number of questions; each question has exactly one right answer
"""
import sys, os, re, json, glob, difflib

FAILS, WARNS = [], []
def fail(s, m): FAILS.append(f"FAIL S{s} {m}")
def warn(s, m): WARNS.append(f"WARN S{s} {m}")

STOP = set('a an the of to in on for and or is are be it its this that which what with by at from as can was were has have does do should must most best first will would you your their they'.split())
def words(t): return {w for w in re.findall(r"[a-z0-9./:]+", t.lower()) if w not in STOP}
def sim(a, b):
    wa, wb = words(a), words(b)
    j = len(wa & wb) / max(1, len(wa | wb))
    return max(j, difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio())

def read(p): return open(p, encoding='utf-8').read() if os.path.exists(p) else ''

def practice_questions(script):
    """Spoken practice questions: (stem, choices) from 'Let's try one/do one ...' and its A-D lines."""
    out = []
    for m in re.finditer(r"Let's (?:try|do) (?:one|another)[.!]?\s*(.+?)\n\s*\n((?:[A-D]\. [^\n]*\n)+)", script, re.S):
        out.append((m.group(1).strip(), re.findall(r'^[A-D]\. (.*)$', m.group(2), re.M)))
    return out

def choice_overlap(a, b):
    na = {re.sub(r'\W+', ' ', x.lower()).strip() for x in a}; nb = {re.sub(r'\W+', ' ', x.lower()).strip() for x in b}
    return len(na & nb) / max(1, min(len(na), len(nb)))

def check_cues(s, script, slides):
    cues = re.findall(r'^\[SLIDE ([^\]]+)\]', script, re.M)
    ids = re.findall(r'<!-- SLIDE ([^ ]+) -->', slides)
    cued = [i for i in ids if not re.match(r'^D\d+$', i)]
    # break slides are dividers in content but cued; compare on the set the script uses
    missing = [c for c in cues if c not in ids]
    uncued = [i for i in cued if i not in cues]
    if missing: fail(s, f"cues: script cues with no slide: {', '.join(missing[:8])}")
    if uncued: warn(s, f"cues: slides never cued in the script (no speaker notes): {', '.join(uncued[:8])}")
    order = [c for c in cues if c in ids]
    pos = [ids.index(c) for c in order]
    if pos != sorted(pos): fail(s, "cues: script cue order differs from slide order")
    dup = sorted({c for c in cues if cues.count(c) > 1})
    if dup: warn(s, f"cues: slides cued more than once: {', '.join(dup[:8])}")

def check_quiz(s, quiz, script, labtext, others):
    pq = practice_questions(script)
    for i, q in enumerate(quiz, 1):
        stem = q['stem']
        for k, (p, pc) in enumerate(pq, 1):
            sc = sim(stem, p[-len(stem) * 2:]); co = choice_overlap([a[0] for a in q['answers']], pc)
            if sc >= 0.70 and co >= 0.5: fail(s, f"overlap: Q{i} copies practice question {k} (stem {sc:.2f}, {co:.0%} same choices): {stem[:80]}")
            elif sc >= 0.70: warn(s, f"overlap: Q{i} reuses the wording of practice question {k} with new choices (stem {sc:.2f}): {stem[:80]}")
            elif sc >= 0.55 and co >= 0.5: warn(s, f"overlap: Q{i} close to practice question {k} (stem {sc:.2f}, {co:.0%} same choices): {stem[:80]}")
        for para in re.split(r'\n\s*\n', labtext):
            if len(para) < 60: continue
            sc = sim(stem, para[-len(stem) * 2:])
            if sc >= 0.60: warn(s, f"overlap: Q{i} close to a lab or worksheet item ({sc:.2f}): {stem[:90]}")
        for name, o in others:
            sc = sim(stem, o)
            if sc >= 0.75: warn(s, f"overlap: Q{i} close to {name} ({sc:.2f}): {stem[:90]}")
        right = [a for a in q['answers'] if a[1]]
        if len(right) != 1: fail(s, f"keys: Q{i} has {len(right)} right answers")
        if right:
            k = len(right[0][0]); d = [len(a[0]) for a in q['answers'] if not a[1]]
            if d and k > max(d) and k >= 1.6 * max(d):
                warn(s, f"answers: Q{i} key is much the longest choice ({k} vs {max(d)} characters)")
    longest = sum(1 for q in quiz if [a for a in q['answers'] if a[1]] and
                  len([a for a in q['answers'] if a[1]][0][0]) > max([len(a[0]) for a in q['answers'] if not a[1]] or [0]))
    if quiz and longest / len(quiz) > 0.5:
        warn(s, f"answers: key is the longest choice in {longest} of {len(quiz)} questions (aim for a third or fewer)")

def check_letters(s, slides):
    L = re.findall(r'\*\*Label:\*\* Answer: ([A-D])', slides)
    if len(L) >= 6:
        top = max(set(L), key=L.count)
        if L.count(top) / len(L) > 0.5:
            warn(s, f"letters: {L.count(top)} of {len(L)} practice answers are {top}")
        if len(set(L)) <= 2: warn(s, f"letters: practice answers use only {''.join(sorted(set(L)))}")

def check_practice_lengths(s, script, slides):
    """Spoken practice questions: the right choice shouldn't be the longest too often, or by a wide margin."""
    labels = re.findall(r'<!-- SLIDE ([^ ]+) -->\n(?:(?!<!-- SLIDE).)*?\*\*Label:\*\* Answer: ([A-D])', slides, re.S)
    cues = [(m.group(1), m.start()) for m in re.finditer(r'^\[SLIDE ([^\]]+)\]', script, re.M)]
    n = longest = 0
    for sid, L in labels:
        idx = [i for i, (c, _) in enumerate(cues) if c == sid]
        if not idx: continue
        i = idx[0]; seg = script[cues[i][1]:cues[i + 1][1] if i + 1 < len(cues) else len(script)]
        ch = dict(re.findall(r'^([A-D])\. (.*)$', seg, re.M))
        if L not in ch or len(ch) < 3: continue
        n += 1; k = len(ch[L]); d = max(len(v) for x, v in ch.items() if x != L)
        if k > d: longest += 1
        if k > d and k >= 1.6 * d:
            warn(s, f"answers: practice {sid} right choice is much the longest ({k} vs {d} characters)")
    if n >= 6 and longest / n > 0.4:
        warn(s, f"answers: right choice is the longest in {longest} of {n} practice questions (aim for a third or fewer)")

HEDGE_BAD = re.compile(r"\b(the exam (?:loves|likes|always|will (?:ask|test|give|show)|is going to|wants you to)|you will (?:definitely |always )?(?:see|be asked|get)|(?:always|guaranteed to) (?:shows?|comes?) up|every exam (?:has|asks))", re.I)
HEDGE_OK = re.compile(r"\b(I'd expect|likely|probably|often|tends to|in my experience|could|may|might|I'd bet)\b", re.I)
def check_hedges(s, name, text):
    for ln in text.split('\n'):
        for sent in re.split(r'(?<=[.!?])\s+', ln):
            if HEDGE_BAD.search(sent) and not HEDGE_OK.search(sent):
                warn(s, f"hedges: {name}: unhedged exam claim: \"{sent.strip()[:110]}\"")

def load_lint():
    rules = []
    for line in read('course_lint.tsv').split('\n'):
        if not line.strip() or line.startswith('#'): continue
        parts = line.split('\t')
        if len(parts) >= 2: rules.append((re.compile(parts[0], re.I), parts[1], re.compile(parts[2]) if len(parts) > 2 and parts[2] else None))
    return rules

def check_facts(s, rules, files):
    for f in files:
        text = read(f); base = os.path.basename(f)
        for rx, msg, allow in rules:
            if allow and allow.search(base): continue
            for m in rx.finditer(text):
                ln = text.count('\n', 0, m.start()) + 1
                fail(s, f"facts: {base} line {ln}: {msg} (found \"{m.group(0)}\")")

def main():
    sessions = sys.argv[1:] or sorted({re.search(r'_S(\d+)', p).group(1) for p in glob.glob('src/script_S*.md')})
    rules = load_lint()
    allq = {}
    for f in glob.glob('src/quiz_S*.json'):
        n = re.search(r'_S(\d+)', f).group(1)
        allq[n] = json.load(open(f, encoding='utf-8'))
    for s in sessions:
        script, slides = read(f'src/script_S{s}.md'), read(f'src/slides_S{s}.md')
        if not script: continue
        check_cues(s, script, slides)
        check_letters(s, slides)
        check_practice_lengths(s, script, slides)
        lab = read(f'src/labguide_S{s}.md') + '\n\n' + read(f'src/worksheet_S{s}.md')
        if s in allq:
            others = [(f"S{n} Q{i}", q['stem']) for n, qs in allq.items() if n != s for i, q in enumerate(qs, 1)]
            check_quiz(s, allq[s], script, lab, others)
            key = read(f'src/quiz_key_S{s}.md')
            kq = len(re.findall(r'^## Q\d+', key, re.M))
            if key and kq != len(allq[s]): fail(s, f"keys: quiz JSON has {len(allq[s])} questions, quiz key has {kq}")
        for name in ('script', 'handout'):
            check_hedges(s, name, read(f'src/{name}_S{s}.md'))
        check_facts(s, rules, sorted(glob.glob(f'src/*_S{s}.*')))
    for line in FAILS + WARNS: print(line)
    print(f"CHECKS: {len(FAILS)} FAIL, {len(WARNS)} WARN across {len(sessions)} sessions")
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
