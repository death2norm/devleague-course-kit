"""Mixed Reviews and the Week 3 Checkpoint: check the random-draw plan against the quiz sizes and write the Moodle setup sheet.

python3 tools/mixed_reviews.py extras/mixed_reviews.tsv OUT.md
TSV columns: quiz, section, opens_after, minutes, draws, description
  draws = "1:5 2:5 3:5" (session:number of random questions from that session's quiz category)
  minutes = time limit (blank = none)
Every draw is checked against src/quiz_SNN.json, and the Session 3 category's 2 random questions per later quiz
are left alone (Moodle draws without repeats inside one attempt, so a draw can't exceed the category size).
FAILs stop the build. The setup sheet follows the Security+ Mixed_Review_Setup (course 43).
"""
import csv, json, os, sys

tsv, out = sys.argv[1], sys.argv[2]
NAME = os.environ.get('COURSE_NAME', 'Course'); COURSE = 'DevLeague ' + NAME
rows = list(csv.DictReader(open(tsv, encoding='utf-8'), delimiter='\t'))
size = {}
for n in range(1, 30):
    p = f'src/quiz_S{n:02d}.json'
    if os.path.exists(p): size[n] = len(json.load(open(p, encoding='utf-8')))
fails = []
L = [f'# Mixed Reviews and Week 3 Checkpoint: Moodle Setup ({NAME})', '',
     '*For the Moodle build. Build once in the master course; every cohort copy inherits them. No new questions: every quiz draws at random from the session quiz categories already imported, never from the Practice Bank pools, so the practice exams stay sealed. All are optional practice in the gradebook category Practice (not counted).*', '',
     '## Shared settings', '',
     '- **Grade category:** Practice (not counted), weight 0.',
     '- **Attempts:** unlimited. **Question behaviour:** deferred feedback, shuffle within questions.',
     '- **Review options:** same as the exam-style quizzes (the attempt, whether correct, marks, specific feedback and right answer, immediately after the attempt).',
     '- **Completion:** none. **Open dates:** none in the master; set per cohort if wanted (cohort runbook).',
     f'- **Add questions with:** Questions, Add, a random question, category **{COURSE} / Session NN**, "Include questions from subcategories" off, then the number.', '',
     '| Quiz | Section | Opens after | Time limit | Questions | Random draws (session: number) |', '|---|---|---|---|---|---|']
for r in rows:
    draws = [tuple(int(x) for x in d.split(':')) for d in r['draws'].split()]
    total = sum(k for _, k in draws)
    for s, k in draws:
        if s not in size: fails.append(f"FAIL {r['quiz']}: no quiz for Session {s}")
        elif k > size[s]: fails.append(f"FAIL {r['quiz']}: draws {k} from Session {s}, which has {size[s]}")
    L.append(f"| {r['quiz']} | {r['section']} | Session {r['opens_after']} | {r['minutes'] + ' min' if r['minutes'] else 'none'} | {total} | "
             + ' · '.join(f'S{s}: {k}' for s, k in draws) + ' |')
L += ['', '## Descriptions to paste', '']
L += [f"- **{r['quiz']}:** {r['description']}" for r in rows]
L += ['', f'*Session quiz sizes used for the check: ' + ', '.join(f'S{s} {n}' for s, n in sorted(size.items())) + '.*', '']
open(out, 'w', encoding='utf-8').write('\n'.join(L))
print('\n'.join(fails) if fails else f'mixed reviews: {len(rows)} quizzes, draws fit')
sys.exit(1 if fails else 0)
