# Course-level extras: templates

`tools/new_extras.sh <course repo>` copies these into the course's `extras/` and fills the placeholders. They start as the Network+ versions (Nov 12, 2026), which were built from the Security+ originals (course 43) and updated to the Nov 5 and Nov 11 program decisions. Build with `tools/build_extras.sh`; the PDF check fails on any leftover placeholder text, markdown or missing screenshot.

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
