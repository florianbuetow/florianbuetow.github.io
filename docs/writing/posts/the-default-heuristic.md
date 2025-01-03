---
authors:
- fb
categories:
- System Design
date: 2025-02-01
description: Explore the Default Heuristic for choosing tech in production environments,
  balancing innovation with stability.
draft: false
slug: the-default-heuristic
tags:
- System Design
---

# How to Choose Tech for Production: The Default Heuristic

## Introduction

During my time as a lead data engineer to build a predictive maintenance platform I came across the concept of the default heuristic. One of my tasks was to identify platform components that would allow us to scale storage and retrieval of time series sensory data to petabytes, while still being able to support critical use cases of data scientists as well as analytical reporting.

<!-- more -->

I am not the first one to tell you that from a developer perspective using the latest cutting edge tech for the job seems like a great idea. After all, new tech usually looks great on paper, and is fun to learn and experiment with. However, for production systems that require long-term stability, maintainability, and reliability, the smarter choice often lies in opting for established, proven solutions. This approach is choosing the "Default Heuristic".

## Understanding the Optimization Fallacy

The Optimization Fallacy refers to the misguided pursuit of the "perfect" or "optimal" solution, often at the expense of time, resources, and clarity. Developers are particularly susceptible due to their innate curiosity and love for problem-solving.

**Why it happens:**

- **Excessive Tinkering:** The thrill of exploring cutting-edge tools.
- **Delusion of Discoverability:** Believing the best option will reveal itself with exhaustive research and trials.
- **Premature Optimization:** Attempting to solve problems that haven't yet occurred.

The fallacy: This relentless chase can delay progress, inflate costs, and introduce unnecessary complexity instead of identifying the optimal solution for the use-case.

## The Default Heuristic

The Default Heuristic on the other hand is a decision-making strategy that prioritizes established, reliable choices over the pursuit of novel or untested alternatives. It is particularly beneficial when:

1. **Costs of New Information are High:** Researching and testing new tools consumes time and resources (e.g., extensive benchmarks for five different databases, redesigning a pipeline to work with an unproven tool, or rewriting major parts of an application to fit a new framework).
2. **Consequences of Deviation are Low:** The safe, default choice is unlikely to lead to catastrophic outcomes (e.g., sticking with REST APIs rather than trying GraphQL for the first time).
3. **Variability in Outcomes is Minimal:** The range of potential results from using the default is narrow and predictable (e.g., using AWS S3 for object storage rather than testing a newer, less mature cloud storage service).

## Real world examples

### How pinterest scaled from 0 to 10s of billions of page views per month

Pinterest's system design evolution is a great example of the efficacy of the Default Heuristic in decision-making. Initially, during their rapid growth phase, Pinterest integrated a variety of - at that time - cutting-edge technologies, including Cassandra and MongoDB, in an attempt to manage their expanding infrastructure. However, this approach led to increased complexity and system failures. Pinterest recognized these challenges and shifted focus to mature, reliable technologies such as MySQL, Solr, Memcache, and Redis. This strategic pivot allowed them to scale effectively by adding more of the same components, thereby simplifying their architecture and enhancing system stability.

This case illustrates the pitfalls of the Optimization Fallacy—pursuing novel solutions without fully considering the associated costs and complexities. By using the Default Heuristic, they reduced avoided unnecessary experimentation with unproven tools, and employed established technologies that offered predictable performance and robust community support. Their decision minimized the risks associated with excessive tinkering and premature optimization, ultimately contributing to their successful scaling and operational efficiency. \[[1](#references)\]

### StackOverflow Update: 560M Pageviews a Month, 25 Servers, and It's All About Performance

Overflow's infrastructure strategy is another example of the application of the Default Heuristic. By favoring established, reliable technologies such as Microsoft IIS for web servers and MS SQL for database management, they ensured system stability and performance. Additionally, they pragmatically incorporated Linux-based solutions like HAProxy for load balancing and Redis for caching where appropriate. In my opinion this shows a balanced approach to technology selection. The deliberate choice to utilize proven technologies, instead of pursuing novel or untested alternatives, has Default Heuristic written all over it. And by doing that they got reliability and predictability in their system design. \[[2](#references)\]

## Conclusion

SQL Databases seem to be a common theme in the above examples, but you get the idea. There is a default heuristic for many areas of tech: Programming languages, Webframeworks, CD/CI SAAS, Data Storage, Project management tools, the list goes on. To summarize:

### When to Use the Default Heuristic

1. **Resource-Constrained Projects:** Limited budgets and tight deadlines benefit from predictable outcomes (e.g., using JavaScript with Node.js for a web application rather than experimenting with a newer runtime like Deno).
2. **Critical Applications:** Reliability outweighs innovation in high-stakes environments (e.g., choosing Python over a niche language for a healthcare application requiring heavy compliance with legal standards).
3. **Rapid Scaling:** When scaling a system, adopting a well-documented technology eases the learning curve (e.g., opting for Kubernetes over a less established container orchestration platform).
4. **Unclear Long-Term Requirements:** Opting for a default allows flexibility as needs evolve (e.g., choosing PostgreSQL over a specialized database when future workloads are uncertain).

### Why Use the Default Heuristic?

- **Proven Reliability:** Battle-tested solutions are trusted by a broader community.
- **Rich Ecosystem:** Established tools offer extensive documentation, community support, and real-world use cases.
- **Talent Availability:** It’s easier to find skilled professionals experienced with widely adopted technologies.
- **Risk Reduction:** Sticking with the familiar reduces operational uncertainty.

### How to Balance Exploration and Defaults

If you have capacity and talent to experiment with new tech, you should aim to:

- **Reserve Defaults for Production:** Use proven tech for core systems where failure is costly.
- **Experiment in Sandboxes:** Explore new tools in isolated environments without risking operational stability.
- **Debias Decision-Making:** Acknowledge cognitive biases, like the Optimization Fallacy, and prioritize pragmatism.

## TLDR

Use the default heuristic to:

1. **Prioritize Stability:** Choose technologies with a track record of reliability for critical systems.
2. **Minimize Risks:** Avoid falling for the Optimization Fallacy by relying on well-understood solutions.
3. **Leverage The Community:** Established tools have extensive support networks, reducing implementation and troubleshooting costs.

**By embracing the Default Heuristic, you balance innovation with stability. Let the safe, predictable defaults power your production systems, and channel your curiosity and creativity into exploratory projects where the stakes are lower.**

## References

\[1\] Y. Nelapati and M. Weiner, "Scaling Pinterest - From 0 to 10s of Billions of Page Views a Month in Two Years," High Scalability, Apr. 15, 2013. [www.highscalability.com](https://highscalability.com/scaling-pinterest-from-0-to-10s-of-billions-of-page-views-a/)

\[2\] M. Cecconi and N. Craver, "StackOverflow Update: 560M Pageviews a Month, 25 Servers, and It's All About Performance," High Scalability, Jul. 21, 2014. [www.highscalability.com](https://highscalability.com/stackoverflow-update-560m-pageviews-a-month-25-servers-and-i/)