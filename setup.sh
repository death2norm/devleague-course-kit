#!/bin/bash
# Build a workspace for one course: setup.sh /path/to/course-repo (normally called by the course repo's ./setup.sh)
# Copies the kit's shared tools and brand assets first, then the course's own tools/ on top (slide generators,
# run-sheet overrides), then the course's sources, assets, Packet Tracer files and settings.
set -e
K=$(cd "$(dirname "$0")" && pwd); R=$(cd "${1:?usage: setup.sh COURSE_REPO}" && pwd)
set -a; . "$R/course.env"; set +a
W=${WORKSPACE:?WORKSPACE missing from course.env}
mkdir -p $W/{tools,src,assets,pkt,out/{Instructor,Moodle,Presentation,Student}} /tmp/claude-0
cp -r $K/tools/. $W/tools/
[ -d $R/tools ] && cp -r $R/tools/. $W/tools/
cp -r $R/src/. $W/src/
cp -r $K/assets/. $W/assets/
[ -d $R/assets ] && cp -r $R/assets/. $W/assets/
[ -d $R/pkt ] && cp -r $R/pkt/. $W/pkt/
for f in course.env sessions.tsv course_lint.tsv; do [ -f $R/$f ] && cp $R/$f $W/; done
[ -d $W/assets/lucide ] || { git clone -q --depth 1 --filter=blob:none --sparse https://github.com/lucide-icons/lucide.git $W/assets/lucide && git -C $W/assets/lucide sparse-checkout set icons; }
echo "Workspace ready at $W ($COURSE_NAME, kit $(git -C $K rev-parse --short HEAD 2>/dev/null || echo local))"
