---
name: devleague-course-builder
description: Plan, build, fix, review and package DevLeague courses with the shared course kit (Production Standard v5): session scripts, decks, quizzes, labs, run sheets, practice banks and the Moodle import. Use for any DevLeague course work.
---

# DevLeague Course Builder (Production Standard v5)

The shared kit (tools, this standard, the playbook, templates, brand assets) is the repo `death2norm/devleague-course-kit`; attach and clone it next to the course repo in every build chat. Every course repo holds only its content plus `course.env`, `sessions.tsv` and `course_lint.tsv`. Course-level steps (plan, reviews, bank, course-level extras, hands-on checks, Moodle import, per-cohort runbook, hand-over) are in the playbook: `devleague-course-kit/docs/playbook.md` (project copy `claude/devleague_course_playbook.md`). Each course has a short status file `claude/<course>_handoff.md`; read it first in every chat, and read the repo's `docs/<course>_history.md` only when you need an older detail.

## Working agreement (Josh)
- Training is king. Every night is exactly 3:00 published; only student Q&A runs long.
- One chat per session build, one per week's review. Keep chats short. Once a week's specs are approved, its session chats can run at the same time: each writes only its own session's files and adds one line to the handoff's status table.
- Week plans: written, checked by an independent agent, then approved by Josh. After approval, build without more questions.
- After each built week: one independent agent fact-checks and coverage-checks scripts, quizzes and keys against the objectives file (on local disk; subagents can't use the Projects tool), plus a "could this story really happen" pass. Once per week, also run a second-model audit (another vendor's model) on the same files.
- Josh uploads to Drive himself when the course is done. Every course goes into Moodle through Claude in Josh's Chrome (playbook Phase 7). Ask before anything that emails people or changes Moodle site settings.
- Replies: what came out, anything to check, next step, in plain language. End every finished build or review reply with the ready-to-paste prompt for the next chat.
- Documents for others: plain language, work assigned to Josh, no mention of Claude, PDFs for Robert.

## Brand and delivery constants (every course)
| Item | Value |
|---|---|
| Persona | Peter Dunn delivering: a clear, plain-spoken instructor briefing tech peers over Zoom. Any qualified instructor must be able to deliver every script. |
| Brand | DevLeague only on student-facing material. Kingsland University internal only. |
| Palette | Charcoal #4D4D4F/#3A3B3D · Shield teal #1B7A8A · League blue #3AA6D0→#2C5F7C · Amber trap accent #C98A1B · White/#F6F9FA |
| Fonts | Deck: Aptos + Consolas. Docs: Calibri |
| Pace | 130 wpm (recalibrate from live recordings) |
| Schedule | 3 sessions a week, days not fixed: never name a weekday for class |
| Cohort | 20–30, breakout groups of 4–5 (same groups all course), TA co-host |
| LMS | learn.devleague.com, Moodle 4.5, Moove theme |

Course-specific values (exam, prefix, voucher rule, labs) are in the course map and `course.env`.

## Workspace
```bash
./setup.sh                      # in the cloned course repo: kit tools, then course tools on top, into $WORKSPACE (course.env)
cd $WORKSPACE
python3 tools/qa.py src/script_SNN.md                     # after each script chunk: banned filler, block length, timing
python3 tools/make_assets.py icons $(grep -ohE "^icons?: .*" src/slides_SNN.md | cut -d: -f2 | sed 's/,/ /g' | xargs -n1 | sort -u)
python3 tools/checks.py NN                                # automatic checks; FAIL must be fixed
tools/rebuild.sh NN [LAB DEBRIEF]                         # checks, then the whole package; minutes saved in sessions.tsv
```
`rebuild.sh` works out the script's meta line (lab size, lecture minutes, Break 1 block, end time) by itself, adds the Packet Tracer build sheet and the course's `pkt/` files when they exist, and stops on any checks FAIL (`CHECKS=warn` to build anyway). Special sessions name their builder in `sessions.tsv` (Session 18: `build_s18.sh`). After a build, copy changed `src/` and course `tools/` files back to the course repo, commit and push. Name sent zips `<PREFIX>_SNN_Package_<date>.zip` (`b`, `c` for same-day rebuilds) and record them in `docs/<course>_packages.md`.

New course: `devleague-course-kit/new_course.sh <key> <PREFIX> "<Course Name>" "<DECK LABEL>" "<Exam>"` makes the repo skeleton with the three settings files.

## Night model (certification courses)
| Segment | S | M | L |
|---|---|---|---|
| Lecture Part 1 | ~55 | ~50 | ~45 |
| Break 1 / Break 2 | 10 / 10 | 10 / 10 | 10 / 10 |
| Lab (breakouts) | 30 | 40 | 50 |
| Debrief + Q&A | 15 | 20 | 20 |

Lecture minutes = spoken words / 130 + 1 per practice question. Run sheet ends 2:53–2:58. Break 1 at the block boundary nearest 55 min. Session 18 is special (briefing 15, exam 90, break 10, review 45, close 20). Other course types (CPE webinars, short courses) get their own model in the playbook.

## Script rules
- Every spoken word written in full prose; contractions fine; no stage directions or fragments. Italic meta lines (objectives, instructor notes) aren't spoken.
- Instructor-neutral (bio only in the Session 1 swappable intro). US terms; explain each exam term in everyday words the first time.
- Banned filler: delve, tapestry, let's dive, in today's fast-paced, here's a scene, operational baseline (full list in qa.py).
- Block anatomy (10–14 blocks, ~800–1,000 words): everyday analogy → named people in a real office → what broke and the exact setting or command that fixes or shows it → the planted exam trap and why the stem rules it out → "Let's try one" practice question with every choice eliminated.
- Stories must be able to happen: before writing one, trace the mechanism step by step (addresses, routes, ports, timing). If a step depends on a guess, change the story.
- Beliefs about the exam are stated as beliefs ("I'd expect…"). checks.py flags "the exam will…" lines.
- Structure: `# Opening`, `# Block N — Title` + `*Objectives: <exam> x.x*`, `# Break 1`, `# Part 2 Opening — Where We Left Off`, `# Closing — Lab Handoff`. `[SLIDE s.nn]` cues on their own line, matching the deck 1:1.
- Write in 4 chunks (Opening + Blocks 1–3, 4–6, 7–10, 11–13 + close); run qa.py after each and expand any block flagged SHORT.
- Voice (match this register): "Now here's the trap, and I want you to really sit with it. The question is going to say something like... That answer feels comforting. Everybody works there. But being an employee isn't the same as being authorized to see that specific data. If you pick the 'it stayed inside' answer, you've let the drama of the story override the plain fact the question is testing."

## Questions (practice, quiz, bank)
- Spread the right answers: across a session's spoken practice questions, use A, B, C and D roughly evenly (no letter more than half). Decide the letter before writing the choices.
- The right answer is not the longest choice in more than about a third of items, and never by a wide margin; put detail in the feedback, not the key.
- A nightly quiz never reuses that night's practice question or lab item: new scenario, new numbers, new choices. The same skill in a new form is fine (subnetting with new numbers).
- Exactly one defensible right answer. Before sending, an agent that hasn't seen the key answers every new item; any disagreement means a rewrite.
- Quiz: 10 MCQ GIFT (12 where coverage added items); first wrong answer is the planted trap, feedback starts "Trap."; from Session 4 on add 2 random from the Session 3 category. 3 reflection prompts. Practice bank 25/session tagged by domain and objective.

## Slides
```
<!-- SLIDE 2.01 -->            cued slide; script text under [SLIDE 2.01] becomes speaker notes
<!-- SLIDE D03 -->             block divider (no cue); one before each block's first slide
## Headline
:::title | :::divider | :::two-column | :::stat-callout | :::horizontal-flow ... :::
```
- two-column: `:left-column` / `### Title` / `icon: name` / `- **Key Parameter:** ...` / `- **Mechanism:** ...` / `:right-column` / `### The Trap` / `- **Planted Distractor:** ...` / `- **Why It Fails:** ...`
- stat-callout: `icon: name` / `### Big text` / `- **Label:** ...` / `- **Context:** ...` (practice slides: Label `Answer: X`)
- horizontal-flow: `icons: a, b, c` / `[Head: detail] ---> [Head: detail]` (last step = the answer, filled teal)
- divider: `### 03` / `## Block title` / `- **Objectives:** 1.2, 4.6`; break slide = divider with `### 10` / `## Minute Break. Part 2 Starts After It.`
- Icons are current Lucide names (check `assets/lucide/icons/<name>.svg`; for example circle-question-mark, triangle-exclamation-point, funnel not filter). Generators: `tools/slides_sNN_gen.py` with `slidelib.py`; `write(slides,"NN")` checks cues and icons.

## Labs
- Labs: named TryHackMe tasks only (admin 48-hour check), or Packet Tracer with a build sheet; a person or computer use builds the .pkt. One PBQ-style artifact per lab plus a "what would you check first" ticket. Files: LabGuide, LabWorksheet, LabDebriefKey.
- Check the lab before writing the script: when a week's specs are approved, open each TryHackMe room and task in Josh's Chrome and test each Packet Tracer feature the lab needs. Write anything that needs a person into `docs/<course>_final_checks.md` with a printed fallback; builds never wait on it.
- Lab steps, worksheets and debrief keys must match the script after any fix.

## Session spec template (approved per course week)
```
Session N: Title · Objectives · Lab size
Lab: room (free/P) and tasks, or Packet Tracer; est. minutes; artifact; check-first ticket
Blocks (10–14): analogy · office story · what broke · control or command · trap · practice question focus
Break 1 after Block X (closest to 55 min)
Callbacks · Exam terms to explain · Practice bank contribution (25 Q: domain/objective)
```

## Files per session (rebuild.sh makes them)
| Folder | Files |
|---|---|
| Instructor | InstructorScript, RunSheet, LabDebriefKey, QuizKey (.docx); PacketTracer_BuildSheet and Finished .pkt when used |
| Presentation | SlideDeck.pptx (notes = script), SlideSource.md |
| Student | StudentHandout.pdf (≤ 2 pages, built by build_handout.py in the course's HANDOUT_STYLE; B = cheat sheet with the check-yourself line), LabGuide.pdf, LabWorksheet.docx; Starter .pkt when used |
| Moodle | MoodleChecklist.docx, Quiz.gift.txt |
| _build | tools, the session's sources, course.env, sessions.tsv |

## QA gates (all before sending)
checks.py 0 FAIL (WARNs looked at) · qa.py PASS on the script and every .md · pdf_check.py clean (no markdown leftovers) and handout ≤ 2 pages · render and look at 6 sample slides · run sheet ends 2:53–2:58 · GIFT one `=` and three `~` per question.

## Course pitfalls
Each course keeps the mistakes its reviewers caught in `docs/pitfalls.md`; read it before writing a script. Add to it after every review. Forbidden stale wording (old pass marks, retired facts) goes into `course_lint.tsv`, so checks.py catches it everywhere.
