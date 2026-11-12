"""Session 18 timing check: python3 tools/s18_timing.py src/script_S18.md
Spoken words / 130 + 1 min per practice question, by section. Session 18 doesn't use run_sheet.py (special timing)."""
import re,sys
s=open(sys.argv[1],encoding='utf-8').read(); out={}
for sec in re.split(r'\n(?=# )','\n'+s)[1:]:
    t,b=sec.split('\n',1); w=len(re.sub(r'\[SLIDE[^\]]*\]|^\*.*\*$','',b,flags=re.M).split()); q=len(re.findall(r"Let's try one",b))
    out[t[2:]]=(w,w/130+q); print(f"{w:5d} words  {w/130+q:5.1f} min  {t[2:]}")
g=lambda k: sum(v[1] for t,v in out.items() if t.startswith(k))
cl=[v[1] for t,v in out.items() if t.startswith('Clinic')]
print(f"Briefing spoken {g('Briefing'):.1f} min (+ about 3.5 min of setup actions = {g('Briefing')+3.5:.1f}; budget 15)")
print(f"Clinics: {len(cl)} written, average {sum(cl)/len(cl):.1f} min; 8 taught = {8*sum(cl)/len(cl):.1f} min (longest 8: {sum(sorted(cl)[-8:]):.1f})")
r=g('Review'); print(f"Review spoken {r:.1f} + 8 clinics {8*sum(cl)/len(cl):.1f} + miss-rate lines 1.5 + Q&A 8 = {r+8*sum(cl)/len(cl)+9.5:.1f} (budget 45)")
c=g('Close'); print(f"Close spoken {c:.1f} + survey 5 + Q&A = 20 -> Q&A {20-5-c:.1f} min")
