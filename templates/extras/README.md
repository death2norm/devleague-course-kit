# Course-level extras: templates

`tools/new_extras.sh <course repo>` copies these into the course's `extras/` and fills the placeholders. They start as the Network+ versions (Nov 12–13, 2026), which were built from the Security+ originals (course 43) and updated to the Nov 5 and Nov 11 program decisions. Build with `tools/build_extras.sh`; the PDF check fails on any leftover `{{ }}` placeholder, markdown or missing screenshot, and the build lists any missing file or file still holding a placeholder (a `{{REWRITE: …}}` line marks a file that must be rewritten for the course, not just filled in).

**The set is the Security+ set.** Security+ (course 43) shipped all of these; Network+ first missed the last five rows and had to add them on Nov 13. Every course gets every row.

| File | What to change for a new course |
|---|---|
| `handbook.md` | Tools table (which lab platforms), "What you need" (computer requirements for the lab software), the exam facts (questions, minutes, passing score), the Packet Tracer lines. Policies stay as they are unless Josh changes them for every course (`claude/secplus_program_decisions.md`). |
| `week0_checklist.md` | Section 2 (the course's lab tool setup) and the warm-up topic |
| `welcome.md` | Usually nothing; the cohort table is filled per cohort |
| `week0_script.md`, `week0_slides.md` | Block 4 (live lab-tool checks) and Block 5 (the warm-up topic and its one practice question); the six-weeks slide (W0.04) |
| `week0_quiz.example.json` | Replace with 10 warm-up questions on the course's first hard skill (binary for Network+; Security+ has none) |
| `quickstart_TryHackMe.md` | Room name in step 2; screenshots `shots/thm_*.png` (Josh's Chrome) |
| `quickstart_LabTool_PacketTracer.md` | Rename to `quickstart_<Tool>.md` and rewrite for the course's own lab tool, or delete if TryHackMe is the only one. Screenshots on Josh's computer (computer use) |
| `acronyms.tsv` | One row per acronym the course uses: write the meanings and notes yourself (CompTIA's list is a checklist only, it's copyrighted); session = the session that teaches it |
| `acronyms_back.md` | The back page of the printable glossary (it doubles as the interest-list download); points to the website |
| `mixed_reviews.tsv` | Same pattern for an 18-session course; check the session numbers if the week split differs |
| `pbq_pack.py` | About 10 new drag-and-drop PBQs for homework after Session 17, one per course-map PBQ type, never a copy of a Session 17 workshop PBQ or a practice-bank item |
| `domains.tsv` | The exam's five domains: name, objective range, weight, the sessions that teach each (used by the Trap Atlas and the cheat sheet headers) |
| `objectives.md` | Every objective and sub-bullet from the official CompTIA PDF (format in the file). Feeds the Coverage Matrix |
| `traps.tsv` | **Trap Atlas** source: one row per planted trap in the scripts (session, objective or `skill`, topic, the trap, why it fails), in our own short words. Start from `tools/trap_extract.py src > traps_draft.tsv`, which lists every "Here's the trap" paragraph with its slide and block objectives; the build warns when a session's scripts have more trap paragraphs than the atlas |
| `cheat_sheets.md` | **Domain Cheat Sheets**, one page per domain (the build warns if the PDF has more pages than domains). Rewrite from the course's handouts; Top Traps come from `traps.tsv` |
| `after_the_exam.md` | **After the Exam** guide: CompTIA facts for this exam checked on comptia.org (passing score, CEUs, renewal by a higher certification), retake and post-retake policy from the handbook, next steps |
| `instructor_guide.md` | **Instructor and TA Guide**: roles, before each session, Zoom, chat pauses, falling behind, the 48-hour lab check, recordings, grading and make-ups, Practice Exams A–D (slots from the course's draws), study plans, Exam D, vouchers, accommodations, TA duties, email templates and the study plan template. Policies come from the handbook; Session 18 roles from its Proctoring Checklist |
| *(generated)* | **Objective Coverage Matrix** (instructor docx) from `objectives.md`, the slide objective tags, nightly quizzes and, if `BANK_ITEMS` in course.env points to the bank's `bank_items.json`, the four pools. Any objective with no session, block, quiz item or pool item is listed under Gaps: fix those before launch |
