#!/bin/bash
# Build the course-level extras (playbook Phase 5b) from the course repo's extras/ folder.
#   tools/build_extras.sh              everything, then <PREFIX>_CourseExtras_<date>.zip
# Expects in extras/ (start from devleague-course-kit/templates/extras with tools/new_extras.sh):
#   handbook.md  week0_checklist.md  welcome.md  week0_script.md  week0_slides.md  week0_quiz.json
#   quickstart_*.md (+ shots/*.png)  acronyms.tsv  acronyms_back.md  mixed_reviews.tsv  pbq_pack.py
#   domains.tsv  traps.tsv  cheat_sheets.md  after_the_exam.md  instructor_guide.md  objectives.md
# The full list, and what each one is for, is in templates/extras/README.md. A missing file is reported at
# the start (Security+ parity check) and its step is skipped, so nothing ships without someone noticing.
# Output: out/Course/{Student,Instructor,Moodle,Presentation}. Every student PDF goes through pdf_check.py.
set -e
cd "${WORKSPACE:-$(cd "$(dirname "$0")/.." && pwd)}"
set -a; . ./course.env; set +a
P=$PREFIX; X=extras; O=out/Course; T=${TMPDIR_BUILD:-/tmp/claude-0}/extras; B=tools/build_docx.py
rm -rf $O $T; mkdir -p $O/{Student,Instructor,Moodle,Presentation} $T
# 0. Completeness: every course ships the same course-level set as Security+ (playbook Phase 5b)
miss=0; for f in handbook.md week0_checklist.md welcome.md week0_script.md week0_slides.md week0_quiz.json \
  acronyms.tsv acronyms_back.md mixed_reviews.tsv pbq_pack.py domains.tsv traps.tsv cheat_sheets.md \
  after_the_exam.md instructor_guide.md objectives.md; do [ -f $X/$f ] || { echo "MISSING extras/$f"; miss=1; }; done
ls $X/quickstart_*.md >/dev/null 2>&1 || { echo "MISSING extras/quickstart_*.md"; miss=1; }
left=$(grep -l '{{' $X/*.md $X/*.tsv $X/*.json 2>/dev/null || true)
[ -n "$left" ] && { echo "WARNING: template placeholders {{ }} still in: $left"; miss=1; }
[ $miss = 0 ] && echo "Extras complete: all course-level items present" || echo "WARNING: course-level extras missing or unfinished (see above)"
pdf() { # md -> docx -> pdf in Student (or $3); $4 = --tight for one-page reference sheets
  python3 $B "$1" $T/$2.docx --logo ${4:---compact}
  (cd $T && timeout 200 soffice --headless --convert-to pdf $2.docx >/dev/null 2>&1); cp $T/$2.pdf $O/${3:-Student}/; }
# 1. Start Here
pdf $X/handbook.md ${P}_Student_Handbook
pdf $X/week0_checklist.md ${P}_Week0_Checklist
python3 -c "import markdown,sys;print(markdown.markdown(open(sys.argv[1]).read(),extensions=['tables']))" $X/welcome.md > $O/Moodle/${P}_Welcome_Page.html
for q in $X/quickstart_*.md; do n=$(basename $q .md | sed 's/quickstart_//'); cp -r $X/shots $T/ 2>/dev/null || true
  cp $q $T/; pdf $T/$(basename $q) ${P}_QuickStart_${n}; done
for f in pkt/Student/${P}_W0_*.pkt; do [ -f "$f" ] && cp "$f" $O/Student/; done
# 2. Week 0 orientation
python3 tools/qa.py $X/week0_script.md | tail -1 || true
python3 tools/build_pptx.py $X/week0_slides.md $O/Presentation/${P}_Week0_Orientation.pptx --script $X/week0_script.md --session 00 --label "WEEK 0 ORIENTATION" --instructor "$INSTRUCTOR"
{ printf "# DevLeague $COURSE_NAME · Week 0 Orientation · Instructor Script\n\n*About 60 minutes · live on Zoom before Session 1*\n\n---\n\n"; cat $X/week0_script.md; } > $T/w0.md
python3 $B $T/w0.md $O/Instructor/${P}_Week0_InstructorScript.docx
python3 tools/gift.py $X/week0_quiz.json $O/Moodle/${P}_Week0_WarmUp.gift.txt $T/w0key.md --session W0 --category "\$course\$/top/DevLeague $COURSE_NAME/Week 0 Warm-Up" >/dev/null
python3 $B $T/w0key.md $O/Instructor/${P}_Week0_WarmUp_Key.docx
# 3. Acronyms
python3 tools/build_acronyms.py $X/acronyms.tsv $T --back $X/acronyms_back.md
cp $T/${P}_Acronym_Glossary.moodle.xml $T/${P}_Acronym_Drills.gift.txt $O/Moodle/; cp $T/${P}_Acronym_Flashcards.csv $O/Student/
pdf $T/${P}_Acronym_Glossary.md ${P}_Acronym_Glossary
# 4. Mixed Reviews and Checkpoint (fails if a draw is bigger than a session's quiz)
python3 tools/mixed_reviews.py $X/mixed_reviews.tsv $T/${P}_MixedReview_Setup.md
python3 $B $T/${P}_MixedReview_Setup.md $O/Moodle/${P}_MixedReview_Setup.docx
# 5. PBQ Practice Pack
python3 tools/build_pbq_pack.py $X/pbq_pack.py $T
cp $T/${P}_PBQ_Practice_Pack.moodle.xml $O/Moodle/
pdf $T/${P}_PBQ_Practice_Pack.md ${P}_PBQ_Practice_Pack
python3 $B $T/${P}_PBQ_Practice_Pack_Key.md $O/Instructor/${P}_PBQ_Practice_Pack_Key.docx
# 6. Study aids: Domain Cheat Sheets, Trap Atlas, After the Exam
if [ -f $X/cheat_sheets.md ]; then pdf $X/cheat_sheets.md ${P}_Domain_Cheat_Sheets Student --tight
  n=$(pdfinfo $O/Student/${P}_Domain_Cheat_Sheets.pdf | awk '/Pages/{print $2}'); d=$(($(wc -l < $X/domains.tsv) - 1))
  [ "$n" = "$d" ] || echo "WARNING: Domain Cheat Sheets are $n pages for $d domains; trim until each domain fits one page"; fi
if [ -f $X/traps.tsv ] && [ -f $X/domains.tsv ]; then
  python3 tools/build_trap_atlas.py $X/traps.tsv $X/domains.tsv $T/${P}_Trap_Atlas.md --check src
  pdf $T/${P}_Trap_Atlas.md ${P}_Trap_Atlas; fi
[ -f $X/after_the_exam.md ] && pdf $X/after_the_exam.md ${P}_After_The_Exam
# 7. Staff: Instructor and TA Guide, Objective Coverage Matrix
[ -f $X/instructor_guide.md ] && python3 $B $X/instructor_guide.md $O/Instructor/${P}_Instructor_TA_Guide.docx
if [ -f $X/objectives.md ]; then
  bank=""; [ -n "$BANK_ITEMS" ] && [ -f "$BANK_ITEMS" ] && bank="--bank $BANK_ITEMS"
  [ -n "$BANK_ITEMS" ] && [ -z "$bank" ] && echo "WARNING: BANK_ITEMS=$BANK_ITEMS not found; build the bank first for pool columns"
  python3 tools/coverage_matrix.py $X/objectives.md src $T/${P}_Coverage_Matrix.md $bank
  python3 $B $T/${P}_Coverage_Matrix.md $O/Instructor/${P}_Coverage_Matrix.docx; fi
# 8. Checks and zip
python3 tools/pdf_check.py $O/Student/*.pdf
cp -r $X $O/_source; rm -rf $O/_source/__pycache__
z=${P}_CourseExtras_$(date +%Y-%m-%d).zip; rm -f $z; (cd $O && zip -qr ../../$z .)
echo "Extras built: $(ls $O/*/* | wc -l) files · $z"
for f in $O/Student/*.pdf; do echo "  $(basename $f): $(pdfinfo $f | awk '/Pages/{print $2}') pages"; done
