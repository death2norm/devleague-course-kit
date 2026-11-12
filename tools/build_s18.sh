#!/bin/bash
# Session 18 build (special timing: no quiz, lab or run_sheet.py). Usage: tools/build_s18.sh (or tools/rebuild.sh 18)
# Uses course.env; the course supplies tools/slides_s18_gen.py and the S18 sources.
set -e
cd "${WORKSPACE:-$(cd "$(dirname "$0")/.." && pwd)}"; set -a; . ./course.env; set +a
n=18; B=tools/build_docx.py; P=$PREFIX; T=${TMPDIR_BUILD:-/tmp/claude-0}; mkdir -p $T out/{Instructor,Moodle,Presentation,Student}
python3 tools/checks.py 18 || { [ "$CHECKS" = warn ] && echo "S18: checks failed, building anyway (CHECKS=warn)"; } || exit 1
python3 tools/qa.py src/script_S18.md | tail -1
python3 tools/s18_timing.py src/script_S18.md | tail -4
[ -f tools/slides_s18_gen.py ] && python3 tools/slides_s18_gen.py
python3 tools/make_assets.py icons $(grep -hoE "^\s*icons?:.*" src/slides_S18.md | sed -E "s/^\s*icons?:\s*//" | tr "," " ") >/dev/null
python3 tools/build_pptx.py src/slides_S18.md out/Presentation/${P}_S18_SlideDeck.pptx --script src/script_S18.md --session 18 --instructor "$INSTRUCTOR"
{ printf "# DevLeague $COURSE_NAME · Session 18 · Instructor Script\n\n*Session 18 timing · Briefing 15 · Practice Exam B 90 · Break 10 · Review 45 (8 of the 18 clinics) · Close 20 · Ends 3:00*\n\n---\n\n"; cat src/script_S18.md; } > $T/scr18.md
python3 $B $T/scr18.md out/Instructor/${P}_S18_InstructorScript.docx
python3 $B src/runsheet_S18.md out/Instructor/${P}_S18_RunSheet.docx
python3 $B src/proctoring_S18.md out/Instructor/${P}_S18_ProctoringChecklist.docx
python3 $B src/moodle_S18.md out/Moodle/${P}_S18_MoodleChecklist.docx
python3 $B src/handout_S18.md $T/${P}_S18_StudentHandout.docx --logo --compact
(cd $T && timeout 200 soffice --headless --convert-to pdf --outdir "$OLDPWD/out/Student" ${P}_S18_StudentHandout.docx >/dev/null 2>&1)
cp src/slides_S18.md out/Presentation/${P}_S18_SlideSource.md
rm -rf pkg18 ${P}_S18_Package.zip; mkdir -p pkg18/_build
for d in Instructor Moodle Presentation Student; do mkdir -p pkg18/$d; cp out/$d/${P}_S18_* pkg18/$d/; done
cp -r tools pkg18/_build/; rm -rf pkg18/_build/tools/__pycache__; cp src/*_S18* pkg18/_build/; cp course.env sessions.tsv pkg18/_build/
(cd pkg18 && zip -qr ../${P}_S18_Package.zip .)
echo "S18: $(pdfinfo out/Student/${P}_S18_StudentHandout.pdf | grep Pages)"
