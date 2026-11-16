---
title: "Interview Series - From South Africa to London, Facebook and Hands on CTO at Escendant (AI)"
subtitle: "A hands-on CTO who never stopped coding - on twenty-six years in engineering, the cyber security through-line, and what AI is doing to the craft."
slug: "interview-series-from-south-africa-to-hands-on-cto"
date: 2026-06-12
draft: false
description: "Estee van der Walt is CTO and Principal Engineer at Escendant in London, with a PhD in AI and Cybersecurity and twenty-six years of engineering behind her. In this interview she walks through the three explicit phases of her career - apprenticeship in London, finding herself back in South Africa, and execution across Mimecast, Facebook, Nominet, and Escendant - the cyber security through-line that connects all of them, and what working with generative AI as an engineer is actually like today."
author: "Florian Buetow & Estee van der Walt"
categories: ["Interviews", "AI Engineering"]
tags: ["Interview", "Cyber Security", "Generative AI", "CTO", "Architecture", "Mentoring", "PhD"]
---

## Preamble

![Portrait of Estee van der Walt](estee-van-der-walt.webp?zoom?left "Estee van der Walt: ML/Cloud Engineer with a PhD in AI and Cybersecurity. Hands-on CTO at Escendant in London.")

Estee van der Walt is a machine learning and cloud engineer with a PhD in AI and cybersecurity.[^estee-li] Today, she serves as hands-on CTO and Principal Engineer at Escendant, a London-based AI venture building *The Human Archive* - a product focused on curating a person's personal history, reconstructing memories, and preserving voices.[^escendant]

In our conversation we trace 26 years in engineering, starting in 2000 at Liberty Global in London and Eindhoven and culminating in her current role. Between those points, she spent a decade in South Africa at a data product company serving the nation's largest banks and insurers, earned a PhD, joined Mimecast, moved to Facebook's integrity team, led architecture at Nominet, and most recently shipped *Whezit*, a privacy-focused mobile bookmarking app built nights and weekends to pressure-test AI-assisted development.[^whezit]

Her story is interesting for two reasons. First, she has always been a hands-on engineer and remained hands-on even in her role as a CTO. Second, her choices were driven by curiosity rather than a career ladder - again and again she steered toward the intersection of the things she cares about, maths, cybersecurity, AI, using each move and each round of study to get closer to the frontier. She frames the journey as three phases - apprenticeship in Europe, finding herself back in South Africa, and execution across Mimecast, Facebook, Nominet, and Escendant - with a possible fourth emerging now as AI reshapes how the work itself gets done. We talked about how she got there, the cybersecurity thread that runs through everything she has built, and what working alongside AI agents at the desk looks like today.

<!--more-->
---

## Growing Up in South Africa

**Florian:** Let's start at the beginning. You were born in South Africa, and after high school you moved to Europe, London. How did that journey start? And what made you decide to go into tech in the first place?

**Estee:** That is correct, I'm from Johannesburg. At the time my school did not offer computer science classes until quite late. When I was 16-18, I had the chance to take computer science as an after-school subject. I enjoyed it, even though it wasn't my strongest subject. Funny how things turn out.

I'll go back further, though. At 13, I did an extracurricular program where I was exposed to Logo - the turtle graphics language where you tell a virtual tortoise to move forward and turn 90 degrees to move it across a board. That fascinated me. We also had an old 386 computer at home, and I'd spend holidays writing small programs on it. I still remember one in particular, that drew a house and filled it in. I always had a logical, engineering mindset. By 16, I was doing computer science in school using Visual Basic. Simple by today's standards, but I was hooked.

In South Africa, you pick your university major when you are between 17 and 18. I wasn't sure what to pick, so I enrolled in a generic BSc covering actuarial science, accounting, and computer science.

**Florian:** Is that like a bachelor's degree?

**Estee:** Yes, a bachelor's degree in science, which in South Africa is a three-year degree. In my first year, I realized that I preferred CS. I pivoted in my second year, which was possible because I had already taken the prerequisite courses. After the third year, I added an honors year. One of my professors then asked me if I wanted to do a master's with him. But my plans were to go overseas. I had never been abroad, and many of my peers were taking the two-year working holiday visa to the UK to travel and explore the world outside of South Africa.

**Florian:** Your professor had offered to supervise a master's, but your heart was set on going overseas. What did you end up choosing?

**Estee:** I decided to stay and work on my master's part-time while I reapplied for a visa to travel. My professor specialized in computer security - firewalls and risk analysis - at a time when firewalls weren't yet standard on every network. Once I got the visa, I arranged to finish my master's remotely and started job hunting in Europe.

---

## Phase 1: The Apprenticeship in London and Eindhoven

**Florian:** You think of your career in three phases - apprenticeship, finding yourself, then execution. Let's take them one at a time. The first begins when you arrive in London with a fresh degree but almost no work experience. How did you get your foot in the door?

**Estee:** I had the degree, but almost no work experience - just the odd summer job here or there, nothing I could really point to. I quickly realized the UK values work experience heavily. For a while, I worked behind the bar at a football club, even in the yellow vest at matches, just to get by. After three months, I found a job doing Excel spreadsheets with Visual Basic for Applications. Not ideal, but you take what you can get.

I stayed there for a while, then a university contact told me his company was hiring. I jumped at it. The company was Liberty Global - formerly Telewest and UPC - one of Europe's largest network operators at the time. I worked on the TV side, as a normal junior developer. Honestly, it still wasn't real programming, but I was content, and I didn't have the ambition to push further yet - maybe it was the era; the landscape was different. Towards the end, though, I started wanting more. I pushed myself into a bit of C#, because a lot of my colleagues were working in it, and what I was doing felt too simple - like it wasn't really programming.

**Florian:** Did you ever consider returning to South Africa?

**Estee:** I thought about it, but my visa had converted to a work permit, which ties you to your employer. That made staying easier. I had good colleagues and traveled to the Netherlands regularly, doing some XML/XSL work. I don't know if you can call that programming, but it was something.

This was the first of what I now see as three career phases: a block in the UK where I was adjusting to life abroad and learning how organizations operate. Coming from South Africa, you're a bit remote - not behind, but things move at a different pace - and this was really my introduction to how the world and its organizations work. I even got British citizenship during those years; I'd been here long enough. But after seven years, I missed family and home, so I decided to go back.

---

## Phase 2: Finding Herself, Back in South Africa

**Florian:** Your profile shows a project linked to a South African bank. That connects to this phase?

**Estee:** Yes, that's the one. I'd done the UK, and the plan was to go back home and find a real programming job - not that I hadn't been programming, but I wanted more. I landed at a small, family-owned company - almost a consultancy, except they had their own data product that they installed at the client. They deployed it to South African banks and insurers; there are four big banks, and they were already at two of them, plus one of the major insurers.

It was essentially an ETL pipeline: pulling home loan and savings data, standardizing it, and running reports. My boss was strict about clean code and proper naming. That's where I learned the beauty of doing things right. I stayed for about seven or eight years. Looking back, my career seems to move in seven-year chunks.

I also did some CUDA work there. The financial modeling was too slow, so we experimented with GPU acceleration. It feels obvious now, but back then it was highly experimental. If I'd known then what I know now, I would've stayed in it.

Towards the end, I felt that familiar itch: not boredom, but a desire to push myself. A colleague was starting a master's, and I wondered about a PhD. I'd already finished my master's remotely from the UK, about ten years earlier. But by then - around 2012, 2013 - everything was about data science, and "big data" was the phrase on everyone's lips. I knew I wasn't doing any of it at work, and I felt like I was missing out. I've never liked not being at the forefront; I want to be where things are actually happening. So I contacted my old professor, and he said yes. That was me investing in structured education - not really for the degree, but to force a career shift toward machine learning.

**Florian:** You've mentioned education as a tool at inflection points. What value does it hold for you?

**Estee:** It provides structure and accountability. Today, it's easy to say, "I'll do LeetCode every day," and not follow through. A structured course with a deadline is like marathon training. It builds habit. I don't mean you need to write an exam, but I sometimes do. Before joining Escendant, I got my AWS certification to force myself into learning cloud architecture systematically. At the end, you get something tangible. Not for show, but like a personal medal.

**Florian:** You also said you wanted to be where the excitement is. Is that FOMO, or genuine curiosity?

**Estee:** Curiosity. I want to be part of things that intersect with my passions: math, cybersecurity, AI, ML. If quantum computing becomes the next big thing tomorrow, I won't chase it unless it aligns with what I care about. I've always been drawn to the intersection of machine learning and cybersecurity because I want to do good. Specifically, protect people.

My PhD focused on protecting minors on social media using Twitter data (when mining was still possible) and running experiments on a SAP HANA server in Potsdam. The PhD taught me rigor: research, verify facts, question assumptions. It also forced me to learn. This was before deep learning was mainstream. My AI work was linear regression by today's standards. I also took Andrew Ng's Stanford course on Coursera. I want to understand how things work. If someone asks how a transformer works, I can explain it, but I still dig deeper to truly know it.

---

## Phase 3: Execution at Mimecast, Facebook, Nominet, and Escendant

**Florian:** Was London still the magnet, or did you simply enjoy being in that part of the world?

**Estee:** No, I think I was looking at any place, really. I was interviewing anywhere, as long as I could do AI. I actually had an opportunity in Belgium, to go to Sony, and then Mimecast came up. I had a remote interview with Kevin and I got the job, so I thought, well, okay, I'm going to London. And London made it easy, because I had the passport, I knew the city, and I still had a bank account. It was simply an easier move than anywhere else in Europe would have been. What I didn't know at the time is that both of Mimecast's founders are South African.

That is where the third part of my career starts. If the first part was the apprenticeship, and the second was finding myself and working out what I wanted to do, then the third is execution, chasing what I want and where I want to get to.

At Mimecast I was thrown in the deep end - not in a bad way, but I had to learn very quickly how things work. It's an amazing company to work for, the culture and everything. I was in the data mining team, so I learned about really massive amounts of data, how you process it and how you analyze it. I was lucky that my team had a bit of autonomy to work on machine learning as well, because we were an analytics team, so we also looked at a bit of fraud and those sorts of things. And that intersects with cybersecurity again.

It made me think about industries. As engineers we can work in any industry, really, because you can apply programming anywhere. But I think you are drawn to certain industries more than others, based on your own ethics and your own aptitude. I like numbers, which is probably why I enjoyed the banking side of things. But I also like cybersecurity and doing good, feeling to some extent that I'm contributing to something.

**Florian:** I remember that you finished your PhD while you were at Mimecast. Did that also mark the end of your time there?

**Estee:** Yes. I'd had the same conversation with my professor as before - I'm going overseas, can I finish from there? - and he said that was fine. I took a six-month sabbatical before I left South Africa to really push the thesis to a point where it was almost finished, although it still took another two years to finish it off from the UK.

Toward the end of my time at Mimecast I still had this feeling that I wanted to work in machine learning, really machine learning, and if I had stayed I probably would have moved toward that. But there is also that thing of Big Tech. I could work for Facebook, so why not try it out, interview, and see if I can get in? I got a job there as an integrity scientist. Is that really machine learning? No. But it's cybersecurity, it's protecting people, and I knew it would be a company that works at great scale with a big impact. Not a lot of people get that opportunity, so I took it.

**Florian:** Facebook's acceptance rates are notoriously low. How did you prepare?

**Estee:** I think I was well prepared by the time I got to Facebook, because I had done a lot of interviews before that one. I interviewed at Amazon and at Twitter and didn't get those, and then in the end I got Facebook. We could talk for a long time about interviews. I don't always agree with these tests, because I think you can game them to some extent. If you put in the work you can pass the test, and that doesn't show that you can really do the job. But to get into these companies you have to put in the work just to pass the test, so I put in a lot of work.

I used *Cracking the Coding Interview*. It makes you realize that the bigger companies all have a bit of a pattern in how they interview. I also learned that you have to show your value, so that when you walk away they want to have you. It's a different type of interview.

At Facebook I learned a lot about impact. If you spend an hour on something that isn't worth it, then why are you doing it? It's a high-pressure environment, but that's why those companies are who they are. I also found that I wasn't an engineer there. I was an analyst, in a very niche integrity role. If I had stayed on I could probably have moved to the engineering side, and I did have that chat with my manager, but I just didn't see the path at that point. There are so many levels - L3, L4, L5 - that it was going to take forever to work through them. And I was by no means the cleverest person there. There are really clever people at Facebook, so I always felt like I was chasing, trying to just keep up. After a year I decided I had learned what I'd come to learn, and I went to Nominet, the UK domain registrar.

It's not a cybersecurity company as such, but I worked on protective DNS there. So again you can see the theme of cybersecurity flowing through.

**Florian:** One thing before we move on. Cybersecurity is one theme, but the other is huge amounts of data, right? It started in South Africa, then came Mimecast's scale, Facebook's scale, and now the scale of an internet registrar.

**Estee:** Yes. We're talking about things you can't do on one machine, things that need to be distributed. So it was learning about queues and Kafka, even learning about deploying things. Nominet was my first real exposure to the cloud, because our product ran on AWS, so I had to learn AWS very quickly. I was the lead architect there, which means making sure the overall design of the system is good, and I discovered that I actually like the architect role.

That period also made me see that I had always been chasing machine learning. You know the T-shaped engineer, who goes deep into one thing and knows a bit about everything else? I always felt like a jack of all trades, and I wanted to be the deep engineer. When I left Mimecast, that is what I told Kevin: "I'm a jack of all trades. I want to specialize." That's why I went to Facebook. And at Facebook I found out that I don't like doing just one thing. You are in a specific role, that's what you need to do, and you're not asked to do a bit of everything. I felt like I was almost losing my skills there.

At Nominet I saw again that I like knowing a bit of everything, and that it's actually handy, because you know the whole solution end to end. I find I can even talk to the customer, so I understand what the customer wants. I understand how the technology works, I know how to scale things, I know cybersecurity, I know databases. All these little building blocks help me to be an architect. I'm still fascinated by machine learning and the transformers underneath it, but I've accepted that it's okay if I just do that on the side, for myself.

**Florian:** That's fascinating. You went deep, found it too narrow, and went broad again. But to me it seems you always had the ability to go very deep. Everything you've described so far was technically deep.

**Estee:** Maybe I go deep, then I get bored, and then I want to go out again. I'd say I go to about 75-80% of something and then I widen out, which is probably not a bad technique, because the last 20% usually takes 80% of the effort. I do know a lot of things quite deeply. I can't always remember all of it, because there's so much, but you gain a gut instinct for where things go wrong, and if I have to deep-dive I can go where I need to go.

At Nominet I was the architecture lead, but I was also managing a lot of people, so I learned about managing people and handling difficult situations. But I wanted to get more hands-on again. I like to build things and do it myself. That's how I ended up at Escendant, a very small startup founded by Neil, whom I knew from Mimecast.

**Florian:** I remember you once saying that apparently you can't avoid getting promoted out of an engineering role, which I thought was so funny. Has that happened at Escendant too?

**Estee:** I guess that's what has happened now. But we're so small that I don't put a lot of value on the title. It's good to have, and I have a bit more responsibility because of it, but I'm still pretty much an engineer, and it's nowhere near being a VP at a larger company. I just naturally progressed to where I am the CTO, of five engineers. Now I'm pretty much the architect, the engineer, the planner, the everything. What I like about it is that because we're so small there are no meetings, and you really have the autonomy to use whatever is the best tool for the job. And we're working at the forefront of these AI models, which scratches that ML itch of mine.

**Florian:** I know what Neil's vision was when he left Mimecast: to preserve humans as a digital twin, for lack of a better word. Is that still the idea?

**Estee:** We've pivoted a little bit, although underneath that is still what we do. Now it's about curating your life, and it should be joyful to do that, and about sharing who you are, the real you, with other people. You could ask what's different from Facebook and all of them, but they accumulate data as an after-effect of other things. It's not really who you are. What we're doing is digging into memories and recreating them. If you can't remember how something looked, AI can help you, or you can hear the voices of people you haven't heard in a long time. There are various use cases. It could be just for you, it could be to share, it could be to be remembered.

And like I say, I like the autonomy. I've been with them longer than with any other company since I came to the UK, which tells you something. I don't have the itch to go somewhere else, or the feeling that I'm stuck. Not yet.

When I was thinking about tonight and the three phases, I did wonder if there's a fourth phase coming now, where AI is changing things. It doesn't mean I change my job. It means that how I work and how I approach things changes completely.

---

## Phase 4: Working with Generative AI

**Florian:** It's remarkable how much has changed in just the last year. Companies like ClickUp are laying off staff and pivoting hard to AI-first workflows instead of bolting AI onto existing ones. What do you expect is going to change going forward?

**Estee:** I don't know. I think we're in a weird state at the moment, a bit in flux. Just in the last year, I've pretty much stopped writing code from scratch. The code I do write is maybe a LeetCode problem here and there, because I felt I was losing my programming and thinking skills, and it's good exercise to still think a problem through.

My worry is that you still need the deep understanding of how things work, and I don't know if that's going to go away. It depends on how big your project is. Ours is pretty big and we are doing it with five people: two on the backend, two on the frontend, one designer, and Neil contributing on the side. We had three more people who left through natural attrition, and we decided not to replace them, because we could move fast enough as we were.

But if the context is too big, AI will give you a good solution that is not necessarily *the* good solution for you and your product and where you want to go. Only you know what your vision is. You can tell it your vision and your mission, and that might bring it a bit closer, but it still won't know everything. For example, it will go and install Kafka and completely over-engineer something that you don't need right now. It doesn't always understand that progression, that you don't need the full solution on day one and can see how things change.

So I'm giving more and more to the agent to do, but I still need to monitor what it's doing. I think that's why I liked the architect role so much. I need to understand the architecture, guide the agent to where I want it to go, and keep it in line. That might change, because these models are getting better and better. If your project is small, I think it's possible already. If it spans multiple technologies and third parties, with people adding things, I think there will always be some role for a human in the loop. We're almost becoming orchestrators.

**Florian:** Do you use one AI, or do you try to get the opinions of several?

**Estee:** We used to use Cursor, and we still have the account at work. There you have exposure to different models, and that was back when it was Claude 3.5 and GPT-4.5, when each had its own strengths. Now it feels like they are getting closer. At some point I got anxious about spending so much money on tokens. With a team license you pay per use, and I almost restricted what I was doing with AI purely because I was thinking of the cost. That wasn't a mandate from the company, just me being frugal.

Then I realized that Claude does the job for me, so I pivoted toward it. I had been using it privately for the app I built on the side. It's $100 a month, and that's more than enough for my capacity, because I don't run agents overnight doing all those clever things. But I can run three or four tasks at the same time, for 8-12 hours a day, and I have enough usage. I can go to GPT-5 if I want to, I just don't feel I have to. Where I still might is documentation, especially anything legal.

**Florian:** So what do you tell young engineers who are starting out today?

**Estee:** I think the job's not going to go away. When computer vision started, everybody said radiologists would be the first job to go, and instead, because the capability became so much better, we need more radiologists. I'm not necessarily saying we're going to need more engineers, but I don't think we're going to need no one. It's going to be a different skill, though. Knowing about systems and how things work will matter more, and so will knowing how to work with people. It's almost more of a consulting role than just sitting and programming.

**Florian:** Do you find yourself reviewing a lot of AI-generated code, or have you started to automate that as well?

**Estee:** No, I still review it, though not line by line. I review at a higher level. I typically do a lot of planning beforehand, usually two or three rounds, because the model doesn't understand the whole system, or a certain nuance, or what I wanted to achieve. Even when you put all of that into documentation there are still gaps. It implements narrowly for one problem and forgets about everything else it has done before, so you always have to remind it to generalize. I'm a big fan of reusable code. So I let it do the plan, I let it implement without interrupting, and at the end I look at the code and sense-check it. Tests are very important to me. I make sure I have tests that run, and if they pass, then I'm good.

**Florian:** You built a side project this year. Did you need to?

**Estee:** No, I didn't need to. It was twofold: to see if I could do it, and to learn about AI, because a year ago we weren't using it that much at work. I built the app on the side, starting with Sonnet 3.5, and I saw how the capabilities just improved from there. In the beginning I had to correct it a lot, and since I didn't know Swift, I was simply lost when it got things wrong, like choosing the wrong frameworks.

The other thing I want to say is to be curious. In everything I do I'm always asking why. Why is something broken? Why do I get this alert? How does this work? I'm starting a little "how does stuff work" series for myself. I know GPUs and what they do, but I want to understand them a bit more.

**Florian:** You clearly had that build-something instinct from early on, tinkering on that old 386 in the holidays. For students today trying to get a first foothold, would you recommend chasing those early summer jobs and internships, the way you did?

**Estee:** I actually would, especially now that we know how much people are struggling to find jobs. Internships are a very good way in, and they don't even have to be paid, unfortunately. If you go and say, "I'll work for you for free," someone will take you on. I see two ways of doing it. One is finding a company you like and offering them your time. The other is doing something yourself, something you're passionate about. That's what my side project was. I wanted to understand how to build an iOS app and an Android app, so I used my own project to learn. Through doing, you learn, and the good thing is that at the end you have experience and something to put on your CV.

**Florian:** There is so much information out there. I remember when data science came up, there were so many courses that it was confusing and overwhelming. What do you pick now?

**Estee:** Take Andrej Karpathy's series on makemore and how to build transformers. I've been working through it for 18 months, because there's no deadline and nothing pushing me to do it. I always feel like I'll do ten minutes tomorrow, or twenty. All the information is there on YouTube and you don't have to pay for it, but I miss the structure. That's probably why I did my PhD, and the AWS certification. Each was a focused time in my life where I had to learn. I'm at a point now where I pick things without an exam at the end, but I do still like the structure.

**Florian:** Have you spoken at conferences?

**Estee:** Nothing big, no. The most has been around 100 people. I'm not really fond of speaking, but I see the value in it, because when you present something you have to know your subject. People are going to ask you questions. I prefer mentoring, which pushes you in the same way, because to mentor somebody you have to know something about it. I've looked at the mentoring platforms, but it's a matter of time at the moment. Maybe when I want to scale down, that would be a good way to give back and to stay relevant and up to date.

One thing I do feel is different about our industry, and it's maybe advice for people going into computer science, is that it never stops. You have to continually learn if you want to stay relevant. It used to be that people worked at the big banks for their whole lives. Now people are being let go, and what skills do you have then, if you've been at one company for 20 years and haven't stayed current?

**Florian:** What do you think is next, for you and for the industry? If one can even make that projection.

**Estee:** That's a big, loaded question. In terms of job security, I'm not that worried for those of us who have been in the industry a long time, because you do need senior people who know architecture, and I think that gap will be there for a while. The automated work is being replaced, yes. But there are still a lot of companies out there on archaic systems, so far behind that they can't even move to AI yet, so I'm not worried even for junior engineers who want to come in.

You can see the trend, though. We used to do the coding ourselves. Then we were giving it to ChatGPT, saying "correct my code," and pasting it back in. Now you leave it to run, look at the result, and say, "no, change that," and I'm doing less and less even of that. So it comes down to knowing your product and your customer and what you actually want to build, so that you can give the instruction. I think that's hard for engineers, because it's not natural for us. We like to build.

**Florian:** Do you find yourself architecting the environment your agents operate in, more than working on the product they are supposed to build?

**Estee:** Some days. I don't think it's that much, but last week, for example, I spent a whole day setting up my environment a bit better. I was annoyed that every time I started from a new worktree I had to run some scripts first, and I thought, can we not automate this, so that the agent can run it without me? It does make you feel like you're automating yourself. But I've never been afraid that I'll automate myself out of a job. It's actually a lot easier to automate something when you've built it yourself. People say jobs are going to disappear, and I think your job is just going to change and look different.

It's closer to Jevons paradox, where something gets cheaper and so we use it more. As long as the technology stays affordable enough for us mere mortals to use, it will just enable us to do better. I'm positive about what can come from here. Just look at medicine and the challenges being solved there. In the last year I've seen things move more than in the previous thirty, when it felt like I was doing the same thing the whole time. Now, suddenly, how I work has changed.

**Florian:** One thing we haven't talked about is the people you met along the way. Did they help you, inspire you, shape your decisions?

**Estee:** There are very specific people who had a huge impact on different parts of my career. The first was back in South Africa, when I worked with the banks. Believe it or not, I was really shy. I never spoke in a meeting. My boss there never called me out. He listened, and in meetings he would specifically ask, "What do you think?" He made a point of getting everybody's opinion. That was a major thing for my confidence, learning that you can say something in a meeting without people thinking you don't know what you're doing.

At Mimecast it was the team, a high-performance team where everybody knew what they were doing and we learned from each other. And from Mimecast onward, managers just believed in me. Kevin gave me a chance without knowing me, because he saw something, and I'm glad he did. I worked with him again at Nominet. He's good at leaving you to do your job and nudging here and there.

Then there's Josh, a project manager at Mimecast, who became a mentor after I left. I appreciated how he approached problems and got things done. On my last day I took him for a coffee to say thank you, because I had learned a lot from him, and he said, "Do you want to stay in touch? I can mentor you if you want." We kept that up for a year, until we mutually agreed that we're still friends but it didn't have to be official anymore.

So I think it's important to identify those people and to have the courage to go and ask them, "I like what you do. Can you help me?" It works both ways. Twice in my career somebody has asked me that.

**Florian:** Do you find it gratifying to help others with your experience?

**Estee:** I do. A lot of younger people are afraid to ask. Recently somebody told me they didn't want to ask the senior engineer because he was always busy and they didn't want to annoy him. And the people who are just getting in are eager but a bit like deer in the headlights, running in every direction, so I like to talk them through it. I first have to tell them, wait, programming is very vast. Do you like data? Do you want to work on the physical chips? Do you like apps and the frontend? Even with a computer science degree, people don't always understand that there are these different areas when they go into a job. Most of us are two or three things, but we're not everything. And I think mentoring works both ways, because through teaching you learn yourself.

**Florian:** So it's fair to say you're excited about what's next with AI?

**Estee:** Yes, I am. What a time to be alive, because I don't think any of us know exactly where it's going. The opportunity is there. It can go bad and it can go good, but so can most things in life. I'm not too worried about the doom that's out there. I think people are inherently good and want to do good, and that's where my hope is.

**Florian:** That feels like the perfect place to end. Estee, thank you so much for the time and for sharing all of this - it's been a genuinely inspiring conversation.

**Estee:** Thank you, Florian - it's been a real pleasure.

---

## Closing Thoughts

Looking back at my conversation with Estee, three things stood out to me as a listener:

1. **She never stopped being an engineer.** Across two continents and six employers - Liberty Global, the South African banking-data company, Mimecast, Facebook, Nominet, and Escendant - Estee kept her hands on the code while her title kept rising. At Escendant she is CTO of a five-person team and still its architect, still the one writing and planning the work. The way she describes her own style - go about 75-80% deep on something, then widen out - is why she can talk to customers, design for scale, and lead the team at once. Cybersecurity runs underneath all of it: the firewall work in her master's, the PhD on protecting minors online, email security at Mimecast, integrity at Facebook, protective DNS at Nominet. Few engineers pair a security background with AI as deliberately as she does.

2. **She used formal study to force each pivot.** She began her PhD to push herself out of the banking-data work and into machine learning - the enrollment was really a way to commit, not a hunt for the title. She did the same before Escendant, sitting the AWS certification to make herself learn cloud architecture properly. The counterexample is the Andrej Karpathy series she admits she has been half-working through for 18 months, precisely because nothing forces her to finish it. If a course has sat open in a browser tab for a year, the fix she keeps reaching for is a deadline and something to hand in.

3. **She thinks AI may be opening a fourth phase.** It would not be a new job - just a different way of doing the one she has. Estee barely writes code from scratch now. On a normal day she keeps three or four Claude tasks running while she watches the agents and sets up the environment they operate in. What makes that work is the twenty-six years behind it: she can tell when the model is over-engineering, losing the thread of the system, or building the wrong thing for the product. The hard part is no longer the typing but knowing what should be built, and that is difficult to learn without having done the work yourself first. It is why she tells junior engineers not to skip the fundamentals.

## References

[^estee-li]: Estee van der Walt on LinkedIn. https://www.linkedin.com/in/esteevanderwalt/
[^escendant]: Escendant, "The Human Archive." https://thehumanarchive.com
[^whezit]: Whezit, Estee's privacy-focused mobile bookmarking app for iOS and Android. All data is stored locally on the device, with no account and no cloud sync. https://whiteorcaoptims.com/whezit
