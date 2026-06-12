---
title: "Interview Series - From South Africa to London, Facebook and Hands on CTO at Escendant (AI)"
subtitle: "A hands-on CTO who never stopped coding - on twenty-six years in engineering, the cyber security through-line, and what AI is doing to the craft."
slug: "interview-series-from-south-africa-to-hands-on-cto"
date: 2026-06-12
draft: true
description: "Estee van der Walt is CTO and Principal Engineer at Escendant in London, with a PhD in AI and Cybersecurity and twenty-six years of engineering behind her. In this interview she walks through the three explicit phases of her career - apprenticeship in London, finding herself back in South Africa, and execution across Mimecast, Facebook, Nominet, and Escendant - the cyber security through-line that connects all of them, and what working with generative AI as an engineer is actually like today."
author: "Florian Buetow & Estee van der Walt"
categories: ["Interviews", "AI Engineering"]
tags: ["Interview", "Cyber Security", "Generative AI", "CTO", "Architecture", "Mentoring", "PhD"]
---

## Preamble

![Portrait of Estee van der Walt](estee-van-der-walt.webp?zoom?left "Estee van der Walt: ML/Cloud Engineer with a PhD in AI and Cybersecurity. Hands-on CTO at Escendant in London.")

This conversation tracks an engineer who started professional development in 2000 at Liberty Global in London and Eindhoven, and who is now, twenty-six years later, CTO and Principal Engineer at Escendant - a London-based AI venture building The Human Archive, a product about curating your life: digging into memories, recreating them, hearing the voices of people you haven't heard. In between she went back to South Africa for a decade at a data product company serving the country's largest banks and insurers, earned a PhD in AI and Cybersecurity, joined Mimecast in London, then Facebook on the integrity team, then Nominet as lead architect on protective DNS for the UK domain. Most recently she shipped Whezit, a privacy-focused mobile bookmarking app she built on nights and weekends specifically to pressure-test AI-assisted coding.

The arc is unusual on two axes: she climbed from developer to CTO without ever stepping off the keyboard, and she frames her own career as three explicit phases - apprenticeship in London, finding herself back in South Africa, and execution across Mimecast, Facebook, Nominet, and Escendant - with a possible fourth emerging now as AI changes how the work itself gets done. Estee van der Walt is a hands-on CTO. We talked about how she got there, the cyber security thread that runs through everything she has built, and what working with AI agents at the desk looks like today.

<!--more-->
---

## Growing up in South Africa

**I would like to start us from the very beginning. My understanding is you're from South Africa, but in your 20s you went to Europe, to London. Can you tell us a little bit about how that journey started? How you came to tech.**

> _I'm from Johannesburg. We didn't have computer science at school until quite late - when I was sixteen, seventeen, eighteen I had the opportunity to take it as an extra subject after school. I took it, I enjoyed it, and coincidentally it wasn't my best subject. Strange how things work out. But I even want to go back to when I was thirteen. I did an extracurricular thing after school where I was exposed to Logo - the tortoise you tell to go forward a hundred steps and turn ninety degrees. That fascinated me. We had an old 386 at home, and I'd spend my holidays building little programs - I still remember writing one that drew a house and filled it in. I always had that logical, engineering mindset. By sixteen I was doing computer science at school in Visual Basic, which was simple by today's standards - kids at school now are far more advanced. In South Africa you pick a university at seventeen or eighteen, and I had to choose a major. I wasn't sure. So I picked a generic BSc covering three areas I could go into: actuarial science, accounting, or computer science._

**Is it like a bachelor's degree?**

> _Yes, a bachelor of science. In South Africa it's a three-year degree. In my first year computer science was one of the subjects alongside accounting, statistics, and maths, and I realised I liked it more than anything else. So I pivoted in my second year - instead of a generic bachelor's in maths, a bachelor's in computer science. I could just do it because I already had the subject. You sort of learn what you like when you start doing it. After third year I added an honours degree on top - the fourth year, which equates roughly to a European bachelor's. One of my professors then reached out and asked if I wanted to write my master's with him. But I wanted to go overseas at that point. I'd never been overseas and just wanted to see the world. A lot of my peers were doing the same, because there was a two-year working holiday visa for the UK at the time. My first visa try didn't go through. So I went back to the professor and said, okay, let's do the master's. Firewalls and risk analysis - my professor was specialising in computer security, and firewalls weren't a stock-standard part of a network yet._

**Were you using Linux? Was it already popular back then?**

> _Not at all. It was Windows all the way. Linux was around but every time I tried to install it, it was too difficult - I had to know the special commands and it always broke. At some point I had a dual-boot on my computer, but I never booted into Linux. So I stayed on Windows. The thing I really wanted was still to go overseas. While I was working on the master's I got the visa. I made an arrangement with my professor that I'd finish part-time, came over, and started looking for work. I'd never really worked in IT yet._

**You had summer jobs. They probably gave you some experience. Would you recommend somebody to do those things?**

> _I would, yes. Particularly now when people are struggling to find jobs. Internships are a very good way in, and unfortunately they don't even have to be paid - if you just go and say, I'll work for you for free, you'll find someone who'll take you on. There are two routes really. The first is finding a company you like and offering your time. The second is doing something yourself - find something you're passionate about and build it. My side project this year was exactly that. I wanted to understand how to implement an iOS app and an Android app, so I used my own project as the vehicle. Through doing, you learn. And at the end you have something to put on your CV._

---

## Phase 1: The apprenticeship in London and Eindhoven

**But you now had a computer science degree. What's the pivot, already doing your bachelor's, right? So how do you end up in London?**

> _I had the bachelor's but barely any work experience - just summer jobs here and there, nothing I could put on a CV and say I'd done. When I came over I realised very quickly that the UK rates work experience very high, so it was difficult to find a job at first. I worked behind the bar at a football club for a while, even worked the football games themselves in the yellow vest, just to get by. After about three months I finally found a job, and it was literally Excel spreadsheets. Visual Basic on Excel. Not my ideal job. I wanted to program, but you sit with that thing of, you take what you can get._

**But you did this for seven years, I think?**

> _I did the Excel job for a while, then someone I knew from university who was also in the UK said his company was looking for someone. I jumped at it, because I wanted to do something other than Visual Basic for Applications on Excel. The company was Liberty Global - it had been Telewest and UPC in the past. One of the biggest network operators in Europe at the time, I believe. I worked on the TV side. To be honest it still wasn't really programming, and I didn't have ambition to do more. I was just happy working in computer science. I wasn't striving to learn more. Maybe it was just the times - there wasn't as much going on then._

**And how was it for you to stay so far away from home? Did you never think about going back?**

> _I did think about it, but I wasn't sure. The visa had turned into a working visa - a work permit - and a work permit binds you to the company, so it made it easier just to stay. I had nice colleagues, I was travelling to the Netherlands regularly, doing a bit of programming. I don't know if you can call XML and XSL programming, but it was something. This is the first of what I think of as three phases in my career - a block in the UK where I was just enjoying life, doing a bit of computer science. Towards the end I started to want more. I pushed to do C#, started writing a small program in it, because a lot of my colleagues were working in C# and what I was doing felt like it wasn't really programming. It felt too simple._

**What was your role description in that first London job?**

> _Developer. Normal developer, I guess. Junior developer._

**Would you say the first phase, would we have to call this the apprenticeship phase?**

> _Yes, definitely. It was about getting familiar with the world, being exposed to Europe. Coming from South Africa you're a bit remote. Not behind, but things move at a different pace. I was exposed to how the world does things, how organisations work. That was my introduction to the work environment. After seven years I missed family, missed home, and decided to go back._

---

## Phase 2: Finding herself, back in South Africa

**I saw you have one project on your profile that is linked to a South African bank. Is that related?**

> _Yes, that's the one. I'd made the choice: I'd done the UK, I'd even got British citizenship in that time. The plan was to go back to South Africa and find a real programming job. The job I landed was at a small family-owned company - almost consulting, but with their own product that they deployed to banks and insurance companies. There are four big banks in South Africa, and we were already at two of them and one of the big insurers. It was a data product, basically an ETL pipeline. You'd pull in different data sources from the bank - home loans, savings accounts - into one place, standardise and generalise it, then run reporting off it. My boss was very strict about language being pure, about naming things properly. That's where I really learned the beauty of doing things right. I was there for what felt like another seven, eight years - it does feel like I have these seven-year chunks. Looking back, I actually did some CUDA work at that company too. The financial modelling was too slow, so we were trying to use CUDA for the mathematical side of things. Today that feels obvious; back then it was very experimental. If I'd only known, I would have stayed in it. Towards the end I started getting that feeling again - not bored, but wanting to push myself. One of my colleagues was starting a master's, and I was like, I wonder about a PhD. By that point I'd already finished my master's remotely from the UK, about ten years earlier. But suddenly everything was about data science and big data, and I knew I wasn't doing that at work. I'd always felt I was never at the forefront, and I wanted to be. So I contacted my old professor, and he said yes, please come do your PhD with me. That was me investing in my own education - not really for the degree, more to push myself, to have a goal, to change my career direction toward data science, or actually machine learning._

**What value does education have for you? You talked about how at the inflection points you always had a very strong feeling of wanting something more, and a very clear idea of what you wanted to go for next, except maybe in the beginning, when you went to Europe.**

> _It correlates with structure. For me education is a structured way of learning something new, and it holds me accountable. In today's world it's easy to commit verbally - I'm going to do a LeetCode puzzle every day - and not many people actually follow through. A structured course with a deadline is almost like training for a marathon. It becomes a habit. I'm not saying you need to write an exam, but I do that sometimes. Before I joined Escendant three years ago, I did my AWS certification because it was a way to force myself to learn the technology in a structured way. At the end you've got something for the work you've put in. It isn't for the world to say, look at my list of achievements. It's for myself, like a medal._

**You also said you wanted to be part of where the excitement is, what the next hot thing seems to be. Is that a feeling of missing out? Or is it more being excited and wanting to be part of it?**

> _It's more wanting to be part of it. That curiosity of how stuff works. It still has to be my passion. If quantum mechanics comes along now, or quantum computers become the next thing tomorrow, I'm not going to say that's something I'm passionate about. But if it's at the intersection of things I care about - maths, cyber security, AI, ML - then I want to know how it works. I'd always liked the intersection of machine learning and cyber security, because I want to do good in the world. That's my way of saying, can I protect people. Big data was the buzzword. The thing we settled on was protecting minors on social media. I was using Twitter data when you could still mine it, and I had a SAP HANA server in Potsdam in Germany that I could run experiments on. When you have a lot of data it doesn't fit on your machine. You either have many machines or one big one. The PhD taught me rigour - you have to research, you have to be sure about your facts. It also forced me to learn new things. This was before deep learning was really known. The AI I did was simple by today's standards, linear regression. One of the first courses I took myself was Andrew Ng's Coursera course - the Stanford one. I want to really understand how things work. If someone asks me how a transformer works, I struggle to explain it even though I know. That's what makes me almost go deeper into it, to really know how it works._

---

## Phase 3: Execution at Mimecast, Facebook, Nominet, and Escendant

**So London was still this magnet? Or was it that you really also enjoyed just being in that part of the world?**

> _I was looking at any place to go, really. I was interviewing anywhere as long as I could do AI somewhere. I had an opportunity in Belgium with Sony. Then Mimecast came up. I had a remote interview with Kevin, and I got the job. So it was London. London made it easy because I had the passport, I knew the city, I still had a bank account there. It was just easier to move back than to land somewhere new in Europe. That's where the third part of my career starts. If the first part is apprenticeship and the second is finding myself, figuring out what I actually want to do, the third is execution. Going after what I want, where I want to get to. I didn't realise at the time, but both Mimecast founders are South African._

**That also marked kind of the end of being at Mimecast, right, for you?**

> _Yes. Mimecast threw me in the deep, in a good way. I had to learn very quickly how things work. The culture was amazing. I was on the data mining team learning about massive amounts of data: how do you process it, how do you analyse it. We had a bit of autonomy as an analytics team to work on machine learning too, looking at fraud and similar things. That intersected with cyber security again, and I realised something. As engineers we can work in any industry, but you're drawn to certain ones based on your own ethics and aptitude. I like numbers, which is probably why I enjoyed banking. But I also like cyber security and doing good. To some extent it feels like I'm contributing to something. I did a quick progression of different jobs at Mimecast - I can ramp up quickly and get to where I want to be. The PhD finished while I was at Mimecast. I had the same arrangement with my professor as before: I'm going overseas, can I finish overseas. He said yes, that's fine. I took a six-month sabbatical to really push the thesis, although it still took another two years to finish off after I left the country. The end of the PhD also marked the end of Mimecast for me. I always had this feeling that I wanted to do machine learning, really machine learning. If I'd stayed at Mimecast I probably would have moved towards that. But there was also the thing of, you know, you've got the big seven, and I could work for Facebook. Let's try it out, interview, see if I can get in._

**The acceptance rates are incredibly low. I think it's more difficult to get into Facebook than into Harvard or something. How did you prepare?**

> _Well, that makes me feel good. I think I was well prepared. I did a lot of interviews before Facebook. I had interviews at Amazon, at Twitter - I didn't get those - and in the end, I got Facebook. I don't always agree with these tests, honestly. You can game them to some extent: if you put in the work, you can pass the test and it doesn't always show that you can really do the job. But unfortunately, to get into these companies you have to put in the work to pass the test. So I did._

**I remember you were using one of the classic books, right, for the preparation?**

> _Yes, Cracking the Coding Interview. It teaches you something useful: the Facebooks, the Googles, all of them, they have a bit of a pattern in how they interview. You also realise you have to show your value. You have to make them want you. It's a shift, a different type of interview. At Facebook I learned a lot about impact and working on impactful things. If you spent an hour on something that wasn't worth it, why were you doing it. Very high pressure environment. But that's why those companies are who they are. I also realised I wasn't really an engineer there. I was just an analyst. Very niche. It was in cyber security, integrity work, and probably if I'd stayed on I could have moved to the engineering side. I did have that chat with my manager, but I just didn't see the path completely. There are so many levels - L3, L4, L5 - it would have taken forever to work through. And by any means I'm not the cleverest person there. There are really clever people. I always felt like I was chasing, trying to just make it. After a year I took the decision for myself: I've learned what I'm going to learn here. So I went to Nominet, the DNS registrar for the UK domain. Not a cyber security company as such, but I worked on protective DNS. Cyber security again. You can see the whole flow, the theme of cyber security running through everything I've done._

**One thing before we pivot again. The theme is now cyber security, but also huge amounts of data, right?**

> _Yes. You can't do that work on a single machine, it has to be distributed. Learning about queues, about Kafka, about deploying things. At Nominet I got my first exposure to the cloud, because our product ran in AWS. I had to learn AWS very quickly. I was the lead architect there, making sure the overall system design was good. And I realised I actually liked the architect role. That period made me realise something else too. I'd always been chasing machine learning, machine learning. There's this idea of the T-shaped engineer, deep in one thing and broad across many. I always felt like I was a jack of all trades and I wanted to be the deep engineer. When I left Mimecast I told Kevin exactly that. I'm a jack of all trades, I want to specialise. That's why I went to Facebook. Then at Facebook I realised I don't actually like doing just one thing. You're in a specific role, you're not asked to do a lot of everything. I felt like I was losing my skills there, because I was so ingrained in just one thing. At Nominet I realised again that I like knowing a bit of everything. It's actually handy. You know the solution end to end. I can talk to the customer. I understand what the customer wants, how things work technically, how to scale, cyber security, databases - all the little building blocks. That's what makes me more of an architect, knowing a bit of everything. I still love machine learning and deep learning. I'm still fascinated by transformers underneath. But I realised it's okay if I do that on the side, for myself._

**It seems you always had the ability to go very deep. Everything you've described so far was technically deep.**

> _Maybe I go deep and then I get bored and want to go out again. I'd say I go to about seventy-five or eighty percent of something, and then I'm like, okay, breadth again. I do know a lot of things quite deeply. I can't always remember it - there's too much - but I have a gut instinct for where things are wrong, and if I need to deep-dive I can go where I need to go. At Nominet I was also managing a lot of people. I was the architecture lead, but with management on top. I learned about managing people, difficult situations and less difficult ones. But I wanted to be more hands-on again. I like being hands-on. I want to build it, I want to do it myself. That's why I'm now back working at a company founded by Neil, who I knew from Mimecast._

**I remember you saying that apparently you cannot avoid getting promoted out of an engineering role. I thought that was so funny.**

> _Yes, that's what's happened at Escendant too. But we're so small that I don't put a lot of value on the title. It's good to have it, but I'm still pretty much an engineer. I have a bit more responsibility because of the title, but it's nowhere near being a VP at Mimecast or a CTO somewhere bigger. I just naturally progressed to CTO. We are five engineers. Now I'm the architect, the engineer, the planner, everything. What I like is that because we're so small there are no meetings. You really have autonomy to use whatever tool is best for the job. And we're working on the forefront of these AI models, which is grabbing that ML itch I've always had._

**Basically the vision was to preserve humans as a digital twin, for lack of a better word, right?**

> _Yes, that's the underlying idea, although we've pivoted a little. Now it's more about curating your life - and it should be joyful in the curating. Sharing who you are with other people, the real you. Facebook and all of them accumulate data, but it's just the after-effect of things. It's not really who you are. What we're doing is digging into memories, recreating them. If you can't remember what something looked like, AI can help you. Hearing voices of people you haven't heard. Use cases vary. It could be just for you, it could be to share, it could be to be remembered. I like the autonomy. I've been with them now the longest of any company since I've been in the UK, which tells you something. I don't have the itch to go somewhere else. Not yet._

---

## Phase 4: Working with Generative AI

**Companies like ClickUp announced they laid off 20% of their people and are now doing an extremely hard pivot toward AI-first workflows versus attaching AI on top of existing workflows, which has been the recipe for a lot of failures. What do you expect is going to change going forward?**

> _We're in a weird state at the moment. It's a bit in flux. Just in the last year I'm not writing any code anymore. The code I write is maybe LeetCode here and there. I'm not as good as you doing it daily. I try because I actually felt like I was losing my programming skills and my thinking skills. LeetCode is good as mental exercise, just to think through a problem. What worries me is that you still need the deep understanding of how things work, and I don't know if that's going to go away. It depends on how big your project is. Our project is big and we're doing it with five people: two back-end, two front-end, one designer, and Neil on the side, who is also an engineer now. We actually had three more people, and through natural attrition they've gone. We just decided not to hire more, because we can go where we need to go. If your context is too big, AI will give you a good solution. But it's not necessarily the good solution for you, your product, and where you want to go. Only you know what your vision is and what your mission is. AI might bring it closer to what you want, but it might still not know everything. For example it will install Kafka where you're completely over-engineering something that's not for now. It doesn't always understand progression. You don't have to have the full solution now. You need to progress and see how things change. I'm giving more and more to the agent to do, but I still need to monitor what it's doing. That's why I like the architecture role I had before. I need to understand the architecture and guide it on where I want it to go, and keep it in line. These models are getting better and better. If your project is small, I think it's possible. If it spans multiple technologies, third parties, more people adding things, I think you're always going to have a human in the loop. We're almost becoming an orchestrator._

**Do you use one AI? Or do you try to get multiple different AIs' opinions?**

> _We used to use Cursor. We still have the account at work. There you've got exposure to different models, and that was still when it was Claude 3.5 and GPT 4.5 and things. Each one had its strengths. Now it feels like they're getting closer to each other. At some point I got anxious about how much money and tokens I was spending. I wanted to use AI more, but with Cursor on a team licence you pay per use, and I almost restricted what I was doing purely because I was thinking about cost. It wasn't a mandate from the company, just me being frugal. Then I realised Claude does the job for me. So I pivoted towards Claude. I'd been using it privately on my own app on the side, and it's a hundred dollars a month for more than enough tokens for my capacity. I don't run agents overnight doing all the clever things you guys do. But I realised I can run three or four tasks at the same time, eight to ten to twelve hours a day, and I have enough usage. So I use Claude at the moment. I can go to GPT-5 if I want to, I just don't feel I have to. Where I might is documentation. For legal documentation or something I do feel GPT might be better._

**So you asked the question yourself, what do you tell young people?**

> _I think the job isn't going to go away. I saw something today about radiologists. When computer vision started, everyone was saying radiologists would be the first job to go. And actually, because the capability got so much better, we need more radiologists. I'm not necessarily saying we're going to need more engineers, but I don't think we're going to need none. I do think it's going to be a different skill. That's why I think systems matter, knowing about systems and how things work, and also how to work with people. It's almost more of a consulting role than just sitting and programming. The way it works is changing._

**Do you find yourself reviewing a lot of AI-generated code? Or did you also start to automate that, use agents for that?**

> _I still review it pretty much. I don't review line by line. I'll review more at a high level. I typically do a lot of planning beforehand. I usually have to do two or three rounds of planning because the model isn't understanding the whole system, or it's not understanding a certain nuance of what I wanted to achieve. Even when you put everything in documentation there are gaps. It tries to implement narrowly for one thing and forgets everything else it's done before. You always have to remind it to generalise. I'm a big fan of code reusability. So I let it run, do the plan, let it implement, and I don't really interrupt it during the implementation. At the end I just look at the code, the depth of what it's generated, and do a sense check. Tests are very important. I focus on having tests that run, and if they pass, I'm good._

**You did the side project this year. Do you need to?**

> _Yes, I did. No, I don't, I don't. But it was twofold: to see if I could do it, and through doing it I learned about AI. We weren't using it that much at work a year ago. I did it on the side and went through Sonnet 3.4, then 3.5, and I saw how the capabilities just improved. In the beginning I had to correct it a lot. Not knowing Swift, I was lost. It got things wrong so many times, choosing the wrong frameworks, that sort of thing. The other thing I want to say is, be curious. Through everything I do I'm always asking the question of why. Why is something broken? Why do I get this alert? Or how does stuff work? In a week or two I'm working on a "how does stuff work" series for myself. I'm going to start doing things like how do GPUs work. I know what they do, I just want to understand a bit more._

**When data science came up, there were so many courses, so much information, completely confusing and overwhelming. What do you pick now to do?**

> _If you think about Andrej Karpathy, his whole series of Make More and how to do transformers. I'm busy working through it. I've been busy with it for the last year and a half, because there's no deadline, nothing pushing me to do it. I always feel like I'll do ten minutes tomorrow, or twenty. The information is there. YouTube has a lot of it, you don't have to pay for stuff, but I sometimes feel like I miss structured things. That's probably why I did my PhD to learn data science and AI and move towards that. It was a focused time in my life where I had to learn that. The AWS course too. I'm just at a point now where I'm picking things where I don't have to write an exam necessarily. But I do like the structure of things._

**You went to a conference with 500 people?**

> _No, I haven't. Most was about a hundred. I'm not really fond of speaking, but I do realise the value in it. I think I like mentoring. Mentoring is a different way, where mentoring somebody also pushes you to know something about it. There are various ways to do this if you want to know more._

**Mentoring is interesting. There are a couple of platforms where you can be a mentor, or you can also get advice from a mentor, like SMNT. Have you used any of those platforms, or have any experience with them?**

> _No, I've looked at it. It's just time at the moment. Too many things to do. I was thinking though, maybe when I want to scale down, that's actually a good way to give back, to stay involved, stay relevant and up to date. One thing I do feel is that our industry is different, and that's maybe some advice for people going into computer science: it never stops. You have to continually learn, stay up to date with the latest technology, if you want to stay relevant. Otherwise you can go and work in a big corporate and do your job for thirty years. It used to be a thing at big banks, where people worked there their whole life. And that's it. But people are being let go now, and it makes you nervous. What skill do you have if you've worked at one company for twenty years and haven't stayed relevant?_

**So what do you think is next for you and for the industry? If one can even make that projection.**

> _It's a very big loaded question._

**Or what is your human judgment or feeling? Maybe there isn't real evidence to support it, but we all kind of have a gut feeling.**

> _In terms of job security, those of us who've been in the industry a longer time, I'm not that worried. You do need senior people with the knowledge of architecture and the rest, and that's going to be a gap for a while. The automated stuff is being replaced, that's where things are going. But there are still a lot of companies so far behind on AI that there are still jobs there. Even for juniors who want to come in. I look at companies that are still on archaic systems and just not even able to move to AI yet. The trend is clear though. We used to do the coding, then we started giving it to ChatGPT and saying correct my code, paste it back. Now you leave it, look at it, say no, change that. I'm doing less and less of that. It almost becomes about knowing your product and your customer and what you actually want to build, so you can give the instruction rather than build it yourself. That's hard for engineers because that's not natural for us. We like to build._

**Have you observed, is it something where you suddenly find yourself architecting the environment in which your agents operate, more than working on the actual product that the agents are supposed to be building?**

> _Some days, some days. I don't think it's that much, but I did, for example, last week, spend all day just architecting my environment to set it up a bit better. I was annoyed that every time from a worktree I had to run some scripts first to get my environment set up. Can we not automate this, and have it so the agent can run it itself, I don't have to run it for it. So yes, it makes you think you're almost automating yourself. But one thing I'm thinking now is I'm never afraid that I'll automate myself out of a job somehow. Everything is automated already. It's actually a lot easier to automate because it has your signature on it._

**Is it called Simpson's paradox, where when something gets cheaper, it gets used more?**

> _I think so. There are different opinions about all of this. Things will get cheaper and cheaper, so cheap that we don't need money really anymore, that much money. But that's doom and gloom. As long as it stays cheaper and they can serve it, it's a new technology that just enables us to do better. I'm positive about what can come from here. You look medically at the challenges that are being solved. It's exciting times. In the last year I have not seen things move as much as in the previous thirty years. The previous thirty felt the same for me. I was doing the same thing. Now suddenly my job has changed, how I work._

**One thing we didn't talk about is people you've met on your path. You talked a little bit about your professor. What would you say about those people? Have they helped you? Did they inspire you? Were they instrumental in your decision forming?**

> _I have very specific people in mind who had a huge impact on various parts of my career. The first was back in South Africa when I worked at the bank. My one boss there - and believe it or not, I was really, really shy. I never spoke in a meeting. He didn't call me out, he actually listened to me, and specifically in meetings he'd ask, what do you think? He made a point of getting everybody's opinion. My confidence was a major thing he helped me with. Realising you can say something in a meeting and not feel like people are going to think you don't know what you do. At Mimecast it was the team, a high-performance team where everybody knew what they were doing. It was a good symbiosis of learning from each other. From Mimecast onwards, managers just believed in me. Kevin. I've worked with him at Nominet again, that was the link. He's somebody who gave me a chance at Mimecast without really knowing me. He just saw something, and I'm glad he took a chance on me. He's good at leaving you to do your job and nudging here and there. So definitely, you need people along the way. Also at Mimecast there was Josh, one of the project managers, who became a mentor of mine after I left. I saw how he approached problems. He's a project manager, a product manager, but I appreciated how he got things done._

**So you just stayed in contact, you reached out?**

> _Basically, yes. When I left, the day I left, I took him for a coffee. I wanted to say thank you, because I learned a lot from him. He said, do you want to stay in touch? I can mentor you if you want. I don't do it usually. So we stayed in touch for a year afterwards. Then we got to a point where we mutually said, okay, we're still friends but we don't have to officially be in a mentor relationship anymore. I think it's important to identify those people and have the courage to go and ask them. I like what you do. Can you help me? I've had the opportunity twice in my career where somebody asked me, can you help me. So it works both ways. It's good._

**Do you find it gratifying to help others with your experience?**

> _Yes, I do. A lot of especially younger people might be afraid to ask. I like to talk them through it. They're still eager and they don't know - they're a bit like deer in headlights, running in any direction, and I have to first tell them, okay wait, programming is very vast. You have to think, do you like data? Do you like silicon, do you want to do the physical chips? Do you like the apps, the front end? Sometimes people don't understand even at university - even though you do a computer science degree, they don't understand when they go into a job that there are these different areas. If you have to classify yourself, what type of engineer are you? Backend, front-end, ML? Most of us are two or three things. We're not everything. Mentoring works both ways. I've always helped people, even at school. But through teaching, you learn yourself. It makes you think about things._

**So it's fair to say you're excited about what's next with AI?**

> _Yes, I am. I think it's exciting. What a time to live at the moment. None of us know exactly where it's going. The opportunity is there. Yes, it can go bad, it can go good. But most things in life can go either way. I'm not too worried about the doom out there. I just think the good is more than that, because people inherently are good and want to do good. So my hope is in that._

**Anything else you wish to share? Otherwise I'll stop the recording.**

> _No, I think that is it. Thank you._

---

## Closing comments

Three threads run through this conversation.

The first is continuity. Estee moved across two continents and a sequence of companies - Liberty Global, then back to South Africa for the banking data work, then Mimecast, Facebook, Nominet, and now Escendant - but she stayed an engineer throughout. The seniority climbed; the keyboard never went away. Even now as CTO of a five-person company, she is by her own account the architect, the engineer, the planner, and everything in between. Her self-described pattern is to go to seventy-five or eighty percent of something and then break for breadth, and the result is an engineer who knows enough things well enough to talk to a customer, scale a system, and run a team. Cyber security is the through-line from her master's onward, connecting the firewall work, the PhD topic on protecting minors on social media, Mimecast email security, Facebook integrity, and Nominet's protective DNS. Notice how she leverages her cyber security background and her PhD in AI deliberately, choosing roles where the two intersect. That is a real competitive advantage that should not be overlooked.

The second thread is structured education as a self-investment tool. The PhD she started while working at the South African bank was not really about the degree. It was a forcing function, like training for a marathon, to push herself toward AI and machine learning. She did the same thing again before joining Escendant with her AWS certification, and she contrasts it with the Karpathy YouTube series she has been "busy with for the last year and a half" because there is no deadline. The lesson is direct: if you find yourself drifting on a playlist you have had open for a year, give yourself a deadline and a thing to hand in.

The third thread is what AI is doing to the work itself. Estee floats this as a possible fourth phase in her career: not a new job, but a new operating mode. She is not writing code by hand anymore. She is running three or four tasks at the same time on Claude, eight to twelve hours a day, monitoring what the agent does and architecting the environment it operates in. She is doing it from a position of long experience. She can spot when the model is over-engineering, when it is forgetting context, when it is making the wrong choice for her product. The bottleneck has moved from typing to product judgement, and that judgement is hard to acquire without a body of work behind you. For junior engineers her answer is consistent with what other senior people have been saying: do not skip the fundamentals. The senior judgement that orchestrates an agent today rests on a foundation you can only build by doing the work yourself, at least at first.

[Comment on LinkedIn](TODO-linkedin-post-url-once-published)

## References

[^estee-li]: Estee van der Walt on LinkedIn. https://www.linkedin.com/in/esteevanderwalt/
[^escendant]: Escendant, "The Human Archive." https://thehumanarchive.com
[^whezit]: Whezit, Estee's privacy-focused mobile bookmarking app for iOS and Android. All data is stored locally on the device, with no account and no cloud sync. https://whiteorcaoptims.com/whezit
