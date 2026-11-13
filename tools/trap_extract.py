#!/usr/bin/env python3
"""Pull every planted-trap paragraph out of the session scripts, as a starting point for the Trap Atlas.

python3 tools/trap_extract.py SRC_DIR [--sessions 1-17] > traps_draft.tsv

For each script paragraph that says "Here's the trap", "That's the trap" or "The trap is",
writes one TSV row: session, objectives (from the block divider in slides_SNN.md),
slide id, slide title, paragraph. A person then condenses each row into the course's
extras/traps.tsv (session, objective, topic, trap, why), which tools/build_trap_atlas.py renders.
Re-run after script changes and compare the counts with traps.tsv (build_trap_atlas.py --check does this).
"""
import re, sys, os, glob

TRAP = re.compile(r"\b(here's the trap|that's the trap|the trap is|the trap here|one more trap|another trap|the other trap)\b", re.I)


def slide_map(path):
    """slide id -> (title, objectives of the block it sits in)."""
    out, objs, sid = {}, '', None
    for line in open(path, encoding='utf-8'):
        m = re.match(r'<!-- SLIDE (\S+) -->', line)
        if m:
            sid = m.group(1); out[sid] = ['', objs]; continue
        if sid is None:
            continue
        m = re.match(r'- \*\*Objectives:\*\* (.+)', line.strip())
        if m and sid.startswith('D'):
            objs = m.group(1).strip(); out[sid][1] = objs; continue
        m = re.match(r'##+ (.+)', line)
        if m and not out[sid][0]:
            out[sid][0] = m.group(1).strip()
    return out


def extract(src, n):
    script = os.path.join(src, f'script_S{n:02d}.md')
    slides = os.path.join(src, f'slides_S{n:02d}.md')
    if not (os.path.exists(script) and os.path.exists(slides)):
        return []
    smap = slide_map(slides)
    rows, cur = [], None
    for para in re.split(r'\n\s*\n', open(script, encoding='utf-8').read()):
        for m in re.finditer(r'\[SLIDE (\S+)\]', para):
            cur = m.group(1)
        text = re.sub(r'\[SLIDE \S+\]', '', para).strip()
        if cur and TRAP.search(text):
            title, objs = smap.get(cur, ['', ''])
            rows.append((n, objs, cur, title, ' '.join(text.split())))
    return rows


def main():
    src = sys.argv[1]
    lo, hi = 1, 17
    if '--sessions' in sys.argv:
        a = sys.argv[sys.argv.index('--sessions') + 1].split('-')
        lo, hi = int(a[0]), int(a[-1])
    print('session\tobjectives\tslide\ttitle\tparagraph')
    total = 0
    for n in range(lo, hi + 1):
        for r in extract(src, n):
            print('\t'.join(str(x).replace('\t', ' ') for x in r)); total += 1
    print(f'{total} trap paragraphs', file=sys.stderr)


if __name__ == '__main__':
    main()
