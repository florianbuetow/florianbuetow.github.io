---
title: >-
  Interview Series - Working with an SRE
date: 2025-01-12
updated: 2025-01-12
authors:
- fb
- pb
categories:
- Interviews
description: >-
  Explore insights from Paul Bütow on SRE practices, automation, collaboration,
  and the role of AI in engineering. Read more!
draft: false
slug: working-with-an-sre-interview
tags:
- Site Reliability Engineering
- Automation
- Runbooks
- Collaboration
- AI in SRE
---

# Interview Series: Working with an SRE

## Preamble 
In this insightful interview, Paul Bütow, a Principal Site Reliability Engineer at Mimecast, shares over a decade of experience in the field. Paul highlights the role of an Embedded SRE, emphasizing the importance of automation, observability, and effective incident management. We also focused on the key question of how you can work effectively with an SRE weather you are an individual contributor or a manager, a software engineer or data scientist. And how you can learn more about site reliability engineering.

<!-- more -->
---

## Introducing Paul

**Hi Paul, please introduce yourself briefly to the audience. Who are you, what do you do for a living, and where do you work?**

> _My name is Paul Bütow, I work at Mimecast, and I’m a Principal Site Reliability Engineer there. I’ve been with Mimecast for almost ten years now. The company specializes in email security, including things like archiving, phishing detection, malware protection, and spam filtering._

**You mentioned that you’re an ‘Embedded SRE.’ What does that mean exactly?**

> _It means that I’m directly part of the software engineering team, not in a separate Ops department. I ensure that nothing is deployed manually, and everything runs through automation. I also set up monitoring and observability. These are two distinct aspects: monitoring alerts us when something breaks, while observability helps us identify trends. I also create runbooks so we know what to do when specific incidents occur frequently._

> _Infrastructure SREs on the other hand handle the foundational setup, like providing the Kubernetes cluster itself or ensuring the operating systems are installed. They don't work on the application directly but ensure the base infrastructure is there for others to use. This works well when a company has multiple teams that need shared infrastructure._

---

## How did you get started?

**How did your interest in Linux or FreeBSD start?**

> _It began during my school days. We had a PC with DOS at home, and I eventually bought Suse Linux 5.3. Shortly after, I discovered FreeBSD because I liked its handbook so much. I wanted to understand exactly how everything worked, so I also tried Linux from Scratch. That involves installing every package manually to gain a better understanding of operating systems._

**And after school, you pursued computer science, correct?**

> _Exactly. I wasn’t sure at first whether I wanted to be a software developer or a system administrator. I applied for both and eventually accepted an offer as a Linux system administrator. This was before 'SRE' became a buzzword, but much of what I did back then-automation, infrastructure as code, monitoring-is now considered part of the typical SRE role._

---

## Roles and Career Progression

**Tell us about how you joined Mimecast. When did you fully embrace the SRE role?**

> _I started as a Linux sysadmin at 1&1. I managed an ad server farm with hundreds of systems and later handled load balancers. Together with an architect, we managed F5 load balancers distributing around 2,000 services, including for portals like web.de and GMX. I also led the operations team technically for a while before moving to London to join Mimecast._

> _At Mimecast, the job title was explicitly 'Site Reliability Engineer.' The biggest difference was that I was no longer in a separate Ops department but embedded directly within the storage and search backend team. I loved that because we could plan features together-from automation to measurability and observability. Mimecast also operates thousands of physical servers for email archiving, which was fascinating since I already had experience with large distributed systems at 1&1. It was the right step for me because it allowed me to work close to the code while remaining hands-on with infrastructure._

**What are the differences between SRE, DevOps, SysAdmin, and Architects?**

> _SREs are like the next step after SysAdmins. A SysAdmin might manually install servers, replace disks, or use simple scripts for automation, while SREs use infrastructure as code and focus on reliability through SLIs, SLOs, and automation. DevOps isn’t really a job-it’s more of a way of working, where developers are involved in operations tasks like setting up CI/CD pipelines. Architects focus on designing systems and infrastructures, such as load balancers or distributed systems, working alongside SREs to ensure the systems meet the reliability and scalability requirements. The specific responsibilities of each role depend on the company, and there is often overlap._  

**What are the most important reliability lessons you’ve learned so far?**

> _Don’t leave SRE aspects as an afterthought. It’s much better to discuss automation, monitoring, SLIs, and SLOs early on. Traditional sysadmins often installed systems manually, but today, we do everything via infrastructure as code-using tools like Terraform or Puppet._
> _I also distinguish between monitoring and observability. Monitoring tells us, 'The server is down, alarm!' Observability dives deeper, showing trends like increasing latency so we can act proactively._
> _SLI, SLO, and SLA are core elements. We focus on what users actually experience-for example, how quickly an email is sent-and set our goals accordingly._
> _Runbooks are also crucial. When something goes wrong at night, you don’t want to start from scratch. A runbook outlines how to debug and resolve specific problems, saving time and reducing downtime._

---

## Anecdotes and Best Practices

**Runbooks sound very practical. Can you explain how they’re used day-to-day?**

> _Runbooks are essentially guides for handling specific incidents. For instance, if a service won’t start, the runbook will specify where the logs are and which commands to use. Observability takes it a step further, helping us spot changes early-like rising error rates or latency-so we can address issues before they escalate._


**When should you decide to put something into a runbook, and when is it unnecessary?**

> _If an issue happens frequently, it should be documented in a runbook so that anyone, even someone new, can follow the steps to fix it. The idea is that 90% of the common incidents should be covered. For example, if a service is down, the runbook would specify where to find logs, which commands to check, and what actions to take. On the other hand, rare or complex issues, where the resolution depends heavily on context or varies each time, don’t make sense to include in detail. For those, it’s better to focus on general troubleshooting steps._  

**How do you search for and find the correct runbooks?**

> _Runbooks should be linked directly in the alert you receive. For example, if you get an alert about a service not running, the alert will have a link to the runbook that tells you what to check, like logs or commands to run. Runbooks are best stored in an internal wiki, so if you don’t find the link in the alert, you know where to search. The important thing is that runbooks are easy to find and up to date because that’s what makes them useful during incidents._  

**Do you have an interesting war story you can share with us?**

> _Sure. At 1&1, we had a proprietary ad server software that ran a SQL query during startup. The query got slower over time, eventually timing out and preventing the server from starting. Since we couldn’t access the source code, we searched the binary for the SQL and patched it. By pinpointing the issue, a developer was able to adjust the SQL. This collaboration between sysadmin and developer perspectives highlights the value of SRE work._

---

## Working with Different Teams

**You’re embedded in a team-how does collaboration with developers work practically?**

> _We plan everything together from the start. If there’s a new feature, we discuss infrastructure, automated deployments, and monitoring right away. Developers are experts in the code, and I bring the infrastructure expertise. This avoids unpleasant surprises before going live._

**How about working with data scientists or ML engineers? Are there differences?**

> _The principles are the same. ML models also need to be deployed and monitored. You deal with monitoring, resource allocation, and identifying performance drops. Whether it’s a microservice or an ML job, at the end of the day, it’s all running on servers or clusters that must remain stable._

**What about working with managers or the FinOps team?**

> _We often discuss costs, especially in the cloud, where scaling up resources is easy. It’s crucial to know our metrics: do we have enough capacity? Do we need all instances? Or is the CPU only at 5% utilization? This data helps managers decide whether the budget is sufficient or if optimizations are needed._

**Do you have practical tips for working with SREs?**

> _Yes, I have a few:_
>
> 1. **Early involvement**: Include SREs from the beginning in your project.
> 2. **Runbooks & documentation**: Document recurring errors.
> 3. **Try first**: Try to understand the issue yourself before immediately asking the SRE.
> 4. **Basic infra knowledge**: Kubernetes and Terraform aren’t magic. Some basic understanding helps every developer.

---

## Using AI Tools

**Let’s talk about AI. How do you use it in your daily work?**

> _For boilerplate code, like Terraform snippets, I often use ChatGPT. It saves time, although I always review and adjust the output. Log analysis is another exciting application. Instead of manually going through millions of lines, AI can summarize key outliers or errors._

**Do you think AI could largely replace SREs or significantly change the role?**

> _I see AI as an additional tool. SRE requires a deep understanding of how distributed systems work internally. While AI can assist with routine tasks or quickly detect anomalies, human expertise is indispensable for complex issues._

---

## SRE Learning Resources

**What resources would you recommend for learning about SRE?**

> _The Google SRE book is a classic, though a bit dry. I really like 'Seeking SRE,' as it offers various perspectives on SRE, with many practical stories from different companies._

**Do you have a podcast recommendation?**

> _The Google SRE prodcast is quite interesting. It offers insights into how Google approaches SRE, along with perspectives from external guests._

---

## Blogging

**You also have a blog. What motivates you to write regularly?**

> _Writing helps me learn the most. It also serves as a personal reference. Sometimes I look up how I solved a problem a year ago. And of course, others tackling similar projects might find inspiration in my posts._

**What do you blog about?**

> _Mostly technical topics I find exciting, like homelab projects, Kubernetes, or book summaries on IT and productivity. It’s a personal blog, so I write about what I enjoy._

---

## Wrap-up

**To wrap up, what are three things every team should keep in mind for stability?**

> _First, maintain runbooks and documentation to avoid chaos at night. Second, automate everything-manual installs in production are risky. Third, define SLIs, SLOs, and SLAs early so everyone knows what we’re monitoring and guaranteeing._

**Is there a motto or mindset that particularly inspires you as an SRE?**

> _"Keep it simple and stupid"-KISS. Not everything has to be overly complex. And always stay curious. I’m still fascinated by how systems work under the hood._

**Where can people find you online?**

> _You can find links to my socials on my website [paul.buetow.org](https://paul.buetow.org)._
> _I regularly post articles and link to everything else I’m working on outside of work._

**Thank you very much for your time and this insightful interview into the world of site reliability engineering**

> _My pleasure, this was fun._

## Closing comments

Dear reader, I hope this conversation with Paul Bütow provided an exciting peak into the world of Site Reliability Engineering. Whether you’re a software developer, data scientist, ML engineer, or manager, reliable systems are always a team effort. Hopefully, you’ve taken some insights or tips from Paul’s experiences for your own team or next project. Thanks for joining us, and best of luck refining your own SRE practices!

---

_All content comes directly from the recorded conversation and reflects Paul’s personal experiences and views._

## Links and Resources

- Paul's Website: [https://paul.buetow.org](https://paul.buetow.org)
- Paul's Blog: [https://foo.zone](https://foo.zone)

- The Google SRE Book: [https://sre.google/books/](https://sre.google/books/)
- Seeking SRE Book: [https://www.oreilly.com/library/view/seeking-sre/9781491978856/](https://www.oreilly.com/library/view/seeking-sre/9781491978856/)
- SRE Prodcast: [https://sre.google/prodcast/](https://sre.google/prodcast/)
- LFS Linux [https://linuxfromscratch.org](https://linuxfromscratch.org)