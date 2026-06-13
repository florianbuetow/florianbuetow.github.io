---
title: "Interview Series - From Classical Guitar to Ruby on Rails"
subtitle: "A professional musician turned software engineer - on career pivots, side projects, and building with AI."
slug: "interview-from-classical-guitar-to-ruby-on-rails"
date: 2026-05-25
draft: false
description: "Eike Rackwitz trained as a classical guitarist before transitioning into software engineering. In this interview, he discusses his career pivot, how he landed his first role as an engineer, the side projects he developed before graduating, and practical lessons for junior developers starting out today."
author: "Florian Buetow & Eike Rackwitz"
categories: ["Interviews", "AI Engineering"]
tags: ["Interview", "Career Pivot", "Ruby on Rails", "Semantic Search", "MCP", "Claude Code", "Codex", "Junior Developers"]
---

## Preamble

This conversation tracks an engineer who started professional software development in October 2022 - two months before ChatGPT shipped. He arrived from outside the field with a music bachelor's and a few years as a working classical guitarist. Four years on, he runs an LLM-powered semantic search engine that serves half a million sheet-music scores, contributes to Rails and Neovim, and operates with multiple coding agents in parallel across Claude Code, Codex, and his own MCP servers.

The arc is unusual on two axes: a late entry into engineering and a career that is AI-native from the start. Both are increasingly common stories and rarely told together. Eike Rackwitz is a senior full-stack engineer at a small recruiting and employer-branding company in Germany. We talked about how he got there, what it taught him, and what he thinks juniors entering the field today should actually do.

<!--more-->
---

![Eike Rackwitz's journey from classical music to AI engineering](Music_to_AI_Engineering_Journey.webp?zoom)

## Introducing Eike

**Hi Eike, please introduce yourself briefly. Who are you? What do you do? Where do you work?**

> _I'm Eike Rackwitz. I'm a senior full-stack engineer at a small software company in Germany. I build web applications end to end with Ruby on Rails and modern JavaScript - backend architecture, integrations, data modeling, frontend. A lot of my recent work has focused on AI-backed product features: semantic search with pgvector and ChromaDB, LLM classification pipelines. I also have a few side projects in that space._

**How long have you been doing this professionally?**

> _Four years in October. I started as a working student in October 2022, went part-time after three months, and I've been there since. Almost the entire time I've been writing software professionally, ChatGPT and Claude have existed._

**What does the product you are working on do?**

> _The company builds recruiting and employer-branding software. The core piece is a recommendation network. When someone applies for a role and they're a strong candidate but not the right fit - maybe the company already picked someone equally good - they get a rejection together with a code. They can use that code to apply to other companies in the network, and those companies see it and know the person was already validated as strong somewhere else. The point is that good applicants don't fall out of the funnel - they get redirected. Around that we have a recruitment management system, search, questionnaire tools, a salary benchmark - the surrounding toolchain - but the network is the core idea._

---

## From classical guitar to code

**Let's go back to understand how you got where you are now. What did you do right after school?**

> _I didn't really have a clue. Civil service was still compulsory back then, so I did that. I'd had guitar lessons for a long time, and every professional musician I knew told me the same thing: don't go that direction, at least not financially. So I had to choose between music and the other things I cared about - math, natural sciences, computer science. I picked computer science and started studying at Martin Luther University Halle._

**And music came back in.**

> _A few semesters in, the artistic subjects at the university moved from Magdeburg to Halle. Through various connections I met a guitar professor, played for him, and he offered me a place in his class if I passed the qualification test. In music that's a rare opening - each professor takes only ten to fifteen students across the whole class. I tried doing both for a semester and quickly realised you can't deepen yourself on the instrument that way. So I dropped computer science and went all-in on music._

**Where did the guitar even come from, going further back?**

> There was a music school called Fröhlich. My parents enrolled me there just before I started school, and the director of the school told them I had a feel for melody and should learn piano - but a real piano wasn't something they could afford. So my dad said, "I have a guitar at home." That's how it started, around first grade.

**At some point classical guitar must have stopped being something you did and started being something you chose.**

> _There was a stretch where I lost motivation - you don't really understand why you're practicing classical guitar when you don't feel like it. Then my dad took me to a Deep Purple concert in Berlin. I was maybe fourteen. Steve Morse was on guitar, and it flashed me. After that I got obsessive - listening solos out by ear, writing down what I heard, recording myself on the old Windows audio recorder and overdubbing my own parts. I wished I still had those takes, but I wasn't doing backups back then. The music carried me to the end of school._

**When you finished your music degree in Halle, you worked as a musician and teacher for a few years. What did that life actually look like?**

> _I taught at the university and at a music school, took private students, and did performances. The guitarist's life is a bit niche - it was still livable, but every contract was honorary. One semester at a time, maybe a year. It always worked out - until Corona came._

**What did Corona do to that life?**

> _For weeks, everyone without a permanent contract simply stopped getting paid. Nobody knew whether that would last a month or a year. Around the same time my first daughter was born, at the end of 2021, and you start asking whether this is really the future. I'd quietly known the honest version for a while: I went into music because of the music, not because of teaching - and teaching is most of the job. Covid forced me to stop pretending otherwise. I discovered that the University of Hagen offered a remote degree in mathematical software development that was actually affordable, and I could recognise a lot of it from my earlier computer science semesters. That's the door I walked through._

> _In hindsight I picked the hardest version on purpose. I could have done a regular computer science degree, but my ego didn't want to admit that dropping CS the first time, when I was in Halle, had been a mistake. So I went and did the math-heavy one._

---

## Learning on a three-person team

**How did you actually find that first job?**

> _I'd started at FernUni Hagen in the summer semester, and after the first half-year the obvious thing hit me: I needed real software experience or this wasn't going to lead anywhere. So I started applying for working-student roles. Most of the ads were paradoxical - they wanted experience for a job whose whole point is that you don't have any yet. Very demanding for what they were offering. One ad was the opposite. It read "who wants to learn Ruby on Rails?" - framed as a learning opportunity, not a requirements checklist. That ad was written by Stefan, our lead engineer._

> _The actual connection was incidental. I'd put on my CV that I worked in Linux and used Vim. I'd just always liked editing text - it predated everything else. It turned out Stefan worked the same way, and that's what made him pick the application up. We talked, and they took me._

**What did the first months look like?**

> _I started in October 2022. I'd had that earlier brush with computer science before guitar, so I knew some Java, I'd written a Bomberman clone for a course, I had some programming muscle. But Ruby and Rails I'd never touched, and I'd never done web development. We were three people on the engineering side - Stefan the lead engineer, Andi, and me. We did a lot of pair-programming sessions. They'd give me an issue I couldn't solve, we'd talk through the solution afterwards. I learned by writing code and being walked through reviews._

**You ended up with a lot of trust quickly.**

> _Within the first year I had permission to merge most things to main directly. If I wasn't sure, we'd review it together. Things did go wrong - I broke something visually here, missed data in a table there. Stefan's line was always, "you learn from it, everyone has it, it happens to me." That mattered. I could make mistakes and grow without theatre around it._

**You had access to the full codebase and the full database from very early.**

> _Yes. I didn't have an SSH key to the VPS, so I couldn't take the production server down directly. But I could absolutely have deleted rows or merged something destructive. That's the kind of access a senior engineer normally has. I think I got there earlier than most because we were small._

**Reflecting on your own path, what is your recommendation for someone picking a first job in tech?**

> _Don't underestimate small teams. In a big company there are processes, queues, meetings. The lead doesn't have two free hours to pair with you. In a three-person team, your colleagues are personally incentivised to make you solid - they go on vacation too. The time they spend with you pays back into their own business. You also touch every layer of the stack: backend, frontend, DevOps, database. You can't specialise yet, which is exactly what a junior should be avoiding._

---

## The UUID benchmark thesis

**Your CS studies are nearing their end, and you just handed in your bachelor's thesis for evaluation.**

{{< sidenote label="UUID" >}}A UUID (Universally Unique Identifier) is a long, randomly generated string of letters and numbers used to identify information. Different formats and generation strategies can heavily affect write speed, index efficiency, and overall system performance at scale.{{< /sidenote >}}

> _Correct, the topic of my thesis is A UUID benchmark across PostgreSQL, MySQL, MongoDB, and Cassandra - how different UUID strategies interact with each storage engine's internal architecture. SQL databases lean on B-tree indexes, Cassandra uses LSM trees, and the choice of UUID version changes write performance, read performance, and concurrent-write behaviour in non-obvious ways._

**Who supervised it?**

{{< sidenote label="DESY" >}}The "German Electron Synchrotron" in Hamburg is a major German research center that develops and operates powerful particle accelerators to study the structure of matter and the universe, serving thousands of scientists from around the world.{{< /sidenote >}}

> _My professor at University of Hagen, and a researcher at DESY in Hamburg - the particle accelerator institute. They handle huge volumes of physics data, so UUID strategy is operationally relevant for them. He was a good supervisor. I picked the topic because it would help my professional life, not just sit in a drawer._

**And there's a paper coming out of it.**

> _I received a perfect mark, which surprised me enough that I wanted to do more with it. We're now extending the work - running the Cassandra benchmark across multiple nodes - and preparing a 12-page paper for EDBT (International Conference on Extending Database Technology) submission in June or July. If it's accepted it would be published next year._

**That's an unusual academic path for someone not heading into academia.**

> _It's not where I want to go long-term, but it was a chance I wasn't going to refuse. I picked up Go for the benchmark harness of the thesis, learned a lot about how to use AI in a research workflow, and got to build something that runs. That combination doesn't happen often as a bachelor's student._

---

## ScoreBase and Cortex

**You also run a few side projects. Walk me through them.**

> _Three of them have been active lately. The biggest is ScoreBase, at scorebase.org. It's a sheet-music search engine with semantic and natural-language search. About half a million scores indexed from six archives, covering all instruments and voice, classical through Renaissance, pop, rock - both public-domain and commercial sheet music. The metadata is normalised through an LLM, I extract features from MusicXML, and search is multilingual._

> _Then there's Cortex. It started as a "second brain" idea but it's more accurately a personal memory assistant. You capture things from a Telegram bot or the web, an LLM classifies them, you search by meaning. It exposes an MCP server so AI assistants can read, search, and write to it as a first-class tool. The point is centralising memory in something I control._

> _The UUID benchmark is the third - same code as the thesis, but a public project I keep extending._

**ScoreBase is interesting because your domain expertise in music intersects with software engineering and AI.**

> _Early on I was using the Music21 Python library to extract features from MusicXML, and I wanted to detect polyphony - whether a piece has multiple simultaneous voices. I asked the model how we could do that well, and it gave me a confident answer based on counting simultaneous notes._

{{< sidenote label="Domain Expertise" >}}Domain expertise is critical for AI because models lack real-world context and common sense. Without subject matter experts to guide them, AI systems produce generic, inaccurate, or biased outputs. Deep industry knowledge is essential for evaluating performance, guiding workflows, and saving costs.{{< /sidenote >}}

> _The actual definition of polyphony in classical music is more subtle. There's something called hidden polyphony: a single-line instrument like violin can imply two voices by alternating between a melody on top and a counter-line underneath, even though it never plays two notes at the same time. To a counterpoint analysis, that's polyphonic. To a "count simultaneous notes" algorithm, it isn't. The AI didn't know that distinction - not because it was stupid, but because I hadn't given it the context. The app is for musicians; the AI defaulted to the more common software-engineering reading of the term._

> _If I hadn't caught it, I'd have shipped a feature that excluded most of the solo violin and cello repertoire from polyphony search results. The lesson is direct: domain knowledge is what tells you when the AI's confident answer is wrong._

---

## How AI changed his workflow

**You started professional development in October 2022. ChatGPT launched at the end of November 2022. How did your workflow evolve over that time?**

> _The first year was almost entirely classical. I'd find an issue, grep through the codebase by hand, follow function names, work out which path the bug came in through. ChatGPT existed but I used it as a slightly better search engine - "how does Rack middleware work in Rails?", "what does the browser actually do with this?" - to fill in fundamentals. Not for code generation._

**Then?**

> _In the second year I started copy-pasting code into the ChatGPT interface and asking it to refactor, but the context window was small, so it was always slices. That period taught me something useful: as I got better, I started noticing when the model's suggestion was overcomplicated, and I'd push back. It became its own form of pair programming._

> _Now I use AI for almost everything. Bug fixes: I'll point Claude Code at a GitLab issue via the glab CLI and let it work. For larger features the workflow has more phases. First a brainstorm - superpowers brainstorming or similar, where the model interrogates the requirements before I write any code. Then specifications. Then I'll usually write some tests so coverage doesn't drop. Finally I let an agent generate the code, and I review._

**How much code do you actually write by hand at work now?**

> _At work, probably under ten percent. Mostly small fixes where typing is faster than describing. The rest is review. Outside work I deliberately still hand-code - Leetcode-style problems, small projects in JavaScript or Vue without AI. Partly for interview prep, since serious companies still ask you to code from scratch. Partly as recreational programming - the same way there's recreational maths or recreational music. It keeps the muscle in shape._

**What's changed about how you decide what to build?**

> _The shape of the work moved upstream. The experienced developers I learned from didn't always know exactly what they were going to build before they started - the creative process was pulled into the coding itself. You'd write something, notice it was the wrong approach, change direction, discover the shape as you went. AI doesn't really let you work that way. The model is at its best when it has full context, and "full context" means you've already specified what the end product is supposed to do, end to end, before the agent starts. That's a slower, more deliberate phase up front - much more waterfall than the way I learned. The payoff is that the implementation step is fast and the behaviour can be tested against the spec. But the centre of gravity of the job has shifted out of the code editor and into the description of what the code is supposed to do._

**You've mentioned running multiple agents in parallel.**

> _Git worktrees changed how I work. I used to live in `git checkout` and `git stash` and hated it. Now I have a bare repo with worktrees and I can spin up an agent per branch. A real example: at work I might be running a big migration on one branch, while two other branches each try a different version of a matching algorithm against the same evaluation set, with a dashboard so I can see how each ranks. I check back in, pick the winner, merge that, and discard the others. That's prototyping at a different scale than I could ever do alone._

**Claude Code versus Codex - how do you split them?**

> _I mostly use Claude Code for planning and Codex for implementation. For planning and review I stay in Claude. I also experiment with MCP servers - I've written one for Cortex and I use a few others. The Linux instinct of "build the tool to fit the workflow" carries over directly._

**Is there a downside?**

> _Yes. When an agent writes a feature I've never built before, even if I review it line by line, I don't always know why it chose this design and not that one. I lose a kind of control I can't fully articulate._

**Can you give a concrete example where that bites?**

> _The migration I mentioned earlier. I'm moving a piece of the system into the monolith, the AI has done a lot of the lifting, and at some point it ships. Then weeks pass and someone notices that a particular matching case never fires, or an approval never lands, or a candidate never hears back. Something silent. The user surfaces it as a bug and asks me what happened. I can answer them, but only by going back to the agent and reconstructing the model - because I don't carry the mental model of why this design was chosen and not another one. It feels strange, and I'm the one on the hook. If I'd hand-coded the same migration, I'd know instantly. With AI in the middle, the path to an answer is longer than it used to be._

**Could you still work without AI?**

> _My honest first answer is no. I can't really imagine it anymore. It's been about a year of Claude Code for me and it feels much longer. The thing AI gives me that I couldn't have before is speed for both planning and implementation._

---

## Tips for juniors starting out today

**You started professional development at the cusp of the AI wave. If you had to advise a student starting today, what would you tell them?**

> _Resist the urge to use AI for everything, especially while you're studying. If you have a Java course, learn Java by hand. If something asks for memory management, work through what a virtual machine is doing. The interview process for serious roles still demands hand-coded fundamentals, and more importantly, the decisions you'll make later sit on top of those fundamentals. AI helps, but you are still the one accountable for the decision._

**Anything specific to picking a first job?**

> _Small teams over big ones, if the work is real. You'll get responsibility you wouldn't see in a large company for years. You'll touch every part of the stack and your colleagues will have a personal interest in making you solid._

**What about the social side - community, hackathons?**

> _Hackathons over solo side projects. "Make a side project" is easy advice to give and hard advice to act on - most people, including me, don't sustain the motivation alone. A hackathon gives you a deadline, a team, and live feedback. You also meet people who explain their systems to you in a way that documentation never will. Community matters in the same way. Most of what I've absorbed about how to design things, how to use AI well, how to interview internationally, came from being in rooms where senior people share what they actually do._

> _There's a second thing community gave me that's harder to describe. Being around people further along recalibrates how you see yourself. I'd been heads-down at the same job for a couple of years and I still thought of myself as a junior. Conversations in those rooms made me realise I'd quietly stopped being one without noticing. That sounds small, but it changes how you present yourself, what you apply for, what you say in interviews and what you aim for._

**What about resumes?**

> _Start refining yours before you'll need to. There's a lot of YouTube content about it, but there's also something free and concrete you can do: post your CV anonymously, for example on Reddit, and ask people to grill you. You can also do it with AI; hand your CV and your project descriptions to a model and ask, "If you were a senior engineer hiring for this role, what's missing?" Or feed it your codebase including a git log and ask for a summary that will help you ask and answer better questions about your own project._

---

## Looking ahead

**What's next for you?**

> _I like to continue to learn and grow, possibly in a different domain or different environment. Getting international experience would be the dream. I've been at the same place for almost four years and I've learned a huge amount, but at some point I want a different context to learn the next thing._

**On the projects side?**

> _ScoreBase keeps growing. More archives to index, more metadata cleanup, polish, new features. I'd like to take the UUID paper through to EDBT. And I'm curious about how the workflow changes over the next year - what becomes possible with longer-running agents, with cheaper inference, with better tools for the parts of the job that are still manual._

**Still play music?**

> _The reason I studied music is the music itself. That hasn't gone away. I don't do concerts anymore, but I make music with my children and do small performances with friends on weekends. Just for fun. It's not something I see myself giving up._

**Thanks for the conversation.**

> _My pleasure._

---

## Closing comments

Two threads run through this conversation. The first is the value of late starts: Eike's path into software is unusual, but the discipline of having to earn the basics quickly - first as a working student on a small team, then through a math-heavy remote degree, accompanied by serious side projects - is exactly the discipline that AI tooling rewards. People who already know how to learn from scratch handle the new tools well. 

Notice how Eike is leveraging his domain expertise in music for at least one of his side projects. That is a real competitive advantage that must not be overlooked.

The second thread is the shape of a career that has been AI-native from day one: no "before times" to anchor against, a comfort with running parallel agents and writing specifications instead of code, and a deliberate practice of hand-coding fundamentals as a counterweight to the cognitive debt that builds up when you stop. If you are a junior trying to find footing in this environment, his advice is concrete enough to act on this week. AI amplifies your skills, which is why strong fundamentals are more important than ever. If not you, who else is going to tell the AI when it is wrong? If you are a senior engineer, reflect on how easy it is to acquire new ways of working and use it as a benchmark against your own workflows and skills, which you need to keep evolving.

## Leave a comment

If you enjoyed reading this article, Eike and I would love to hear from you.

Comment on [LinkedIn](https://www.linkedin.com/posts/fbuetow_eike-rackwitz-spent-years-as-a-professional-share-7464665765586104320-7Y8h) 

## References

* [Eike on LinkedIn](https://www.linkedin.com/in/eike-rackwitz) - Eike's LinkedIn profile.
* Eike on [GitHub](https://github.com/moguls753) (moguls753) - Eike's GitHub profile, including the ScoreBase and UUID benchmark repositories.
* [Cortex - A self-hosted personal memory assistant](https://moguls753.github.io/cortex/) - Eike's self-hosted personal memory assistant with MCP server integration, discussed in the side projects section.
* [ScoreBase - Sheet Music Search](https://scorebase.org/) - Sheet music search engine with semantic and multilingual search, built by Eike and referenced throughout the interview.
* [Music21 - A toolkit for computer-aided musicology](https://www.music21.org/) - Python library used in ScoreBase for MusicXML feature extraction, central to the polyphony detection example in the interview.
* [University of Hagen - distance-learning university](https://www.fernuni-hagen.de/) - The remote university where Eike completed his degree in mathematical software development.
* [DESY - German Electron Synchrotron](https://desy.de/index_eng.html) - Research institute in Hamburg that co-supervised Eike's bachelor's thesis on UUID benchmarking.
* [EDBT - International Conference on Extending Database Technology](https://edbt.org/) - Conference where Eike's extended UUID benchmark paper is being submitted.
