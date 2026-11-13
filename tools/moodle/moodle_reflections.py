"""Moodle XML for the session reflections (3 essays per session, 5 marks each, TA rubric in grader info) and the
practice-exam honor statement (a Description item). Reads the "## Reflection prompts" section of src/moodle_SNN.md.
Moved into the kit Nov 12, 2026 (first used for the Network+ import, course 44).
Run from the workspace: python3 tools/moodle/moodle_reflections.py [OUT.xml]
Uses course.env (COURSE_NAME, PREFIX); RUBRIC_TOPIC env var names the subject in the rubric (default "networking")."""
import re, html, sys, os, glob
src=os.environ.get('SRC','src')
NAME=os.environ.get('COURSE_NAME','Course'); P=os.environ.get('PREFIX','XX'); TOPIC=os.environ.get('RUBRIC_TOPIC','networking')
ID=''.join(c for c in P if c.isupper())[:3] or P[:2].upper()
RUB=("<p><strong>TA rubric (5 points)</strong></p><ul>"
"<li>2 points: answers every part of the prompt.</li>"
f"<li>2 points: the {TOPIC} ideas are correct and use the right terms from the session.</li>"
"<li>1 point: gives a specific example, number or step, not just a general statement.</li></ul>"
"<p>Give a short comment on anything wrong, and point the student to the slide or handout section.</p>")
out=['<?xml version="1.0" encoding="UTF-8"?>','<quiz>']
total=0
sessions=sorted(int(re.search(r'S(\d+)',f).group(1)) for f in glob.glob(f'{src}/moodle_S*.md') if '## Reflection prompts' in open(f).read())
for n in sessions:
    t=open(f'{src}/moodle_S{n:02d}.md').read()
    sec=t.split('## Reflection prompts',1)[1]
    ps=re.findall(r'^>\s*(?:\*\*)?(\d)\.(?:\*\*)?\s*(.+)$',sec,re.M)
    assert len(ps)==3,(n,ps)
    out.append(f'<question type="category"><category><text>$course$/top/DevLeague {NAME}/Reflections/Session {n:02d}</text></category></question>')
    for i,p in ps:
        total+=1
        out.append(f'''<question type="essay"><name><text>S{n:02d} Reflection {i}</text></name>
<questiontext format="html"><text><![CDATA[<p>{html.escape(p.strip())}</p>]]></text></questiontext>
<generalfeedback format="html"><text></text></generalfeedback><defaultgrade>5</defaultgrade><penalty>0</penalty><hidden>0</hidden><idnumber>{ID}-S{n:02d}-R{i}</idnumber>
<responseformat>editor</responseformat><responserequired>1</responserequired><responsefieldlines>10</responsefieldlines>
<minwordlimit></minwordlimit><maxwordlimit></maxwordlimit><attachments>0</attachments><attachmentsrequired>0</attachmentsrequired><maxbytes>0</maxbytes><filetypeslist></filetypeslist>
<graderinfo format="html"><text><![CDATA[{RUB}]]></text></graderinfo><responsetemplate format="html"><text></text></responsetemplate></question>''')
out.append(f'<question type="category"><category><text>$course$/top/DevLeague {NAME}/Practice Exam Admin</text></category></question>')
out.append('''<question type="description"><name><text>Honor statement</text></name><questiontext format="html"><text><![CDATA[<p><strong>Honor statement.</strong> By starting this exam, you agree: "I am completing this practice exam on my own, without notes, other tabs or programs, a phone, AI tools or help from anyone."</p><p>One 90-minute attempt. The timer keeps running if you leave the page. A score more than 20 percentage points above your previous practice exam means a short, friendly call with the program team before a voucher is released. The same rule applies to everyone.</p>]]></text></questiontext><generalfeedback format="html"><text></text></generalfeedback><defaultgrade>0</defaultgrade><penalty>0</penalty><hidden>0</hidden><idnumber>'''+ID+'''-HONOR</idnumber></question>''')
out.append('</quiz>')
open(sys.argv[1] if len(sys.argv)>1 else f'{P}_Reflections_and_Honor.xml','w').write('\n'.join(out))
print(total)
