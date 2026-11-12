import re, os
T=lambda h,l,li,lk,lm,r,rd: ("two-column",h,f":left-column\n### {l}\nicon: {li}\n- **Key Parameter:** {lk}\n- **Mechanism:** {lm}\n:right-column\n### The Trap\n- **Planted Distractor:** {r}\n- **Why It Fails:** {rd}")
S=lambda h,ic,big,lab,ctx: ("stat-callout",h,f"icon: {ic}\n### {big}\n- **Label:** {lab}\n- **Context:** {ctx}")
F=lambda h,ics,steps: ("horizontal-flow",h,f"icons: {ics}\n"+" ---> ".join(f"[{a}: {b}]" if b else f"[{a}]" for a,b in steps))
D=lambda n,t,o: ("divider",None,f"### {n:02d}\n## {t}"+(f"\n- **Objectives:** {o}" if o else ""))
import os
TITLE=lambda n,sub: ("title",None,f"## {os.environ.get('COURSE_NAME','Course')} Session {n}\n### {sub}\n- **Instructor:** {os.environ.get('INSTRUCTOR','Instructor')}")
Q="circle-question-mark"; TRAP="triangle-exclamation-point"
def write(slides,n):
    out=[]
    for sid,(kind,h,body) in slides:
        out.append(f"<!-- SLIDE {sid} -->")
        if h: out.append(f"## {h}")
        out.append(f":::{kind}\n{body}\n:::\n")
    open(f'src/slides_S{n}.md','w').write("\n".join(out))
    sc=re.findall(r'\[SLIDE ([\w.]+)\]',open(f'src/script_S{n}.md').read()); sl=[x[0] for x in slides]
    print(len(sc),len(sl),"MATCH" if sc==sl else [(a,b) for a,b in zip(sc,sl) if a!=b][:5] or (sc[len(sl):],sl[len(sc):]))
    icons=set()
    for l in open(f'src/slides_S{n}.md'):
        if l.startswith('icon: '): icons.add(l[6:].strip())
        if l.startswith('icons: '): icons|={x.strip() for x in l[7:].split(',')}
    print("missing:",[i for i in icons if not os.path.exists(f'assets/lucide/icons/{i}.svg')])
    open(f'icons_S{n}.txt','w').write(' '.join(sorted(icons)))
