#!/usr/bin/env python3
"""Objective coverage matrix: exam objectives against sessions, quizzes, practice pools and script text.

python3 tools/coverage_matrix.py OBJECTIVES.md SRC_DIR OUT.md [--bank bank_items.json]

OBJECTIVES.md  "## 1.1 Title" headings with "- " sub-bullet lines (items inside a bullet split on ";",
               and "Label: a; b" uses the items after the colon). Lines in *italics* are ignored.
SRC_DIR        slides_SNN.md (block dividers carry "- **Objectives:** 1.1, 1.2"), script_SNN.md,
               handout_SNN.md, labguide_SNN.md, quiz_SNN.json (each item's "domain" is "D1 1.7").
--bank         JSON list of practice-bank items with "obj" and "pool" (A-D); adds one column per pool.

Writes a markdown report: one row per objective, then every sub-bullet whose words (or acronym)
don't appear in any script, handout or lab guide. Most of those are taught under other wording:
check each and either confirm the session or add a sentence. Re-run after any content change.
"""
import re, os, sys, glob, json, collections


def objectives(path):
    objs, cur = collections.OrderedDict(), None
    for ln in open(path, encoding='utf-8'):
        m = re.match(r'##\s+(\d\.\d+)\s+(.*)', ln)
        if m:
            cur = m.group(1); objs[cur] = {'title': m.group(2).strip(), 'bullets': []}; continue
        if cur and ln.startswith('- ') and not ln[2:].lstrip().startswith('*'):
            body = re.sub(r'\s+[—–]\s+taught in.*$', '', ln[2:].strip())
            if ':' in body and body.index(':') < 60:
                head, rest = body.split(':', 1)
                items = split_top(rest) or [head]
            else:
                items = split_top(body)
            objs[cur]['bullets'] += items
    return objs


def split_top(s):
    """Split on ';' outside parentheses."""
    out, depth, cur = [], 0, ''
    for ch in s:
        depth += (ch == '(') - (ch == ')')
        if ch == ';' and depth == 0:
            out.append(cur); cur = ''
        else:
            cur += ch
    out.append(cur)
    return [x.strip() for x in out if x.strip()]


def strip_parens(s):
    while re.search(r'\([^()]*\)', s):
        s = re.sub(r'\([^()]*\)', '', s)
    return ' '.join(s.split())


STOP = {'and', 'the', 'for', 'with', 'vs.', 'of', 'to', 'or', 'issues', 'types', 'concepts'}


def expand(tag):
    """'1.1, 1.4' -> {1.1, 1.4}; '5.1–5.5' -> 5.1..5.5; 'All domains' -> set()."""
    out = set()
    for a, b in re.findall(r'(\d\.\d+)\s*[–-]\s*(\d\.\d+)', tag):
        d = a.split('.')[0]
        for k in range(int(a.split('.')[1]), int(b.split('.')[1]) + 1):
            out.add(f'{d}.{k}')
    tag = re.sub(r'(\d\.\d+)\s*[–-]\s*(\d\.\d+)', '', tag)
    out |= set(re.findall(r'\b\d\.\d+\b', tag))
    return out


def candidates(item):
    item = item.strip().rstrip('.')
    acr = re.findall(r'\(([^()]+)\)', item)
    plain = strip_parens(item)
    c = {plain} | {a for a in acr if len(a) > 1}
    for a in acr:  # "(tunneling, dual stack, NAT64)" -> each item
        c |= {x.strip() for x in re.split(r',\s*|;\s*', a) if len(x.strip()) > 1}
    for x, y in re.findall(r'\((\w+)\)(\w+)', item):  # "registered jack (RJ)11" -> RJ11
        c.add(x + y)
    for part in re.split(r'/| vs\. | and |, ', plain):
        if len(part.strip()) > 2:
            c.add(part.strip())
    return {x for x in c if x}


def main():
    a = sys.argv
    objs, src, out = objectives(a[1]), a[2], a[3]
    sessions, blocks, reviewed = collections.defaultdict(set), collections.Counter(), collections.defaultdict(set)
    for p in sorted(glob.glob(os.path.join(src, 'slides_S*.md'))):
        n = int(re.search(r'S(\d+)', os.path.basename(p)).group(1))
        for tag in re.findall(r'- \*\*Objectives:\*\* (.+)', open(p, encoding='utf-8').read()):
            ranged = bool(re.search(r'\d\.\d+\s*[–-]\s*\d\.\d+', tag))
            for o in expand(tag):
                if ranged:
                    reviewed[o].add(n)
                else:
                    sessions[o].add(n); blocks[o] += 1
    quiz = collections.Counter()
    for p in glob.glob(os.path.join(src, 'quiz_S*.json')):
        for q in json.load(open(p, encoding='utf-8')):
            m = re.search(r'\d\.\d+', str(q.get('domain', '')))
            if m:
                quiz[m.group(0)] += 1
    bank = collections.defaultdict(collections.Counter)
    if '--bank' in a:
        for q in json.load(open(a[a.index('--bank') + 1], encoding='utf-8')):
            if q.get('pool') in tuple('ABCD'):
                bank[q['obj']][q['pool']] += 1
    text = ' '.join(open(p, encoding='utf-8').read() for pat in ('script_S*.md', 'handout_S*.md', 'labguide_S*.md')
                    for p in glob.glob(os.path.join(src, pat))).lower()
    text = re.sub(r'\s+', ' ', text)

    sentences = re.split(r'(?<=[.!?|])\s', text)

    def found(item):
        if any(re.search(r'(?<![a-z0-9])' + re.escape(c.lower()) + r'(?![a-z0-9])', text) for c in candidates(item)):
            return True
        # every significant word (by its first five letters) in one sentence
        words = [w[:5] for w in re.findall(r'[a-z0-9.+]+', strip_parens(item).lower()) if len(w) > 2 and w not in STOP]
        return bool(words) and any(all(w in s for w in words) for s in sentences)

    pools = ['A', 'B', 'C', 'D'] if bank else []
    head = '| Objective | Sessions | Teaching blocks | Quiz items | ' + ' | '.join(f'Pool {p}' for p in pools) + (' | ' if pools else '') + 'Sub-bullets matched |'
    L = ['# Objective Coverage Matrix', '',
         f'*Generated by tools/coverage_matrix.py from slide objective tags, nightly quizzes{", practice bank pools" if pools else ""} '
         'and the scripts, handouts and lab guides. Re-run after any content change. Sessions lists the sessions that teach the objective in a tagged block; review sessions whose blocks cover a whole domain are listed once at the end of this table. '
         '"Sub-bullets matched" means the sub-bullet\'s words (or its acronym) appear in a script, handout or lab guide, not that it is fully taught: spot-check low-confidence matches.*', '',
         '## By Objective', '', head, '|' + '---|' * (head.count('|') - 1)]
    missing, gaps = collections.OrderedDict(), []
    for o, d in objs.items():
        miss = [b for b in d['bullets'] if not found(b)]
        if miss:
            missing[o] = miss
        title = d['title'] if len(d['title']) <= 70 else d['title'][:67].rsplit(' ', 1)[0] + '…'
        ss = ', '.join(str(s) for s in sorted(sessions.get(o, []))) or '**none**'
        row = f"| **{o}** {title} | {ss} | {blocks[o]} | {quiz[o]} | "
        row += ''.join(f"{bank[o][p]} | " for p in pools)
        row += f"{len(d['bullets']) - len(miss)} of {len(d['bullets'])} |"
        L.append(row)
        if not sessions.get(o) or blocks[o] == 0 or quiz[o] == 0 or (pools and min(bank[o][p] for p in pools) == 0):
            gaps.append(o)
    rv = sorted({n for v in reviewed.values() for n in v})
    if rv:
        L += ['', f"*Whole-domain review: Session{'s' if len(rv) > 1 else ''} {', '.join(map(str, rv))}.*"]
    L += ['', '## Gaps', '']
    L += [f'- **{o}**: ' + ', '.join(k for k, bad in (('no session', not sessions.get(o)), ('no teaching block', blocks[o] == 0),
                                                   ('no quiz item', quiz[o] == 0),
                                                   ('a pool with no items', bool(pools) and min(bank[o][p] for p in pools) == 0)) if bad)
          for o in gaps] or ['None: every objective has a session, a teaching block, a quiz item' + (' and items in every pool.' if pools else '.')]
    L += ['', '## Sub-Bullets Not Found Word for Word', '',
          '*Most are taught under a different phrasing; check each and either confirm the session or add a sentence.*', '']
    for o, miss in missing.items():
        L += [f'**{o}**', ''] + [f'- {m}' for m in miss] + ['']
    open(out, 'w', encoding='utf-8').write('\n'.join(L))
    total = sum(len(d['bullets']) for d in objs.values())
    print(f'Coverage: {len(objs)} objectives, {total - sum(map(len, missing.values()))} of {total} sub-bullets matched, '
          f'{len(gaps)} objectives with gaps')


if __name__ == '__main__':
    main()
