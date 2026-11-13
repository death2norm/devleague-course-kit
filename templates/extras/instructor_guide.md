{{REWRITE: adapted from Network+. Check every section against this course: lab types by session (Section 3), the 48-hour lab check (Section 6), the practice-exam slots from course.env draws (Section 9), Session 18 roles from its Proctoring Checklist, and Appendix C. Delete this line.}}

# DevLeague {{COURSE_NAME}} ({{EXAM_CODE}}) · Instructor and TA Guide

*Internal: instructors, TAs and the program team. Version 1.0, adapted from the Network+ guide (version 1.1) with the current program policies and the {{COURSE_NAME}} details. Everything here is approved: the Security+ guide decisions of October 28, the program decisions of November 5 and 11, and the working practices, email templates and study plan template approved November 13, 2026. Anything new for {{COURSE_NAME}} (beyond these) is marked **(pending)** until Josh approves it; don't promise students anything marked pending. Student-facing rules come from the Student Handbook, Moodle steps from each session's Moodle Checklist and the Practice Bank Moodle Checklist, and timing from each session's Run Sheet. If this guide and one of those ever disagree, those win, and tell the build team.*

## 1. Who Does What

| Role | Approved duties | Not their job |
|---|---|---|
| **Instructor** | Teaches every live session from the script. Runs chat pauses, breakout rooms and the debrief. Watches the clock against the Run Sheet. Runs the Session 13 TryHackMe demo. Proctors Practice Exam B in Session 18 (watches the gallery) and teaches the review clinics. | Moodle builds, vouchers, study plans, make-up checks, grading |
| **TA** (every cohort has one) | Co-hosts every session. Handles private chat (tech problems, stuck students). Answers student questions in the cohort Slack channel **within 24 hours**. Joins breakout rooms on Ask for Help, and takes half the rooms when the cohort is above 20. Grades reflections and labs. Checks make-ups. Watches private chat and Moodle during Exam B, keeps the incident log and builds the most-missed list. Holds the 15-minute Exam D call and asks the program team to add the student to Exam D candidates. | Teaching new content, grading practice exams, any policy decision |
| **Program team** (Josh and the admins, {{SUPPORT_EMAIL}}) | Accounts and enrollment, TryHackMe Premium seats, the Moodle build, the 48-hour checks, posting recordings, accommodation overrides, rescheduling a session the instructor can't teach, study plans, Exam C access, vouchers, score-jump calls, refunds, all student emails. | Teaching |

**Settled for this program:** every cohort has a TA (approved October 28 for the program); there are no scheduled office hours (the TA's Slack support replaces them); there's no backup instructor (the program team reschedules, Section 5); refunds follow the Student Handbook (full before the cohort starts, 75% in the first week, none after), and only the program team answers refund questions.

## 2. Before Each Session

| When | Who | What |
|---|---|---|
| Before Week 0 | Program team | Enroll students in Moodle, Slack and TryHackMe Premium. Build the Start Here section. Send the Week 0 Checklist. |
| 48 hours before | Program team | Follow the session's Moodle Checklist: the lab check (Section 6), the session section is built, breakout groups are pre-assigned, the TA is co-host. If a TryHackMe task number changed, fix the Lab page and tell the instructor. |
| Before class | Instructor | Read the script and the Run Sheet. Skim the Lab Debrief Key. Open the deck in Presenter View so the speaker notes (the script) are on your screen, not the students'. On Packet Tracer nights, open tonight's .pkt once yourself. |
| 15 minutes before | Instructor and TA | Join Zoom, check audio, confirm co-host, confirm cloud recording is on (Section 7), open the session's Moodle section and the Lab page in a browser tab. |

**Session 1 and Week 0:** if you're not Peter Dunn, replace the marked personal introduction in the Session 1 script with your own background (under a minute). The Week 0 orientation script has the same swap, kept to a sentence or two.

**Session 13:** run the TryHackMe layer2 room's Task 7 demo once before your first cohort, and start its machine 10 minutes before Break 2 ends (the Run Sheet shows when).

## 3. Running the Night in Zoom

Every lab night has the same shape: Part 1, Break 1 (10 minutes), Part 2 and the lab handoff, Break 2 (10 minutes), the lab in breakout rooms, then the debrief and questions. The published night is 3:00. Only student questions run it long. Session 18 has its own time model (see its Run Sheet), and Week 0 is 60 minutes.

**Zoom settings (set once per cohort meeting):**
- Breakout rooms enabled, with the cohort's groups of 4–5 pre-assigned. Same groups all course.
- Cloud recording, recording the active speaker with shared screen.
- Participants join muted. Chat to everyone and to host/co-host allowed.

**During the lecture:**
- Teach from the script as written. Every spoken word is there, at 130 words per minute, so the Run Sheet clock holds.
- Slide cues **[SLIDE n.nn]** in the script match the deck exactly. Advance on the cue.
- The TA watches private chat and answers technical problems there. Content questions wait for the practice-question pauses, the break or the debrief, unless they block the whole room.

**Lab nights by type:**

| Lab | Sessions | Students need |
|---|---|---|
| Packet Tracer | 7, 8, 9, 14, 15, 16 | Packet Tracer installed (Week 0) and tonight's .pkt from the Lab page. Remind them in the closing to download it during Break 2. |
| TryHackMe | 1, 2, 3, 4, 6, 10, 12, 13 | Their DevLeague Premium seat and the room links on the Lab page |
| Worksheet only | 5, 11, 17 | The worksheet. Session 17 is the 50-minute PBQ workshop. |

## 4. Chat Pauses (Practice Questions)

Every practice question in a script starts with "Let's try one" or "Let's do one," and the Run Sheet allows one minute for each.

1. Read the question and every answer choice, exactly as written.
2. Say "type your answer in the chat" and wait. About a minute is the budget. Don't fill the silence.
3. Glance at the chat. If the room split between two answers, say so ("about half of you said B"). Never name a student who got it wrong.
4. Read the explanation from the script. It eliminates every choice, including why the planted trap feels right.

If chat is quiet, ask once more ("even a guess helps; a wrong answer costs nothing") and move on. Don't call on individuals by voice.

## 5. Falling Behind and Things Going Wrong

**Behind schedule.** Check the clock at Break 1 against the Run Sheet.
- **Up to 5 minutes behind:** no change.
- **More than 5 minutes behind at Break 1:** shorten the Part 2 practice-question pauses to about 30 seconds. Don't cut a block. Every block carries exam objectives.
- **Still behind at Break 2:** keep Break 2 and the lab at full length. The debrief absorbs up to 5 minutes; cover the findings in the Lab Debrief Key and save open questions for after 3:00, which students may stay for or leave.
- **Never** skip Break 1 or Break 2 to catch up.

**Instructor connection drops.** The TA (co-host) keeps the meeting open, tells the room in chat that the instructor is reconnecting, and keeps recording running. If the instructor isn't back within 10 minutes, the TA moves students into their breakout rooms to start the lab early from the Lab page, and the instructor picks up the lecture when back. Lost lecture time is made up from the recording, not by running past 3:00.

**Instructor can't teach a session.** The program team reschedules it and tells students in the cohort Slack channel and by email.

**A student's Packet Tracer won't work at class time.** First, the file: "won't open" almost always means a different Packet Tracer version, so after class they install the version listed on the course page (the lab files are built in 9.0.1). Tonight, they join a groupmate who shares their screen, and the group submits one worksheet with everyone's name on it. A student whose computer can't run Packet Tracer at all (a Chromebook, a tablet, or an Apple-silicon Mac where it fails) does every Packet Tracer lab this way; tell the program team so they know before Session 7.

**TryHackMe down or the room changed at class time.** Students do the parts of the worksheet that don't need the room, and finish the TryHackMe part later as part of the lab submission. Tell the program team.

**Moodle down.** The instructor shares the Lab Guide on screen (it's in the session package's Student folder; the .pkt can be sent in Slack) and students submit after Moodle is back.

## 6. The 48-Hour Lab Check

The program team does it with a test student account, 48 hours before each session, from that session's Moodle Checklist.

**TryHackMe nights:**
1. Open each room link from the checklist (it labels each room free or Premium; DevLeague seats include Premium).
2. Confirm the room opens and the assigned task numbers still have the titles the checklist lists.
3. If a machine is needed, confirm it starts.
4. **If anything changed:** fix the task numbers on the Lab page, then tell the instructor before class. If the room is gone, the lab runs on the worksheet alone until the build team picks a replacement.

**Packet Tracer nights:**
1. Download the .pkt from the Lab page as a student would, and open it in the Packet Tracer version listed on the course page (9.0.1).
2. Wait for the link lights to settle, then do the Lab Guide's first step. The starting state should match what the Lab Guide describes.
3. If Cisco releases a newer Packet Tracer, the build team tests every .pkt in it before the course page changes. Until then, students stay on the listed version.

**Known notes:** Networking Secure Protocols (Session 13) shows as Premium on its page. Session 13's demo needs the layer2 room's Task 7, not Task 6.

## 7. Recordings

- Record every session to the Zoom cloud. Cloud recording captures the main room only, not the breakout rooms, which is fine: the lab is done from the Lab page.
- Recordings are posted in the session's Moodle section, **normally by the next day** (the Student Handbook promises this). The program team adds the link as a URL named "Session ## Recording."
- **Session 18:** the exam portion may be trimmed before posting.
- Students who miss a session make it up from the recording (Section 8).

## 8. Nightly Quizzes, Reflections, Labs and Make-Ups

**Nightly quiz.** 10 or 12 questions per session in Moodle (from Session 4 on, plus 2 random subnetting questions), open notes, unlimited attempts, with the trap explained in every wrong answer's feedback. Moodle grades it; nobody reviews individual attempts. The one optional review step takes two minutes: before the next session, the instructor can open the quiz's **Results, then Statistics** and, if one question's facility index is below about 50%, mention its trap in that session's debrief.

**Reflection.** 3 short answers, 5 points each, graded by the **TA** with the program's rubric (approved October 28): 5 points to an answer that addresses the prompt with a reason, 3 to one that answers without a reason, and 0 to a blank or off-topic answer. No written comments are required. Sessions 1–9 use a Moodle quiz with essay questions and Sessions 10–17 an online-text assignment, so the TA grades them in two places.

**Lab.** The **TA** marks it complete or incomplete. Complete means the worksheet is submitted with every item attempted (one per group is fine, with every member's name on it), plus the screenshot or .pkt the Lab Guide asks for. Correctness is taught in the debrief, not graded.

**Make-ups.** A student who misses a session makes it up within 7 days: watch the recording, submit that session's lab worksheet, and score 80% or higher on its nightly quiz. Make-ups keep students on track; they don't affect the voucher. The **TA** checks the gradebook when the 7 days are up and sends one reminder in Slack if anything is missing. There's no further penalty to enforce.

**Mixed Reviews** (after Sessions 3, 6, 9, 12 and 15) and the **Week 3 Checkpoint** (after Session 9) are optional and ungraded. Nobody checks them.

## 9. Practice Exams A–D

Every practice exam is 90 questions, 90 minutes, one attempt, drawn from its own sealed pool in domain order: **slots 1–21 Domain 1, 22–39 Domain 2, 40–56 Domain 3, 57–69 Domain 4, 70–90 Domain 5**. The Moodle build steps are in the **Practice Bank Moodle Checklist** (in the practice bank zip); Exam B's night is in the **Session 18 Moodle Checklist** and **Proctoring Checklist**.

| Exam (own pool) | When | Where and how | Who runs it |
|---|---|---|---|
| **A** (diagnostic) | Opens at least 48 hours before Session 17, closes before Session 18 | At home | Program team builds and opens it. Students use their domain scores in Session 17's opening and Reflection 1. |
| **B** (readiness) | Session 18, 0:15–1:45 | Live in Zoom, cameras on, password-protected | Instructor proctors from the Session 18 script and watches the gallery; the TA watches private chat and the attempts page and keeps the incident log. |
| **C** (retake) | When study plans are sent; open 2 weeks | At home, honor statement first, group **Exam C candidates** | Program team |
| **D** (second retake) | 2–3 weeks after Exam C closes; open 2 weeks | At home, same rules as C, group **Exam D candidates** | Program team; the TA holds the call and adds the student |

**Rules that keep the pools sealed:**
- Never show or read a Pool B, C or D question, and never turn on Right answer or feedback review options for any practice exam. Only marks and overall feedback are shown.
- Never add Pool questions to a nightly quiz, Mixed Review, Checkpoint or practice file, and never use "include subcategories" when adding random questions.
- Never name, rank or compare individual students' scores in class. Vouchers and study plans go out by email.

**Missed Exam B.** If the student contacts the program team within 48 hours, add a **user override** on Exam B with new open and close times within 7 days, and a new password sent only to that student (Missed Exam B email, Appendix A). The closed-book rules are the same as Exam C's. A student who lost more than 10 minutes on the night gets the same makeup. Because Exam B has no honor statement item, the makeup email asks the student to reply "I agree" to the honor statement before starting, and the voucher waits for that reply. If they don't contact within 48 hours, add them to **Exam C candidates** with the students below 77 of 90, and build their study plan from their Practice Exam A domain scores.

**Camera fails during Exam B.** The student keeps working; the TA tries for 5 minutes in the "Camera help" breakout room. If it can't be fixed, the score counts under the at-home rules (honor statement and the score-jump check). The TA marks it in the incident log and, after the session, sends the honor statement by Slack direct message; the voucher waits until the student replies "I agree" (Proctoring Checklist).

## 10. After Exam B: Study Plans and Exam C

**By the next business day (TA):** send the program team (Josh) the 77-or-higher list, the below-77 list with each student's two weakest domains, and the incident log (Proctoring Checklist, "After the session").

**Within two business days of Session 18 (program team):**
1. Domain scores: sum each student's marks in slots 1–21, 22–39, 40–56, 57–69 and 70–90 (the gradebook's domain items do this). The weakest domain is the lowest percentage, not the lowest raw mark.
2. **77 of 90 or higher (77.00 in Moodle):** issue the voucher (Section 12).
3. **Below 77 of 90:** fill in a **Study Plan** (Appendix B) for the two weakest domains and send it with the **Study Plan** email (Appendix A). Add the student to **Exam C candidates**; Exam C opens for them when the plan is sent and closes two weeks later.
4. Three days before Exam C closes, send the **Exam C Reminder** to anyone who hasn't attempted it.

**Score-jump check.** If an at-home score (makeup B, C or D) is more than **20 percentage points** above the student's previous practice exam, the program team holds a short, friendly call about how they prepared before releasing the voucher. It's a conversation, not an accusation. If the explanation is reasonable, release the voucher. If there's a real integrity concern, Josh decides (Proctoring Checklist).

## 11. Exam D: The Unlock and the Last Step

A student below 77 of 90 on Exam C gets Exam D once **both** are true:

1. They've retaken the nightly quizzes for their **two weakest domains** (from their Exam C domain scores, worked out as in Section 10) and scored **80% or higher** on each of those sessions' quizzes.
2. They've had a **15-minute call with their TA**.

Then the program team adds them to **Exam D candidates** (the TA asks; the TA's Moodle role can't manage groups). Exam D opens 2–3 weeks after Exam C closes and stays open 2 weeks, at home, under Exam C's rules. Send the **Exam D Path** email (Appendix A) when Exam C results come in.

**The 15-minute TA call** (the only one-to-one call in the program):
- **Minutes 0–3:** look at the student's Exam C domain scores together. Name the two weakest domains.
- **Minutes 3–10:** ask how they studied and which traps keep catching them. Point them to that domain's session recordings, handouts, the Domain Cheat Sheet and the Trap Atlas.
- **Minutes 10–15:** agree a date to take Exam D inside its window, and confirm the quizzes are done or when they will be.
- Afterward, tell the program team the call happened and whether the quizzes are done, so they can add the student to Exam D candidates. That's the only record needed.

**Below 77 of 90 on Exam D:** the student gets 3 more months of access to the recordings and practice exams, plus a free seat in the next cohort's Sessions 17 and 18 and that cohort's live Exam B. The program team sends the offer (Appendix A) and enrolls them when that cohort is set up.

## 12. Vouchers

- **Who qualifies:** 77 of 90 on Practice Exam B, C or D. The score is the only requirement. Attendance, labs and quizzes don't gate it.
- **How:** mark the student Exam Ready in the program's student records, assign the next CompTIA {{COURSE_NAME}} voucher code, and send the **Voucher Issued** email **within 3 business days** of the qualifying score (after the score-jump call, if one is needed).
- **Voucher stock:** CompTIA vouchers expire on a fixed date, can't be extended or refunded, and the retake only works for the same exam version. Buy close to when they're issued, and issue the oldest first.
- **Retake:** the voucher includes one retake. CompTIA's current policy: no wait before a second attempt, 14 days before a third.
- **Didn't pass after the retake:** the student gets 3 more months of access to the recordings and practice exams, plus a reduced-price voucher for another attempt (amount set by the program team). The program team arranges both when the student tells them.

## 13. Accommodations

- **Practice exams:** a student with CompTIA-approved testing accommodations gets the same on every practice exam. They email their CompTIA approval to {{SUPPORT_EMAIL}} before Practice Exam A. The program team adds a **user override** on each of Exams A–D with the extra time **and a later close time** (an attempt ends at the time limit or the close time, whichever comes first).
- **Exam B:** tell the instructor and TA which students have overrides. A student whose extra time would run past 3:00 (for example, double time) takes Exam B at home as an approved makeup and joins at 1:55 for the review and close.
- **Live sessions:** students raise these during Week 0. The program team records them and tells the instructor before Session 1.

## 14. TA Duties at a Glance

| When | Duty |
|---|---|
| Every session | Zoom co-host. Answer private chat (tech problems first). Keep recording running if the instructor drops. |
| Between sessions | Answer student questions in the cohort Slack channel within 24 hours. |
| After each session | Grade the three reflections (5 / 3 / 0 rubric) and mark labs complete or incomplete. |
| 7 days after a missed session | Check the make-up in the gradebook; send one Slack reminder if it's missing. |
| Every lab | Join a room when a group clicks Ask for Help. Take half the breakout rooms when the cohort is above 20. Pair a student whose Packet Tracer fails with a groupmate's screen. |
| Week 0 | Help stuck students through account setup and the Packet Tracer test file by private chat; give the program team the names of anyone still stuck. |
| Session 18 | Run the Proctoring Checklist: private chat, attempts page, camera help, incident log, the most-missed list at the break, and the lists to the program team by the next business day. |
| After Exam C | Hold the 15-minute call for each eligible student and tell the program team, who add them to Exam D candidates. |

That's the whole list. Any other duty needs the program team's approval first.

## Appendix A: Email Templates

*Program team: replace the bracketed fields. Send from {{SUPPORT_EMAIL}}. Exam D Path, Missed Exam B and Exam D Below 77 are adapted from the approved Security+ templates; Voucher Issued, Study Plan, Exam C Reminder and Score Check Call were approved November 13, 2026.*

### Voucher Issued

> **Subject:** Your CompTIA {{COURSE_NAME}} voucher
>
> Hi [First name],
>
> Congratulations: you scored [score] of 90 on Practice Exam [B/C/D], and you've earned your voucher. Your CompTIA {{COURSE_NAME}} voucher code is **[code]**. It expires on **[date]** and includes one retake.
>
> To book: sign in at login.comptia.org with your name exactly as it appears on your government ID, schedule {{COURSE_NAME}} {{EXAM_CODE}} with Pearson VUE (online or at a test center), and enter the code at checkout. Most students do best testing within two to three weeks. Your Session 18 Exam-Day and Voucher Guide has the details.
>
> Keep this code private: anyone who has it can use it. When you've taken the exam, tell us how it went.
>
> [Program team name], DevLeague

### Study Plan (below 77 on Exam B)

> **Subject:** Your study plan and Practice Exam C
>
> Hi [First name],
>
> Thank you for taking Practice Exam B. You scored [score] of 90, and the voucher bar is 77 of 90. That's a measurement, not a verdict. Your two weakest domains were **[Domain]** and **[Domain]**, and your study plan for them is attached.
>
> Practice Exam C is open in Moodle (Session 18) from **[date]** to **[date]**. It's at home: one 90-minute attempt, closed book, new questions, with an honor statement first. Score 77 of 90 or higher, and your voucher is released.
>
> Questions about the plan go to your TA in the cohort Slack channel; they answer within 24 hours.
>
> [Program team name], DevLeague

### Exam C Reminder

> **Subject:** Practice Exam C closes on [date]
>
> Hi [First name],
>
> A reminder that your Practice Exam C closes on **[date]**. Give yourself 90 quiet, uninterrupted minutes, and work your study plan's two domains first if you haven't yet.
>
> [Program team name], DevLeague

### Exam D Path

> **Subject:** Your next step: Practice Exam D
>
> Hi [First name],
>
> Thank you for taking Practice Exam C. You scored [score] of 90, and the voucher bar is 77 of 90. You have one more practice exam, Exam D, with new questions you haven't seen.
>
> **To unlock it:**
> 1. Retake the nightly quizzes for your two weakest domains, [Domain] and [Domain], until you score 80% or higher on each. The sessions for each domain are listed at the top of its Domain Cheat Sheet.
> 2. Book a 15-minute call with your TA, [TA name], at [booking link or reply to this email].
>
> Exam D opens on **[date]** and closes on **[date]**. It runs the same way as Exam C: at home, one 90-minute attempt, closed book, with an honor statement. Score 77 of 90 or higher, and your voucher is released.
>
> [Program team name], DevLeague

### Missed Exam B: Makeup Confirmed

> **Subject:** Your makeup Practice Exam B
>
> Hi [First name],
>
> Thanks for letting us know. Your makeup Practice Exam B is open in Moodle (Session 18) from **[date and time]** to **[date and time]**. Take it at home, alone: one 90-minute attempt, closed book, with no notes, people, websites or AI tools. The exam password is **[password]**.
>
> Before you start, reply to this email with "I agree" to this statement: *I will complete Practice Exam B on my own, without notes, other tabs or programs, a phone, AI tools or help from anyone.*
>
> Score 77 of 90 or higher, and your voucher is released. Otherwise, you'll receive a study plan and move to Practice Exam C.
>
> [Program team name], DevLeague

### Score Check Call

> **Subject:** A quick call before your voucher
>
> Hi [First name],
>
> Congratulations on your Practice Exam [B/C/D] score. Because it's more than 20 percentage points above your previous practice exam, we have a short, friendly call with everyone in that situation before releasing the voucher, about how you prepared. Reply with two times that work for you this week.
>
> [Program team name], DevLeague

### Exam D Below 77: Next Cohort Seat

> **Subject:** Your seat in the next cohort's final review
>
> Hi [First name],
>
> Thank you for sticking with it through Practice Exam D. You scored [score] of 90. As your handbook describes, you have 3 more months of access to the recordings and practice exams, and a free seat in the next cohort's final review, Sessions 17 and 18, where you'll take that cohort's Practice Exam B. We'll send dates as soon as that cohort is scheduled.
>
> [Program team name], DevLeague

## Appendix B: Study Plan Template

*One page per student. Domain scores come from the gradebook's domain items for Exam B (for a student who missed Exam B and didn't ask for a makeup, use Exam A).*

| | |
|---|---|
| Student | [Name] |
| Exam and score | Practice Exam [A/B]: [score] of 90 (bar: 77 of 90) |
| Domain scores | D1 [ ]/21 · D2 [ ]/18 · D3 [ ]/17 · D4 [ ]/13 · D5 [ ]/21 |
| Weakest domains | [Domain] ([%]) and [Domain] ([%]) |
| Exam C window | [date] to [date] |

**For each weak domain:**
1. Read its Domain Cheat Sheet, then its section of the Trap Atlas, covering the right-hand column.
2. Rewatch the sessions listed on the cheat sheet, starting with the blocks you were least sure of.
3. Retake those sessions' nightly quizzes until you can say why every wrong answer is wrong (aim for 90%; the Exam D unlock needs 80%).
4. Do 20 timed questions in 20 minutes from those quizzes the day before Exam C.

**Help:** your TA, [TA name], in the cohort Slack channel (answers within 24 hours).

## Appendix C: Approvals

*Approved on November 13, 2026 (Network+ guide v1.1, for every course): the working practices carried over from the Security+ guide (behind schedule, connection drops, lab-tool, TryHackMe and Moodle outages, the quiz-statistics look, trimming the Session 18 recording), the lab-tool fallback and listed version, the "I agree" reply before a makeup Exam B, the Exam C reminder, voucher buying, the four email templates and the study plan template. The program policies (Student Handbook and Session 18 guide, a TA in every cohort, TA grading, TA Slack answers within 24 hours, no office hours, no backup instructor, the 20-point score-jump call) were approved earlier. List anything new for {{COURSE_NAME}} here, marked (pending), until Josh approves it.*
