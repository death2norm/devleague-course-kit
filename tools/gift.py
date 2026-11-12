"""python3 gift.py quiz.json out.gift.txt key.md --session 01 [--course "DevLeague <course>" (default: DevLeague $COURSE_NAME)] [--category X]"""
import json, argparse
ap=argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('gift'); ap.add_argument('key')
ap.add_argument('--session',default='01'); import os
ap.add_argument('--course',default='DevLeague '+os.environ.get('COURSE_NAME','Course')); ap.add_argument('--category')
a=ap.parse_args(); Q=json.load(open(a.src,encoding='utf-8'))
cat=a.category or f"{a.course}/Session {a.session}"
esc=lambda t: ''.join('\\'+c if c in '\\~=#{}:' else c for c in t)
out=[f"$CATEGORY: {cat}",""]
for i,q in enumerate(Q,1):
    assert sum(1 for x in q['answers'] if x[1])==1, f"Q{i} needs exactly one correct answer"
    assert len(q['answers'])==4, f"Q{i} needs 4 answers"
    out.append(f"::N{a.session}-Q{i:02d} {esc(q['title'])}::{esc(q['stem'])} {{")
    out+= [f"\t{'=' if ok else '~'}{esc(t)}#{esc(fb)}" for t,ok,fb in q['answers']]
    out.append("}\n")
open(a.gift,'w',encoding='utf-8').write("\n".join(out))
L=[f"# {os.environ.get('COURSE_NAME','Course')} Session {a.session} Quiz: Instructor Key and Trap Breakdown","","*Internal only. Students see the same feedback in Moodle after each attempt.*",""]
for i,q in enumerate(Q,1):
    c=next(x for x in q['answers'] if x[1]); t=next(x for x in q['answers'] if not x[1])
    L+=[f"## Q{i}. {q['title']} ({q.get('domain','')})",q['stem'],f"- **Correct:** {c[0]}",f"- **Planted trap:** {t[0]}",f"- **Why it's wrong:** {t[2].replace('Trap. ','')}",""]
open(a.key,'w',encoding='utf-8').write("\n".join(L)); print(len(Q),"questions written")
