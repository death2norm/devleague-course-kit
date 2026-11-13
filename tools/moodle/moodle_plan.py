"""Print the Moodle steps for a course's extras from its moodle.json, in the order to run them.

python3 tools/moodle/moodle_plan.py [moodle.json] [--js]
Checks that every file it names exists (run tools/build_extras.sh first) and that the Mixed Review plan's
rows exist. With --js it prints the ML.* calls to paste after loading tools/moodle/moodle_helper.js in Chrome.

Order: 1 question imports (category ids exist only after these) · 2 files and pages · 3 quizzes (create, copy the
model's settings, add questions) · 4 glossary · 5 checks (slot counts, hidden course). Ask Josh before anything that
changes visibility, enrolments, email or site settings.
"""
import csv, json, os, sys

args = [a for a in sys.argv[1:] if not a.startswith('--')]
js = '--js' in sys.argv
cfg = json.load(open(args[0] if args else 'moodle.json', encoding='utf-8'))
C = cfg['course_id']; root = cfg['question_root']
plan = {}
if os.path.exists('extras/mixed_reviews.tsv'):
    plan = {r['quiz']: r for r in csv.DictReader(open('extras/mixed_reviews.tsv', encoding='utf-8'), delimiter='\t')}
missing = []
def need(p):
    if p and not os.path.exists(p): missing.append(p)
    return p

print(f"# Moodle steps for course {C} ({cfg.get('short_name', '')}), model course {cfg.get('model_course_id')}\n")
print('## 1. Question imports (Question bank, Import; "Get category from file" on)')
for e in cfg['extras']:
    if e.get('import'):
        need(e['import'])
        fmt = 'xml' if e['import'].endswith('.xml') else 'gift'
        print(f"- {os.path.basename(e['import'])} -> {root}/{e['category']}")
        if js: print(f"  await ML.importQuestions({C}, ML.file('{os.path.basename(e['import'])}'), '{fmt}')")
print('\n## 2. Files and pages')
for e in cfg['extras']:
    if e['mod'] in ('resource', 'page'):
        src = need(e.get('file') or e.get('html'))
        print(f"- Section {e['section']}: {e['mod']} \"{e['name']}\" from {src}" + (f" (settings like cmid {e['model_cmid']})" if e.get('model_cmid') else ''))
        if js and e['mod'] == 'resource':
            print(f"  await ML.addModule({C}, {e['section']}, 'resource', {{name: '{e['name']}', display: {5 if e.get('display') == 'download' else 0}, 'introeditor[text]': ''}}, {{files: [ML.file('{os.path.basename(src)}')]}})")
print('\n## 3. Quizzes')
for e in cfg['extras']:
    if e['mod'] != 'quiz': continue
    how = ('every question in ' + e['category']) if e.get('fixed_all') else (f"{e['random']} random from {e['category']}" if e.get('random') else '')
    row = plan.get(e.get('plan_row', ''), None)
    if e.get('plan_row') and not row: missing.append('mixed_reviews.tsv row: ' + e['plan_row'])
    if row: how = 'random draws ' + row['draws'] + (f", {row['minutes']} min" if row['minutes'] else '')
    print(f"- Section {e['section']}: \"{e['name']}\" · {how}" + (f" · copy settings from cmid {e['model_cmid']}" if e.get('model_cmid') else '') + (f" · printable {e['printable']}" if e.get('printable') else ''))
    need(e.get('printable'))
print('\n## 4. Glossary')
for e in cfg['extras']:
    if e['mod'] == 'glossary':
        print(f"- Section {e['section']}: \"{e['name']}\" · import {need(e['import_glossary'])} into the current glossary")
print('\n## 5. Checks')
print('- Each quiz shows the right number of slots and categories (ML.slots); random draws come from one session each, no subcategories')
print('- Completion off on practice items; Practice (not counted) grade category; course still hidden')
print('\n## Per cohort (not in the master)')
for p in cfg.get('per_cohort', []): print('- ' + p)
if missing:
    print('\nMISSING:\n' + '\n'.join('  ' + m for m in missing)); sys.exit(1)
