#!/bin/bash
# Build the course-level extras (playbook Phase 5b) from the course repo's extras/ folder.
#   tools/build_extras.sh              everything, then <PREFIX>_CourseExtras_<date>.zip
# Expects in extras/ (start from devleague-course-kit/templates/extras with tools/new_extras.sh):
#   handbook.md  week0_checklist.md  welcome.md  week0_script.md  week0_slides.md  week0_quiz.json
#   quickstart_*.md (+ shots/*.png)  acronyms.tsv  acronyms_back.md  mixed_reviews.tsv  pbq_pack.py
# Output: out/Course/{Student,Instructor,Moodle,Presentation}. Every student PDF goes through pdf_check.py.
set -e
cd "${WORKSPACE:-$(cd "$(dirname "$0")/.." && pwd)}"
set -a; . ./course.env; set +a
P=$PREFIX; X=extras; O=out/Course; T=${TMPDIR_BUILD:-/tmp/claude-0}/extras; B=tools/build_docx.py
rm -rf $O $T; mkdir -p $O/{Student,Instructor,Moodle,Presentation} $T
pdf() { # md -> docx -> pdf in Student (or $3)
  python3 $B "$1" $T/$2.docx --logo --compact
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
# 6. Checks and zip
python3 tools/pdf_check.py $O/Student/*.pdf
cp -r $X $O/_source; rm -rf $O/_source/__pycache__
z=${P}_CourseExtras_$(date +%Y-%m-%d).zip; rm -f $z; (cd $O && zip -qr ../../$z .)
echo "Extras built: $(ls $O/*/* | wc -l) files · $z"
for f in $O/Student/*.pdf; do echo "  $(basename $f): $(pdfinfo $f | awk '/Pages/{print $2}') pages"; done
