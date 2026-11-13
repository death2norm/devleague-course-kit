#!/bin/bash
# Start a course's extras/ folder from the kit templates (playbook Phase 5b).
#   devleague-course-kit/tools/new_extras.sh /home/claude/devleague-<course>
# Fills {{COURSE_NAME}} {{EXAM_CODE}} {{PREFIX}} {{DECK_COURSE}} {{SUPPORT_EMAIL}} {{WEBSITE}} from the course's course.env
# (SUPPORT_EMAIL and WEBSITE default to support@devleague.com and devleague.com). Won't overwrite an existing file.
# Then rewrite every course-specific part: see templates/extras/README.md for the list.
set -e
K=$(cd "$(dirname "$0")/.." && pwd); R=$(cd "${1:?usage: new_extras.sh COURSE_REPO}" && pwd)
set -a; . "$R/course.env"; set +a
EXAM_CODE=${EXAM_CODE:-${EXAM##* }}; DECK_COURSE=${DECK_COURSE:-${DECK_LABEL%% *}}
SUPPORT_EMAIL=${SUPPORT_EMAIL:-support@devleague.com}; WEBSITE=${WEBSITE:-devleague.com}
mkdir -p "$R/extras/shots"
for f in "$K"/templates/extras/*; do
  b=$(basename "$f"); [ "$b" = README.md ] && continue; d="$R/extras/${b/.example/}"
  [ -e "$d" ] && { echo "keep  $d"; continue; }
  sed -e "s/{{COURSE_NAME}}/$COURSE_NAME/g; s/{{EXAM_CODE}}/$EXAM_CODE/g; s/{{PREFIX}}/$PREFIX/g; s/{{DECK_COURSE}}/$DECK_COURSE/g; s/{{SUPPORT_EMAIL}}/$SUPPORT_EMAIL/g; s/{{WEBSITE}}/$WEBSITE/g" "$f" > "$d"
  echo "made  $d"
done
[ -f "$R/moodle.json" ] || { cp "$K/templates/moodle.json.example" "$R/moodle.json"; echo "made  $R/moodle.json (fill in the ids)"; }
echo "Next: rewrite the course-specific parts (templates/extras/README.md), take the screenshots, then tools/build_extras.sh"
