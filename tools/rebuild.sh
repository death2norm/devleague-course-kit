#!/bin/bash
# Rebuild one session package from the workspace sources.
#   tools/rebuild.sh NN            lab/debrief minutes come from sessions.tsv
#   tools/rebuild.sh NN 50 20      override (and save) the lab/debrief minutes
# Settings: course.env (PREFIX, COURSE_NAME, DECK_LABEL, EXAM, INSTRUCTOR, WORKSPACE, HANDOUT_STYLE) in the workspace root.
# HANDOUT_STYLE: A polished, B cheat sheet (default), C study guide (tools/build_handout.py), or plain (build_docx.py, the pre-Nov 12 look).
# Special sessions (sessions.tsv "builder" column, e.g. build_s18.sh) are handed to their own script.
# The automatic checks run first; any FAIL stops the build (CHECKS=warn to build anyway and see the list).
set -e
n=$1
cd "${WORKSPACE:-$(cd "$(dirname "$0")/.." && pwd)}"
set -a; . ./course.env; set +a
B=tools/build_docx.py; P=$PREFIX; T=${TMPDIR_BUILD:-/tmp/claude-0}; mkdir -p $T out/{Instructor,Moodle,Presentation,Student}
row=$(awk -F'\t' -v s="$n" '$1==s' sessions.tsv)
lab=${2:-$(echo "$row" | cut -f2)}; deb=${3:-$(echo "$row" | cut -f3)}; builder=$(echo "$row" | cut -f4)
if [ -n "$builder" ] && [ -z "$2" ]; then exec bash tools/$builder; fi
[ -z "$lab" ] && { echo "S$n: no lab/debrief minutes in sessions.tsv; run tools/rebuild.sh $n LAB DEBRIEF once"; exit 1; }
if [ -n "$2" ]; then  # save new minutes
  python3 - "$n" "$lab" "$deb" <<'EOF'
import sys
n, lab, deb = sys.argv[1:]
rows = [r.split('\t') for r in open('sessions.tsv').read().rstrip('\n').split('\n')]
hit = False
for r in rows:
    if r[0] == n: r[1:3] = [lab, deb]; hit = True
if not hit: rows.append([n, lab, deb, ''])
open('sessions.tsv', 'w').write('\n'.join('\t'.join(r) for r in rows) + '\n')
EOF
fi
python3 tools/checks.py $n || { [ "$CHECKS" = warn ] && echo "S$n: checks failed, building anyway (CHECKS=warn)"; } || exit 1
[ -f tools/rs_S$n.env ] && . tools/rs_S$n.env
python3 tools/build_pptx.py src/slides_S$n.md out/Presentation/${P}_S${n}_SlideDeck.pptx --script src/script_S$n.md --session $n --instructor "$INSTRUCTOR"
python3 tools/gift.py src/quiz_S$n.json out/Moodle/${P}_S${n}_Quiz.gift.txt src/quiz_key_S$n.md --session $n >/dev/null
python3 tools/run_sheet.py src/script_S$n.md src/runsheet_S$n.md --lab $lab --debrief $deb --session $n >/dev/null
meta=$(python3 tools/meta.py $n $lab)
{ printf "# DevLeague $COURSE_NAME · Session ${n#0} · Instructor Script\n\n*$meta*\n\n---\n\n"; cat src/script_S$n.md; } > $T/scr$n.md
python3 $B $T/scr$n.md out/Instructor/${P}_S${n}_InstructorScript.docx
python3 $B src/runsheet_S$n.md out/Instructor/${P}_S${n}_RunSheet.docx
python3 $B src/debriefkey_S$n.md out/Instructor/${P}_S${n}_LabDebriefKey.docx
python3 $B src/quiz_key_S$n.md out/Instructor/${P}_S${n}_QuizKey.docx
python3 $B src/moodle_S$n.md out/Moodle/${P}_S${n}_MoodleChecklist.docx
[ -f src/ptbuild_S$n.md ] && python3 $B src/ptbuild_S$n.md out/Instructor/${P}_S${n}_PacketTracer_BuildSheet.docx
python3 $B src/worksheet_S$n.md out/Student/${P}_S${n}_LabWorksheet.docx --logo --compact
HS=${HANDOUT_STYLE:-B}; HC=${HANDOUT_COURSE:-${EXAM#CompTIA }}
if [ "$HS" = plain ]; then python3 $B src/handout_S$n.md $T/${P}_S${n}_StudentHandout.docx --logo --compact
else python3 tools/build_handout.py src/handout_S$n.md $T/${P}_S${n}_StudentHandout.docx --style $HS --course "$HC" --session $((10#$n)); fi
python3 $B src/labguide_S$n.md $T/${P}_S${n}_LabGuide.docx --logo --compact
(cd $T && timeout 200 soffice --headless --convert-to pdf --outdir "$OLDPWD/out/Student" ${P}_S${n}_StudentHandout.docx ${P}_S${n}_LabGuide.docx >/dev/null 2>&1)
for d in Student Instructor; do for f in pkt/$d/${P}_S${n}_*.pkt; do [ -f "$f" ] && cp "$f" out/$d/; done; done
cp src/slides_S$n.md out/Presentation/${P}_S${n}_SlideSource.md
rm -rf pkg$n ${P}_S${n}_Package.zip; mkdir -p pkg$n/_build
for d in Instructor Moodle Presentation Student; do mkdir -p pkg$n/$d; cp out/$d/${P}_S${n}_* pkg$n/$d/; done
cp -r tools pkg$n/_build/; rm -rf pkg$n/_build/tools/__pycache__; cp src/*_S$n* pkg$n/_build/; cp course.env sessions.tsv pkg$n/_build/
(cd pkg$n && zip -qr ../${P}_S${n}_Package.zip .)
pages=$(pdfinfo out/Student/${P}_S${n}_StudentHandout.pdf 2>/dev/null | awk '/Pages/{print $2}')
echo "S$n built: $meta · handout $pages pages (style ${HS}) · ${P}_S${n}_Package.zip"
python3 tools/pdf_check.py out/Student/${P}_S${n}_LabGuide.pdf || exit 1
python3 tools/pdf_check.py out/Student/${P}_S${n}_StudentHandout.pdf --pages 2 || exit 1
