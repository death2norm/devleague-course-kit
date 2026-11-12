"""python3 run_sheet.py script.md out.md --lab 30 --debrief 15 --session 01 [--wpm 130]"""
import re, argparse
import os
ap=argparse.ArgumentParser(); ap.add_argument('script'); ap.add_argument('out')
ap.add_argument('--lab',type=int,default=30); ap.add_argument('--debrief',type=int,default=15)
ap.add_argument('--session',default='01'); ap.add_argument('--wpm',type=int,default=130); a=ap.parse_args()
s=open(a.script,encoding='utf-8').read()
secs=re.split(r'\n(?=# )','\n'+s)[1:]
clock=0.0; rows=[]
fmt=lambda m: (lambda r: f"{r//60}:{r%60:02d}")(int(round(m)))
for sec in secs:
    title=sec.split('\n',1)[0][2:].strip(); body=sec.split('\n',1)[1] if '\n' in sec else ''
    if title.startswith('Break 1'):
        rows.append((fmt(clock),'**Break 1**','10','')); clock+=10; continue
    words=len(re.sub(r'\[SLIDE[^\]]*\]|^\*.*\*$','',body,flags=re.M).split())
    q=len(re.findall(r"Let's (?:try|do|run the method)",body)); mins=words/a.wpm+q
    cues=re.findall(r'\[SLIDE ([\w.]+)\]',body)
    rows.append((fmt(clock),title,f"{mins:.0f}",f"{cues[0]}–{cues[-1]}" if cues else '')); clock+=mins
rows.append((fmt(clock),os.environ.get('RS_BREAK2','**Break 2** (students go straight to breakout rooms after it)'),'10','')); clock+=10
rows.append((fmt(clock),os.environ.get('RS_LAB','**Lab** in breakout rooms'),str(a.lab),'')); clock+=a.lab
rows.append((fmt(clock),'**Debrief + Q&A** (main room)',str(a.debrief),'')); clock+=a.debrief
rows.append((fmt(clock),'**End of published session**','',''))
L=[f"# {os.environ.get('COURSE_NAME','Course')} Session {a.session}: Instructor Run Sheet","",f"*Calculated from the script at {a.wpm} words per minute plus 1 minute per practice question. If you're more than 5 minutes behind at Break 1, shorten the Part 2 practice-question pauses. Don't cut a block.*","","| Clock | Section | Min | Slides |","|---|---|---|---|"]
L+=[f"| {c} | {t} | {m} | {sl} |" for c,t,m,sl in rows]
L+=["","## Checkpoints","- **Break 1 starts on time:** within 5 minutes of the clock above.",os.environ.get('RS_LAUNCH',"- **Lab launch:** open breakout rooms the moment Break 2 ends. Same groups every session; 5-minute warning before closing."),"- **Debrief:** call on groups, not individuals. Ask each group which trap they avoided."]
open(a.out,'w').write('\n'.join(L)); print('\n'.join(L[4:]))
