#!/bin/bash
# Start a new course repo skeleton next to this kit.
#   devleague-course-kit/new_course.sh cysaplus CySAPlus "CySA+" "CYSA+ CS0-004" "CompTIA CySA+ CS0-004" [instructor]
# Then: create an empty private GitHub repo devleague-<key>, push this folder to it, attach it in a chat.
set -e
K=$(cd "$(dirname "$0")" && pwd)
key=${1:?key}; P=${2:?prefix}; name=${3:?course name}; deck=${4:?deck label}; exam=${5:?exam}; inst=${6:-Peter Dunn}
D=${DEST:-$(dirname "$K")/devleague-$key}; mkdir -p "$D"/{src,docs,tools,assets,pkt/Student,pkt/Instructor,bank/src}
cat > "$D/course.env" <<EOT
# Course settings read by every kit tool (bash \`source\`-able; KEY="value" only)
PREFIX="$P"
COURSE_NAME="$name"
DECK_LABEL="$deck"
EXAM="$exam"
INSTRUCTOR="$inst"
WORKSPACE="/home/claude/$key"
HANDOUT_STYLE="B"
EOT
printf 'session\tlab\tdebrief\tbuilder\n18\t\t\tbuild_s18.sh\n' > "$D/sessions.tsv"
cp "$K/templates/course_lint.tsv.example" "$D/course_lint.tsv"
cat > "$D/setup.sh" <<'EOT'
#!/bin/bash
set -e
R=$(cd "$(dirname "$0")" && pwd)
for K in "$R/kit" "$R/../devleague-course-kit"; do [ -x "$K/setup.sh" ] && exec "$K/setup.sh" "$R"; done
echo "Course kit not found: attach and clone death2norm/devleague-course-kit next to this repo"; exit 1
EOT
chmod +x "$D/setup.sh"
printf '# %s pitfalls (mistakes reviewers caught; read before writing a script)\n\n' "$name" > "$D/docs/pitfalls.md"
printf '# %s packages Josh holds\n\n| Session | Current zip | Replaces | Why |\n|---|---|---|---|\n' "$name" > "$D/docs/${key}_packages.md"
echo "New course skeleton at $D. Next: objectives file, course map (playbook Phase 1)."
