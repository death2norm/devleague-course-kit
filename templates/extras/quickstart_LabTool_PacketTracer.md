# Packet Tracer Quick Start

*For DevLeague {{COURSE_NAME}} students · Do this before the Week 0 orientation · About 30–40 minutes, most of it waiting for the download*

## What Packet Tracer Is

Cisco Packet Tracer is a free network simulator. You build networks from switches, routers, wireless gear and computers, type real Cisco commands, and watch traffic move. We use it in Sessions 7, 8, 9, 14, 15 and 16. It runs on Windows 11, macOS 12 or newer, and Ubuntu 22.04 or 24.04. It doesn't run on Chromebooks, tablets or phones.

## 1. Create a Cisco Networking Academy Account

1. Go to **netacad.com** and click **Sign up** at the top right.
2. Fill in your name, email and country, and choose a password. Use an email you check: Packet Tracer asks you to sign in with this account.
3. Confirm your email from the message Cisco sends you.

![The Cisco Networking Academy home page, where you sign up](shots/pt_01_netacad.png){width=5.5}

## 2. Download Packet Tracer

1. Signed in to netacad.com, open the **Resource Hub** page (search the site for "Resource Hub", or go to netacad.com/resources/lab-downloads) and scroll to **Learning Resources**.
2. Under **Cisco Packet Tracer**, click the version for your computer: **Windows 64bit**, **MacOS 64bit** or **Ubuntu 64bit**. Take the newest version listed (9.0.1 on November 12, 2026).
3. If you'd like a short tour first, the free self-paced course **Getting Started with Cisco Packet Tracer** (click **Get Started With Self-Paced**) also has the download link and a few short videos. You don't need to finish it.

![The Resource Hub page, Learning Resources: Packet Tracer downloads (the links work once you're signed in)](shots/pt_03_download.png){width=5.5}

![The Getting Started with Cisco Packet Tracer course page](shots/pt_02_course.png){width=5.0}

## 3. Install

1. Run the installer and accept the defaults. On Windows, click **Yes** if it asks whether to allow the app to make changes. On a Mac, if macOS says it can't check the developer, open **System Settings, Privacy & Security** and click **Open Anyway**.
2. Cisco lists these requirements: Windows 11, macOS 12 or newer, or Ubuntu 22.04 or 24.04; an x86-64 (Intel or AMD) processor; 4 GB of free memory; 1.4 GB of free disk space. Apple-silicon Macs run it through Rosetta 2, which macOS offers to install the first time.
3. On a work laptop, the install may be blocked. Use a personal computer for this course if it is.

## 4. Start Packet Tracer and Sign In

1. Open Packet Tracer. The first time, it asks you to sign in.
2. Click the green **Skills For All** button and sign in with your Networking Academy account from step 1. Tick **Keep me logged in** so it doesn't ask every time.
3. The main window opens: the workspace in the middle (empty until you open a file), with devices and cables at the bottom left.

![The main window, shown here with the test file open](shots/pt_04_main.png){width=5.8}

## 5. Open the Test File

1. In Moodle, open **Start Here** and download **{{PREFIX}}_W0_TestFile.pkt**.
2. In Packet Tracer, click **File, Open** and choose the file.
3. You'll see two computers, **PC-A** and **PC-B**, connected to one switch. The link lights may be orange for up to 30 seconds while the switch starts. Wait until they're green.

![The test file: PC-A and PC-B on one switch, link lights green](shots/pt_05_testfile.png){width=4.6}

## 6. Ping From PC-A to PC-B

1. Click **PC-A**, open the **Desktop** tab and click **Command Prompt**.
2. Type **ping 192.168.1.11** and press Enter.
3. You should see four replies from 192.168.1.11. Take a screenshot of the window. That's your Week 0 proof that Packet Tracer works.

![A successful ping: four replies from PC-B](shots/pt_06_ping.png){width=4.8}

## 7. Three Things You'll Use in Every Packet Tracer Lab

- **The CLI tab.** Click a switch or router and open **CLI** to type Cisco commands. Press Enter if the screen is blank.
- **Realtime and Simulation.** The tabs at the bottom right switch between normal time and Simulation mode, which shows each packet step by step. Labs say when to use Simulation.
- **Save your work.** Use **File, Save As** and add your name to the file name, for example **{{PREFIX}}_S07_Starter_JaneDoe.pkt**. Some labs ask you to submit the .pkt file.

![A switch's CLI tab, where you type commands](shots/pt_07_cli.png){width=4.6}

## 8. Submit in Moodle

1. Open the session's **Lab** page in Moodle and click **Add submission**.
2. Drag in your screenshot, your worksheet, and the .pkt file if the lab asks for it.
3. Click **Save changes**. The status should say **Submitted for grading**.

## Troubleshooting

| Problem | Fix |
|---|---|
| Packet Tracer won't let me sign in | Use the email and password from your Networking Academy account, not a Cisco.com or Webex account. Try **Forgot password** on netacad.com. |
| I can't find the download link | Sign in to netacad.com first, then open the **Resource Hub**; the links only work when you're signed in. |
| The installer is blocked | Work laptops often block installs. Use a personal computer. |
| The link lights stay orange | Wait 30 seconds; switch ports take time to come up. Still orange after a minute? Close the file and open it again. |
| Ping says "Request timed out" | Check the address you typed: 192.168.1.11. |
| A lab file won't open | Update to the newest Packet Tracer. Files saved in a newer version don't open in an older one. |
| Packet Tracer is slow | Close other programs and browser tabs. It needs 4 GB of free memory. |

Still stuck? Ask in the course Slack channel or email {{SUPPORT_EMAIL}}, and bring it to the Week 0 orientation.
