# DevLeague Course Kit

One shared kit for every DevLeague course. A course repo holds only its content and three settings files; everything that's the same for every course lives here, so a fix to a tool is made once.

*Repo: `death2norm/devleague-course-kit` (private). In a build chat, attach and clone it next to the course repo (`/home/claude/devleague-course-kit` beside `/home/claude/devleague-<course>`); the course repo's `./setup.sh` finds it there.*

## What's here
| Path | What it is |
|---|---|
| `docs/playbook.md` | Every course-level step, start to finish (plan, build, reviews, bank, hands-on checks, Moodle import, hand-over) |
| `skill/SKILL.md` | The build standard (Production Standard v5), also saved as the devleague-course-builder skill |
| `tools/` | Shared build tools: `rebuild.sh`, `build_s18.sh`, `checks.py`, `qa.py`, `meta.py`, `build_pptx.py`, `build_docx.py`, `build_handout.py` (handout layouts A/B/C), `pdf_check.py` (markdown leftovers, page limit), `gift.py`, `run_sheet.py`, `make_assets.py`, `slidelib.py`, `s18_timing.py` |
| `tools/` (extras) | `build_extras.sh` (all course-level extras), `build_acronyms.py`, `build_pbq_pack.py`, `mixed_reviews.py`, `new_extras.sh` (start a course's extras from the templates) |
| `tools/moodle/` | `moodle_helper.js` (runs Moodle's own forms in Josh's Chrome), `moodle_plan.py` (steps from `moodle.json`), `moodle_reflections.py` (reflection essays and honor statement) |
| `templates/` | `course.env`, `sessions.tsv`, `course_lint.tsv`, `moodle.json` examples; `extras/` templates for the handbook, Week 0, quick starts, acronyms, Mixed Reviews and PBQ Practice Pack (see `templates/extras/README.md`) |
| `assets/` | DevLeague brand images used by every deck and document (logos, shield, dark background); a course can override any of them in its own `assets/` |
| `setup.sh` | `setup.sh <course repo>`: builds the workspace (kit tools and assets, then the course's own on top) |
| `new_course.sh` | Makes a new course repo skeleton |

## A course repo
| Path | What it is |
|---|---|
| `course.env` | PREFIX, COURSE_NAME, DECK_LABEL, EXAM, INSTRUCTOR, WORKSPACE, HANDOUT_STYLE (A, B, C or plain) |
| `moodle.json` | Moodle ids and the extras list for the Moodle tools |
| `extras/` | Course-level extras sources (Phase 5b) and `shots/` screenshots |
| `sessions.tsv` | Per session: lab minutes, debrief minutes, special builder (Session 18) |
| `course_lint.tsv` | Wording that must never appear (stale pass marks, retired facts), checked in every file |
| `src/` | Session sources (`script_SNN.md`, `slides_SNN.md`, `quiz_SNN.json`, keys, lab files, handout, Moodle checklist) |
| `tools/` | Course-only tools: `slides_sNN_gen.py`, `rs_SNN.env` run-sheet overrides |
| `pkt/Student`, `pkt/Instructor` | Packet Tracer files; `rebuild.sh` puts them in the package |
| `bank/` | Practice bank sources and tools |
| `docs/` | Course map, objectives, reviews, final checks, `pitfalls.md`, `<course>_packages.md` |
| `setup.sh` | Finds the kit (`../devleague-course-kit`) and runs its `setup.sh` |

## Daily use
```bash
./setup.sh && cd $WORKSPACE          # once per chat
python3 tools/checks.py              # whole course: FAIL must be fixed, WARN gets a look
tools/rebuild.sh 07                  # one session: checks, then the package (minutes from sessions.tsv), then pdf_check
tools/build_extras.sh                # the course-level extras and their zip
python3 tools/moodle/moodle_plan.py moodle.json   # Moodle steps for the extras
```

## What checks.py looks for (and why)
Every check is a problem a review or audit had to fix by hand on Security+ or Network+:
- **cues:** script slide cues and deck slides match, in order
- **overlap:** a nightly quiz question that copies that night's practice question, lab item or another quiz (about 45 rewritten after the Network+ audit)
- **answers:** keys that are the longest choice by a wide margin, or in more than half the quiz
- **letters:** spoken practice answers bunched on one letter (Network+ S13–S18 were all B)
- **hedges:** unhedged claims about what the exam will do (about 40 hedged after the audit)
- **facts:** anything in `course_lint.tsv` (for example the old 85% voucher wording)
- **keys:** one right answer per question; quiz and key agree on the count
