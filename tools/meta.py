"""Print the instructor-script meta line for a session from its built run sheet and script.

python3 tools/meta.py NN LAB_MINUTES
-> "Lab size L (50 min) · Lecture about 88 min · Break 1 after Block 5 · Ends about 2:57"
Run after run_sheet.py has written src/runsheet_SNN.md. No more hunting old chats for the meta line.
"""
import sys, re, subprocess
n, lab = sys.argv[1], int(sys.argv[2])
size = {30: 'S', 40: 'M', 50: 'L'}.get(lab, f'{lab}-minute')
rs = open(f'src/runsheet_S{n}.md', encoding='utf-8').read()
qa = subprocess.run([sys.executable, 'tools/qa.py', f'src/script_S{n}.md'], capture_output=True, text=True).stdout
lec = re.search(r'LECTURE: (\d+) min', qa).group(1)
rows = [r for r in rs.split('\n') if r.startswith('| ')]
blk = None
for i, r in enumerate(rows):
    if '**Break 1**' in r and i > 0:
        m = re.search(r'Block (\d+)', rows[i - 1]); blk = m.group(1) if m else None
end = re.search(r'\| (\d:\d\d) \| \*\*End of published session', rs).group(1)
parts = [f'Lab size {size} ({lab} min)', f'Lecture about {lec} min']
if blk: parts.append(f'Break 1 after Block {blk}')
parts.append(f'Ends about {end}')
print(' · '.join(parts))
