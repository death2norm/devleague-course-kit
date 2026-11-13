"""Fail if a student PDF shows markdown leftovers or runs past its page limit.

python3 tools/pdf_check.py out/Student/NetPlus_S07_StudentHandout.pdf [more.pdf ...] [--pages 2]
Exit 1 on any FAIL. rebuild.sh runs it on every student PDF it makes.

Leftovers caught (each one reached a student at least once):
  backticks (`code` printed literally), **bold** or __bold__ markers, # headings, [text](link) markdown links,
  <!-- comments -->, and table pipes at the start of a line (| a | b |).
Long underscore runs (____) are fill-in blanks and are allowed.
"""
import re, subprocess, sys

PATTERNS = [
    (r'`', 'backtick'),
    (r'\*\*', 'bold marker **'),
    (r'(?<![_\w])__(?=[A-Za-z0-9])|(?<=[A-Za-z0-9])__(?![_\w])', 'bold marker __'),
    (r'^\s*#{1,6} ', 'markdown heading'),
    (r'\]\((?:https?|mailto|/|\.)', 'markdown link'),
    (r'<!--|-->', 'HTML comment'),
    (r'^\s*\|.*\|\s*$', 'table pipes'),
    (r'\[screenshot missing', 'missing screenshot'),
]


def check(pdf, limit=None):
    problems = []
    try:
        text = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True, check=True).stdout
    except Exception as e:
        return [f'FAIL {pdf}: cannot read ({e})']
    for n, line in enumerate(text.split('\n'), 1):
        for pat, name in PATTERNS:
            if re.search(pat, line, re.M):
                problems.append(f'FAIL {pdf}: {name} on line {n}: {line.strip()[:90]}')
    if limit:
        info = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
        m = re.search(r'Pages:\s+(\d+)', info)
        if m and int(m.group(1)) > limit:
            problems.append(f'FAIL {pdf}: {m.group(1)} pages (limit {limit})')
    return problems


if __name__ == '__main__':
    args = sys.argv[1:]; limit = None
    if '--pages' in args:
        i = args.index('--pages'); limit = int(args[i + 1]); del args[i:i + 2]
    out = [p for f in args for p in check(f, limit)]
    print('\n'.join(out) if out else f'pdf_check: {len(args)} file(s) clean')
    sys.exit(1 if out else 0)
