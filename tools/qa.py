"""QA lint: python3 qa.py script.md"""
import sys,re
EXAM_TERMS=["control plane","bollard","pdu","encapsulation","mtu"]
BANNED=["operational baseline","remediation plane","fault line of the scene","identity state","system baseline","structural boundaries","four kinds","the five as you'll use them","letter from what happened","and one more on time","soft spot into identity","here's a scene","distribution loop","delve","tapestry","in today's fast-paced","let's dive"]
MIN_BLOCK=650
s=open(sys.argv[1],encoding='utf-8').read()
low=s.lower(); bad=0
for b in BANNED:
    n=low.count(b)
    if n: print(f"BANNED '{b}': {n}"); bad+=1
for b in re.split(r'\n(?=# )',s):
    t=b.split('\n',1); w=len(re.sub(r'\[SLIDE[^\]]*\]|\*Objectives[^\n]*','',t[1] if len(t)>1 else '').split())
    flag='' if (w>=MIN_BLOCK or not t[0].startswith('# Block')) else '  <-- SHORT'
    print(f"{w:5d}  {t[0][2:60]}{flag}")
for t in EXAM_TERMS:
    if t in low: print(f"EXAM TERM (check it's explained): '{t}' x{low.count(t)}")
strip=lambda x: re.sub(r'\[SLIDE[^\]]*\]|\*[^\n]*\*$|^#.*$','',x,flags=re.M).split()
spoken=len(strip(s)); pauses=len(re.findall(r"Let's (?:try|do|run the method)",s))
parts=re.split(r'\n# Break 1',s)
if len(parts)==2:
    for name,p in zip(("Part 1","Part 2"),parts):
        w=len(strip(p)); q=len(re.findall(r"Let's (?:try|do|run the method)",p))
        print(f"{name}: {w} words + {q} pauses = {w/130+q:.0f} min")
print(f"LECTURE: {spoken/130+pauses:.0f} min ({spoken} words @130 + {pauses} x 1-min pauses)")
print("RESULT:","FAIL" if bad else "PASS")
