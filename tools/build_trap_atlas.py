#!/usr/bin/env python3
"""Render the Trap Atlas from the course's extras/traps.tsv.

python3 tools/build_trap_atlas.py extras/traps.tsv extras/domains.tsv OUT.md [--check SRC_DIR]

traps.tsv columns: session, objective (e.g. 2.1, or "skill" for exam-skill traps), topic, trap, why.
domains.tsv columns: domain, name, objectives, weight, sessions.
Writes one table per domain, plus "Exam Skills" first if any rows are tagged skill.
--check SRC_DIR compares the row count per session with the trap paragraphs tools/trap_extract.py
finds in the scripts, and warns where the scripts have more (a trap may be missing from the atlas).
"""
import csv, os, sys, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def read_tsv(p):
    return list(csv.DictReader(open(p, encoding='utf-8'), delimiter='\t'))


def env():
    e = {}
    if os.path.exists('course.env'):
        for ln in open('course.env', encoding='utf-8'):
            if '=' in ln and not ln.startswith('#'):
                k, v = ln.strip().split('=', 1); e[k] = v.strip('"')
    return e


def main():
    a = sys.argv
    traps, doms, out = read_tsv(a[1]), read_tsv(a[2]), a[3]
    E = env()
    bad = [r for r in traps if not all(r.get(k, '').strip() for k in ('session', 'objective', 'topic', 'trap', 'why'))]
    if bad:
        sys.exit(f'traps.tsv: {len(bad)} rows with an empty column, first: {bad[0]}')
    groups = collections.OrderedDict()
    skill = [r for r in traps if r['objective'].lower() == 'skill']
    if skill:
        groups['Exam Skills'] = skill
    for d in doms:
        n = d['domain'][1:]
        rows = [r for r in traps if r['objective'].split('.')[0] == n]
        groups[f"Domain {n}: {d['name']}"] = rows
    placed = sum(len(v) for v in groups.values())
    if placed != len(traps):
        sys.exit(f'traps.tsv: {len(traps) - placed} rows have an objective outside domains.tsv')
    sess = sorted({int(r['session']) for r in traps})
    L = [f"# Trap Atlas: {E.get('COURSE_NAME', '')} {E.get('EXAM', '').split()[-1] if E.get('EXAM') else ''}".rstrip(), '',
         f"*The planted traps taught in Sessions {sess[0]}–{sess[-1]} ({len(traps)}, with repeats listed once), grouped by exam domain. "
         "For each one: the topic, the wrong answer that feels right, and why the question rules it out. "
         "Read a domain the night before its practice-exam review, and cover the right-hand column to test yourself.*", '']
    for name, rows in groups.items():
        rows = sorted(rows, key=lambda r: (int(r['session']), r['objective']))
        L += [f'## {name} ({len(rows)} traps)', '', '| Session | Topic | The Trap | Why It Fails |', '|---|---|---|---|']
        L += [f"| {r['session']} | {r['topic']} | {r['trap']} | {r['why']} |" for r in rows]
        L.append('')
    open(out, 'w', encoding='utf-8').write('\n'.join(L))
    print(f'Trap Atlas: {len(traps)} traps, ' + ', '.join(f'{k.split(":")[0]} {len(v)}' for k, v in groups.items()))
    if '--check' in a:
        from trap_extract import extract
        src = a[a.index('--check') + 1]
        have = collections.Counter(int(r['session']) for r in traps)
        for n in range(1, max(have) + 1):
            found = len(extract(src, n))
            if found > have[n]:
                print(f'  check: Session {n} scripts have {found} trap paragraphs, the atlas has {have[n]} '
                      '(fine if some were merged or are repeats)')


if __name__ == '__main__':
    main()
