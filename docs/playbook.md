# DevLeague Course Playbook: Every Step, Start to Finish

*Version 2, November 11, 2026 (v2 adds the shared kit, automatic checks, saved build settings and the short handoff). Written from what Security+ (Moodle course 43) and Network+ (N10-009) actually went through. Use it for every new course. Session-level build rules (script, deck, quiz, lab, QA) are in the build standard, `devleague-course-kit/skill/SKILL.md` (saved as the devleague-course-builder skill); this playbook covers the whole course around them.*

## How the work is run

- **Three files per course:**
  - `claude/<course>_handoff.md`: current status only, kept under about 6 KB: state, the status table (one row per session or phase), what's next, the next chat's prompt. Every chat starts with "Read claude/<course>_handoff.md in the test prep project and pick up from there," and ends by updating it.
  - `docs/<course>_history.md` (repo only, to keep project reads small): what happened and why, newest first. Only read when an old detail is needed. When the handoff grows past about 6 KB, move finished sections here.
  - `docs/<course>_packages.md` (repo): one row per session with the zip Josh holds and what it replaced.
- **One shared kit, one repo per course.** The kit (tools, build standard, this playbook, templates) is shared by every course, so a fix is made once. A course repo (for example `death2norm/devleague-netplus`) holds only `src/`, its own `tools/` (slide generators, run-sheet overrides), `pkt/`, `bank/`, `docs/` and three settings files: `course.env`, `sessions.tsv`, `course_lint.tsv`. Brand assets come from the kit (a course can override one in its own `assets/`). In every chat, attach and clone the kit and the course repo side by side in /home/claude; the course's `./setup.sh` builds the workspace. The repos are the source of truth; project copies are backups. A new course starts with `devleague-course-kit/new_course.sh`.
- **Checks that need a person never block a build.** Anything that needs Josh, a TA or the admin (Packet Tracer features, TryHackMe rooms, logo, Moodle version) goes into `docs/<course>_final_checks.md` with exact steps, and the build uses a printed fallback in the meantime.
- **Independent review at every gate.** Each week's plan is reviewed by a fresh agent before Josh sees it, each built week gets a fact-check and coverage check, and the practice bank gets its own review. The reviewer never sees the build chat.
- **Ask Josh first** before anything that emails people or changes Moodle site settings. Josh uploads to Drive himself when the course is done; nothing goes to Drive piecemeal.
- **Documents for others** (Robert, Peter, admins) use plain language, assign work to Josh, and are PDFs, not Claude docs.

## Phase 1: Course plan (one chat, plus approvals)

0. Make the repo skeleton: `devleague-course-kit/new_course.sh <key> <PREFIX> "<Course>" "<DECK LABEL>" "<Exam>"`; Josh creates the empty private GitHub repo and the skeleton is pushed to it.
1. Pull the official exam objectives into `docs/objectives_<exam>.md`; add the sub-bullets (`docs/objectives_<exam>_detail.md`) week by week before each review.
2. Write the course map (`docs/<course>_course_map_v1.md`): constants table (exam facts, prefix, voucher rule, LMS, labs), domain weights, the 18-session map with objectives, lab size (S/M/L) and lab source, practice-bank split per session (25 each, about 425), PBQ types for Session 17, Week 0 additions.
3. Check every lab source: TryHackMe room slugs and free vs. Premium (room database, then the live site in Josh's Chrome); Packet Tracer only where it can actually show the skill.
4. Write the specs one course week (3 sessions) at a time: blocks, Break 1 position, lab artifact, check-first ticket, exam terms, bank split. Independent agent reviews the week's specs; apply fixes; Josh approves.
5. **Lab check before scripts:** as soon as a week's specs are approved, open each assigned TryHackMe task in Josh's Chrome and test each Packet Tracer feature the labs rely on (computer use on Josh's computer). On Network+, these checks came after all 18 sessions and forced rebuilds of eight of them.
6. Put the course's settled facts (pass mark wording, voucher rule, exam facts with the date they were checked) in the course map, and any wording that must never appear in `course_lint.tsv`.

## Phase 2: Build, one session per chat

1. Prompt pattern (keep in the handoff): attach and clone `death2norm/devleague-course-kit` and the course repo side by side in /home/claude, run the course's setup.sh, build Session N with the build standard, copy sources back, commit and push, send the package, update the handoff. Packet Tracer sessions add: write `src/ptbuild_SNN.md`, build the build-sheet docx, mark every [VERSION CHECK] step with a fallback, add new checks to the final checks file.
2. Script timed at 130 words a minute plus 1 minute per practice question; run sheet ends 2:53–2:58; handout 2 pages; deck renders checked.
3. Quiz 10 questions (12 if coverage needs it); from Session 4 on, Moodle adds 2 random questions from the Session 3 category (subnetting/crypto core).
4. Questions: spread practice-question answers across A–D; keep keys from being the longest choice; write the nightly quiz after the script with new scenarios, numbers and choices; then have an agent that hasn't seen the key answer every new item (any disagreement means a rewrite).
5. `python3 tools/checks.py NN` must show 0 FAIL; look at every WARN. `tools/rebuild.sh NN` runs the checks itself, works out the script's meta line, adds the Packet Tracer build sheet and .pkt files, and builds the package. The first build of a session sets its minutes: `tools/rebuild.sh NN 40 20` (saved in `sessions.tsv`).
6. Package name `<Prefix>_SNN_Package_<date>.zip`; a rebuild on the same day becomes `..._<date>b`, then `c`. Update `docs/<course>_packages.md`.
7. **Speed:** once a week's specs are approved, its three session chats can run at the same time. Each touches only its own session's files and updates only its own row in the handoff's status table.

## Phase 3: Weekly review (one chat per course week)

1. Add the week's objective sub-bullets to the detail file.
2. One independent agent fact-checks and coverage-checks scripts, quizzes and keys against those objectives (model: the previous week's `docs/review_weekN.md`). Report sections: MUST FIX, SHOULD FIX, NOTE, coverage gaps.
3. The reviewer also does a "could this story really happen" pass: each story's mechanism traced step by step.
4. Once a week, a second model from another vendor (Grok did this for Network+) audits the same files. On Network+ one end-of-course audit found 76 issues after six weekly reviews; weekly is cheaper than rebuilding all 18 sessions.
5. Apply fixes, rebuild the affected packages, commit, send, update the handoff. Add each mistake the reviewers caught to `docs/pitfalls.md`, and any wording to ban to `course_lint.tsv`. Coverage items that are only taught as traps go to the bank list.

## Phase 4: Session 17 and 18 (course-level sessions)

- Session 17: domain review by weight plus one PBQ simulation per type, groups rotating; PBQs also built as Moodle drag-and-drop items for an optional workshop quiz.
- Session 18: special timing (briefing 15, Practice Exam B 90, break 10, review 45, close 20). The review uses trap clinics mapped to the most-missed questions, never shows Exam B questions. Voucher and policy lines come from `claude/secplus_program_decisions.md` (same rules for every course): pass mark written as marks out of 90 (77 of 90), voucher code by email within 3 business days, camera-failure and lost-time rules.
- Build with `tools/rebuild.sh 18` (the kit's `build_s18.sh`; the course supplies `tools/slides_s18_gen.py`); proctoring checklist for the TA; Moodle checklist with Practice Exam B settings.

## Phase 5: Practice bank and Practice Exams A–D

1. About 425 multiple-choice items (25 per session for Sessions 1–17) plus drag-and-drop, each tagged domain, objective, and (for Pool B) the Session 18 clinic number. Sources in `bank/src/`; build with `bank/tools/build_bank.py`.
2. Four sealed pools, one per exam (A diagnostic before Week 6, B live in Session 18, C and D at home after a study plan). Every pool meets the draw per domain; Pool B items carry the clinic number in the name ("B-D5-014 C15"); no Session 18 clinic practice question, nightly quiz practice question or close copy goes into B, C or D. Items that are only safe in Pool A carry "(A only)".
3. Even out answer lengths (the key is the longest choice in no more than about a third of items, never twice the longest distractor); run the similarity check against every quiz and script question.
4. Independent review of the bank; apply; export Moodle XML and GIFT; zip as `<Prefix>_PracticeBank_<date>.zip`. Any later change re-deals the pools, so only the newest zip is ever imported.

## Phase 6: Hands-on checks (Josh's computer and Chrome)

- **Packet Tracer:** build every starter and finished .pkt from the build sheets with computer use on Josh's computer (Packet Tracer installed and signed in; ask which folder first). Save after each lab, paste configs through the clipboard, record every [VERSION CHECK] Yes/No in the final checks file, apply fallbacks, copy the .pkt files into `pkt/Student` and `pkt/Instructor`, and rebuild those sessions so the .pkt files are inside their packages.
- **TryHackMe:** in Josh's Chrome (he's signed in), open every assigned room, confirm task numbers and titles, confirm free vs. Premium, and start any instructor-demo machine once (then terminate it). Fix lab guides that changed and rebuild those packages.
- **Logo and any other person checks** stay in the final checks file until Josh closes them.

## Phase 7: Moodle import (Josh's Chrome, site admin)

The site is learn.devleague.com (Moodle 4.5, Moove theme). There is no server access, so everything is done through the web interface in Josh's Chrome, signed in as site admin. Security+ is the model: course 43, recorded step by step in `claude/moodle_import_checklist.md`. Start a running checklist for the new course the same way (`claude/<course>_moodle_checklist.md`) and tick items off as they're done.

1. **Site readiness (once per course, read only):** Moodle version (4.3+ needed for per-domain grade items), question types enabled (drag and drop into text, onto image, select missing words, matching, essay, description), upload limit, completion tracking. Don't change site settings without asking Josh.
2. **Master course:** create it hidden, in the DevLeague category, Custom sections, 20 sections (Start Here, Session 01–18 with titles, Practice Exams, Course Resources), completion on. Short name `<COURSE>-MASTER`.
3. **Gradebook:** Lab Completion scale (Incomplete, Complete); categories Labs, Session Quizzes, Reflections, Practice Exams, and Practice (not counted) at weight 0; course and category totals hidden from students; "Calculated weight" and "Contribution to course total" columns hidden.
4. **Question banks:** import every session quiz (GIFT) into its Session category; the four pool XML files into Practice Bank / D1–D5 / Pool A–D; the Session 17 PBQ Workshop XML; reflection essays (3 per session, 5 marks each, TA rubric in grader info); the honor statement as a Description item. Never import per-session bank files, so Pool B stays sealed.
5. **Sections 1–16:** Slides PDF (exported from the .pptx with no speaker notes), Student Handout, Lab assignment (Lab Guide pasted as the description, worksheet attached, .pkt starter attached for Packet Tracer labs, submissions limited per the checklist, Lab Completion scale, Labs category, no dates), Reflection (3 essays, 15 marks, 1 attempt), Exam-Style Quiz (unlimited attempts, shuffle, deferred feedback; plus 2 random from the Session 3 category from Session 4 on).
6. **Sessions 17 and 18, and Practice Exams:** Session 17 adds the PBQ Workshop quiz (optional, ungraded). Practice Exams A–D: 90 minutes, auto-submit, 1 attempt, one per page, free navigation, shuffle, review shows Marks only (plus overall feedback), 90 random slots from the exam's own pool in domain order, maximum grade 90, grade to pass 77.00, overall feedback boundary entered as the mark 77, per-domain grade items on the quiz Grades page. B goes in Session 18 (password set the day before, instructor only); A and D in Practice Exams; C and D hidden, restricted to their candidate groups, honor statement first.
7. **Completion and enrolment:** view for files, submit for labs, an attempt for reflections and PBQ quizzes, a grade for exam-style quizzes, none on practice items. Manual enrolment on; self-enrolment and guest access off; no content change notifications.
8. **Test-student pass:** enrol the test account as Student, use "Log in as," make the course visible only for the test, then check: session materials show, hidden items stay hidden, one quiz attempt scores and shows feedback, a drag-and-drop PBQ saves, a random-draw quiz starts, Practice Exam A shows 90 minutes and 1 attempt, a lab shows "Add submission," the grades page shows no totals. Hide the course again.
9. **Per cohort (later):** copy the master without user data, set dates, Zoom link and schedule, Exam B password the day before Session 18, open and close times for Exams A–D, candidate groups for C and D, recording URLs, course survey link.

**What made the Network+ import fast (Nov 12, about 2 hours):** combine every session GIFT file into one import (the `$CATEGORY` lines keep them apart); import each pool XML separately; make the reflections and honor statement with the course repo's `tools/moodle_reflections.py`; copy each new activity's settings from the matching Security+ activity (course 43) and change only what differs; check the random slots' domain order and the domain grade items after each exam. In Exams C and D, put the honor statement alone in an unshuffled first quiz section, so section shuffle can't move it. Before enrolling the test account, switch off the course's manual-enrolment welcome message and switch it back on afterwards, so no email goes out. "Log in as" ends Josh's admin session: he signs back in before the course is hidden again.

## Phase 8: Hand-over

- Final bundle: every session package (newest letter of each), the practice-bank zip, the final checks file with every item closed or assigned. Josh uploads to Drive.
- The handoff ends with what's left for people (admin, TA, Josh) and nothing left for a build chat.

## Course types (to add as each is needed)

The phases above are written for 18-session certification prep. Other course types reuse the same kit, tools and review steps, with their own time model, assessments and Moodle setup:
- **CPE webinar (NASBA, group internet based):** learning objectives, program level (basic, intermediate, advanced, update or overview), prerequisites, field of study and credits (50 minutes = 1 credit); at least 3 content-related polling questions per credit, with participants told beforehand how many there are and how many they must answer; each participant's response to each poll kept as the attendance record; the evaluation form; certificates with the required fields (templates in `claude/cpe_certificate_templates.md`). A tax subject needs a reviewer who is a CPA, an EA or a tax attorney. To be written up as its own phase list before the first CPE course is built.
- **Short course or workshop:** to be defined.
