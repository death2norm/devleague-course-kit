# Timing

*About 60 minutes. Opening 3 · Block 1 (how the course runs) 6 · Block 2 (exam and voucher) 6 · Block 3 (tools, with a 2-minute Moodle tour) 5 · Block 4 (Packet Tracer and TryHackMe live checks) 10 · Block 5 (binary warm-up, one practice question) 10 · Close and questions 15-19. If the live checks run long, shorten the questions, not the checks.*

# Opening

[SLIDE W0.01]

Good evening, everybody, and welcome to DevLeague {{COURSE_NAME}}. This is Week 0, our one-hour orientation. Tonight isn't a lecture on networking yet. Tonight is about making sure that when Session 1 starts, nobody is fighting with a login screen or an installer while the rest of the class is learning. If we do this hour right, every one of you walks into Session 1 with your accounts working, Packet Tracer installed and tested, TryHackMe ready, and a clear picture of how you earn your exam voucher.

*Instructor note: the next paragraph is your personal introduction. Replace it with your own background. Keep it under a minute.*

Let me introduce myself quickly. I've spent my career building and fixing networks, from small offices with one switch in a closet to large sites with hundreds of devices and a change board that meets every week. I've sat these exams myself, and I've learned that knowing a fact and answering a question about that fact are two different skills. This course teaches both.

You'll also meet your TA tonight. Your TA is in every session as a co-host, helps in the breakout rooms, reads your reflections and answers your questions in Slack. When I say "ask in Slack," that's who answers, and the promise is an answer within 24 hours.

*Instructor note: have the TA say hello and post the Slack channel name in the chat.*

[SLIDE W0.02]

Here's the hour. First, how the course runs, so you're never guessing what comes next. Second, the exam and the one number that earns your voucher. Third, a quick tour of the tools. Fourth, the important part: a live check of Packet Tracer and TryHackMe, where everyone opens the same test file and we fix any problems together. And last, a ten-minute warm-up on binary numbers, with time for your questions at the end.

If you haven't done the Week 0 Checklist yet, don't worry. We'll do the key parts live. But keep the checklist open, because anything we don't finish tonight is on it.

# Block 1 — How the Course Runs

*Objectives: Orientation*

[SLIDE D01]

[SLIDE W0.03]

Every night in this course has the same shape, so you can plan your evening around it. We start with a lecture, broken into two parts with a ten-minute break between them. Inside the lecture, you'll hear me say "Let's try one" a lot. That's a practice question. I read it out loud, you pick an answer in the chat, and then we go through every choice, including the wrong ones, because knowing why the wrong answers are wrong is what makes you fast on exam day.

After the second part of the lecture, there's another short break, and then you go into breakout rooms with your lab group. Same group every night, four or five people, so you get to know who you're working with. The lab is hands-on: some nights in Packet Tracer, some nights in TryHackMe, some nights a worksheet like a cabling plan or a disaster recovery plan. Every lab ends with the same question: what would you check first? That habit matters, because troubleshooting is the biggest part of the exam.

After the lab, everyone comes back to the main room for a debrief. Each group tells us what they found. Then the night ends, three hours after it started. We keep to time. Your questions can run long; the lesson won't.

[SLIDE W0.04]

Here's the six weeks at a glance. The first two weeks build the foundation: the OSI model, ports and protocols, IPv4 subnetting, IPv6 and the services every network runs, then cables and connectors and the way networks are laid out. Week 3 is the heart of the course: switching, routing and wireless, mostly in Packet Tracer. Week 4 moves to cloud and modern architectures, documentation and disaster recovery, and monitoring. Week 5 is security, attacks and defenses, then the first troubleshooting night. Week 6 finishes troubleshooting, then Session 17 is a full review with practice on the performance-based questions, and Session 18 is the live practice exam.

You don't need to remember any of that tonight. The calendar is in Moodle, and each session's slides and handout are posted there too.

[SLIDE W0.05]

Homework is short, and it's designed to teach, not to grade you. Every night there's a quiz in Moodle: 10 or 12 questions on that night's material, and from Session 4 on, two extra subnetting questions, because subnetting is the skill that fades fastest if you don't use it. You can take each quiz as many times as you like. Every answer, right or wrong, tells you why. Read that feedback even when you got it right, especially when you got it right by guessing.

There are also three short reflection questions each night. Your TA reads them and gives you a few words back. And at the end of each week, there's an optional Mixed Review: 15 random questions from that week and earlier weeks. After Session 9, there's a 45-question Checkpoint, timed like the real exam, to show you where you stand halfway through. None of those count toward anything. They're there because pulling old material back out of your memory is what makes it stick.

If you miss a session, you make it up within seven days: watch the recording, submit that night's lab worksheet, and score 80 percent or higher on its quiz. Recordings are usually posted by the next day.

# Block 2 — The Exam and Your Voucher

*Objectives: Orientation*

[SLIDE D02]

[SLIDE W0.06]

Let's talk about the exam itself. CompTIA {{COURSE_NAME}}, exam code {{EXAM_CODE}}. Up to 90 questions in 90 minutes, and a passing score of 720 on a scale that runs from 100 to 900. Most questions are multiple choice. A few are performance-based questions, which we'll call PBQs: you drag cables to ports, fill in a subnet plan, read some command output and pick the fix. They tend to come first on the exam and they're slow, so in Session 17 we practice exactly how to handle them.

The exam has five domains. Troubleshooting is the biggest, almost a quarter of the questions, which is why we start the troubleshooting method on night one and never stop using it.

[SLIDE W0.07]

Now the practice exams, because this is how your voucher works. There are four practice exams, A, B, C and D. Each one is 90 questions in 90 minutes, weighted by domain like the real exam. And each one draws from its own sealed pool of questions, so a question you see on one exam doesn't show up on another.

Practice Exam A is a diagnostic. It opens at home at least 48 hours before Session 17; take it before Session 17 so your score by domain shapes the final review. Practice Exam B is the big one. You take it live in Session 18, cameras on, one attempt. If Exam B doesn't go your way, you get a personal study plan within two business days, and Exam C opens at home for two weeks. If you need it, Exam D comes after that, once you've retaken the nightly quizzes for your two weakest domains at 80 percent and had a short call with your TA.

[SLIDE W0.08]

And here's the one number that matters: 77 out of 90. Score 77 or higher on Practice Exam B, C or D, and you've earned your voucher. That's about 85 percent, but go by the 77, because that's the number Moodle checks. Attendance doesn't decide it, and labs don't decide it. The score does. The program team emails your voucher code within three business days (after a short check call, if one is needed), and the voucher includes a retake, so if the real exam doesn't go your way the first time, your second attempt is already paid for.

Why 77? Because students who score there on a fresh practice exam they've never seen tend to pass the real one. We want you to walk into the testing center already knowing you're ready.

[SLIDE W0.09]

Two rules about practice exams, and they're the same for everyone. First, they're closed book. No notes, no other tabs, no AI tools and no help from anyone. At-home exams start with an honor statement you agree to before the first question. Please don't copy or share the questions either. The pools are sealed so that the score actually predicts how you'll do, for you and for every student after you.

Second, if an at-home score jumps more than 20 percentage points above your previous practice exam, the program team sets up a short, friendly call about how you prepared before the voucher goes out. Big jumps happen, and that's great. The call is a conversation, not an accusation, and everyone gets the same rule.

# Block 3 — Your Tools

*Objectives: Orientation*

[SLIDE D03]

[SLIDE W0.10]

Five tools, and each one has one job. Moodle holds everything for the course: slides, handouts, the nightly quizzes, the lab pages where you submit work, recordings and the practice exams. Slack is for questions between sessions, and it's where announcements go. Zoom is the classroom, including the breakout rooms. Please use the Zoom app, not the browser version, because breakout rooms work much better in the app. Packet Tracer is Cisco's free network simulator, and we use it in six sessions. TryHackMe is a lab site with guided rooms, and your Premium account is included through 30 days after Session 18.

*Instructor note: share your screen and open the Moodle course. Show the Start Here section (Handbook, Week 0 Checklist, the two Quick Starts, the Warm-Up quiz), then open Session 1 and point out the slides, handout, lab, reflection and quiz. Then open Course Resources and show the acronym glossary and drills. Two minutes.*

[SLIDE W0.11]

Every lab gets submitted the same way, so let me show you once. You open that session's Lab page in Moodle. You do Part 1 on your own and Part 2 with your group, out loud. You take a screenshot that shows your work, and you fill in the worksheet. Then you go back to the Lab page, click Add submission, drag in the screenshot and the worksheet, and click Save changes. The status should say Submitted for grading. Your TA marks it complete. That's it.

For screenshots: on Windows, press the Windows key, Shift and S, then drag a box. On a Mac, press Shift, Command and 4, then drag a box. The Quick Starts in Moodle show both.

# Block 4 — Lab Check: Packet Tracer and TryHackMe

*Objectives: Orientation*

[SLIDE D04]

[SLIDE W0.12]

Now the most useful ten minutes of the night. Everyone, open Packet Tracer. If it asks you to sign in, use your Cisco Networking Academy account. Then download the test file from Start Here in Moodle. It's called {{PREFIX}}_W0_TestFile.pkt. Open it with File, then Open.

You'll see a small network: two computers, PC-A and PC-B, connected to one switch. When the file first opens, the link lights on the cables may be orange for a few seconds while the switch starts up. Wait until they turn green.

Now click PC-A, open the Desktop tab, and open Command Prompt. Type ping, a space, and 192.168.1.11. That's PC-B's address. Press Enter. You should see four replies. When you do, take a screenshot and post a thumbs-up in the chat. If you don't, post what you see instead, and we'll work through it together.

*Instructor note: give the class about five minutes. The TA watches the chat and takes anyone stuck into a breakout room. Most failures are an orange link (wait), a typo in the address, or Packet Tracer not installed yet (they finish the Quick Start after class).*

[SLIDE W0.13]

If your ping didn't work, read what you see before you change anything. That's the troubleshooting method in miniature, and we'll use it all course. Orange link lights mean the switch is still starting; give it thirty seconds. "Request timed out" usually means the address was typed wrong, so check it. If Packet Tracer won't let you sign in, make sure you're using the email from your Networking Academy account. And if it won't install at all, it's often a work laptop that blocks software installs. Use a personal computer for this course if you can.

Anyone whose Packet Tracer isn't working yet, the TA will follow up with you in Slack tomorrow. You'll need it working by Session 7, but please don't wait that long.

[SLIDE W0.14]

TryHackMe next, and this one's quick. Go to tryhackme.com and sign in with the account DevLeague set up for you. Your invite came by email; check your spam folder if you can't find it. Once you're in, check that your profile shows Premium. If it says free, you may be signed into a personal account, so sign out and use the DevLeague one.

Then open the room called What is Networking? and click Join Room. That's your first lab in Session 1, so joining it now saves you a minute next time. Thumbs-up in the chat when you see the room's task list.

*Instructor note: anyone without an invite gets added to a list the TA sends to the program team tonight.*

# Block 5 — Warm-Up: Binary in Ten Minutes

*Objectives: 1.7 preview*

[SLIDE D05]

[SLIDE W0.15]

Last block. A ten-minute warm-up on binary, because Session 3 is subnetting, and subnetting is a lot easier if binary doesn't scare you.

An IPv4 address is four numbers, called octets, like 192.168.1.10. Each octet is eight bits, and each bit has a value. From left to right: 128, 64, 32, 16, 8, 4, 2, 1. Each one is double the one to its right. When a bit is on, it's a 1, and you add its value. When it's off, it's a 0, and you skip it.

So 00000001 is 1. 00000010 is 2. 00001010 has the 8 and the 2 on, so it's 10. And if all eight bits are on, you add everything: 128 plus 64 plus 32 plus 16 plus 8 plus 4 plus 2 plus 1, which is 255. That's why no octet in an IPv4 address is ever bigger than 255.

That's the whole trick. Write those eight values across the top of a scrap of paper, and any octet becomes simple addition.

[SLIDE W0.16]

Let's try one.

What is the binary number 11000000 in decimal?

A. 128
B. 192
C. 224
D. 96

Type your letter in the chat.

*Pause for answers.*

The answer is B, 192. The first two bits are on, and they're worth 128 and 64. Add them and you get 192. A is the trap for people who only count the first bit. C, 224, is 11100000, with three bits on, not two. And D, 96, is what you get if you start the values at 64 instead of 128, so always start at 128.

And notice where you've seen 192 before. 192.168 is the start of the most common home network addresses. By the end of Session 3, you'll be reading addresses like that in binary without thinking about it.

[SLIDE W0.17]

The warm-up quiz is in Start Here in Moodle: ten questions on binary and subnet basics. Take it tonight or tomorrow. It doesn't count toward anything. It tells you, and it tells us, where to spend a little extra time before Session 3.

If it felt hard, that's completely normal. Session 3 teaches all of it from scratch. The best thing you can do between now and then is ten minutes a day of turning numbers into binary and back. It's like learning the times tables: it feels slow for a few days and then it just clicks.

# Close

[SLIDE W0.18]

Before Session 1, five things. Read the Student Handbook once; it answers most questions before you have them. Make sure the Packet Tracer test file pings. Make sure TryHackMe shows Premium and you've joined What is Networking? Take the warm-up quiz. And say hello in Slack, because the people in this cohort are the ones you'll be studying with for six weeks.

Let's use the rest of our time for your questions. Anything about the schedule, the tools, the voucher, the exam, anything at all.

*Instructor note: take questions until the hour is up. Common ones: when can I take the real exam (book it as soon as you've earned the voucher, which is Session 18 at the earliest), what if I miss a night (make-up within 7 days), do I need a Cisco background (no), will recordings be available (yes, by the next day). Anything about money, refunds or accounts goes to {{SUPPORT_EMAIL}}.*

Thanks, everybody. See you in Session 1.
