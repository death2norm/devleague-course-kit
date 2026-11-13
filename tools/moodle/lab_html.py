"""Lab guides as clean HTML for the Moodle assignment descriptions (one JSON file, session number -> HTML).

python3 tools/moodle/lab_html.py [OUT.json]      (from the workspace; reads src/labguide_SNN.md)
Drops the "# Title" line (the activity already has the name), puts a blank line before every list and table so
markdown sees them (pasting raw markdown flattened the lists on Nov 12), and uses h3 for the section headings.
In Chrome, read the JSON through the helper's file input and set each lab's introeditor[text] with ML.update;
the worksheet and .pkt attachments are a separate field and stay as they are.
"""
import glob, json, re, sys
import markdown

out = {}
for f in sorted(glob.glob('src/labguide_S*.md')):
    n = int(re.search(r'S(\d+)', f).group(1))
    lines = open(f, encoding='utf-8').read().split('\n')
    if lines and lines[0].startswith('# '): lines = lines[1:]
    fixed = []
    for l in lines:
        is_list = bool(re.match(r'^\s*([-*]|\d+\.)\s', l)); is_tbl = l.startswith('|')
        prev = fixed[-1] if fixed else ''
        if (is_list and prev.strip() and not re.match(r'^\s*([-*]|\d+\.)\s', prev)) or (is_tbl and prev.strip() and not prev.startswith('|')):
            fixed.append('')
        fixed.append(l)
    html = markdown.markdown('\n'.join(fixed), extensions=['tables', 'sane_lists'])
    out[n] = html.replace('<table>', '<table class="table table-bordered">').replace('<h2>', '<h3>').replace('</h2>', '</h3>')
dest = sys.argv[1] if len(sys.argv) > 1 else 'out/lab_descriptions.json'
json.dump(out, open(dest, 'w', encoding='utf-8'))
print(f'{len(out)} lab descriptions -> {dest}')
