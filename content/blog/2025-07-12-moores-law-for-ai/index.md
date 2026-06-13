---
title: "Moore's Law for AI?"
date: 2025-07-12
draft: false
slug: moores-law-for-ai
description: "An exploration of how AI is moving beyond monolithic models, mirroring the CPU's shift from single-core to multi-core, and what the future of multi-agent AI systems looks like."
author: "Florian Buetow"
readTime: "12 min read"
categories: ["AI Engineering"]
tags: ["AI", "LLM", "Scaling", "Multi-Agent Systems", "Moore's Law", "Dennard Scaling", "Mixture of Experts", "AI Architecture", "Agents"]
---

## From Single-Core Limits to Multi-Agent Systems

Moore's Law \[1\] fueled decades of computing progress by predicting the doubling of transistor density approximately every two years. For a long time, this translated into rapid gains in CPU speed-until thermal limits and the end of Dennard scaling hit. At that point, the industry pivoted: instead of faster single cores, we got multicore processors.

AI seems to be approaching a similar transition point. While model sizes have grown exponentially, the returns on intelligence are proving sub-linear. We are now in a resource-constrained environment where the brute-force scaling of the past few years is no longer economically or practically viable. This pressure is forcing an architectural pivot. What comes next might not be another order-of-magnitude increase in model parameters but a shift in architecture. Just like CPUs went multicore, AI is going to find a way to continue to scale intelligence.

<!--more-->

### Podcast

If you prefer listening over reading, check out this podcast episode where the topic is explored in more detail.

<audio controls style="width:100%" preload="none">
  <source src="moores_law_for_ai.mp3" type="audio/mpeg">
  Your browser does not support the audio element.
</audio>

## Moore's Law and the Pivot to Multicore

Moore's Law originally described a hardware phenomenon-transistor density doubling on silicon chips every 18 to 24 months. For decades, this increase drove exponential improvements in CPU performance. By the early 2000s, Dennard scaling-the principle that shrinking transistors keeps power density constant-failed. As transistors miniaturized, leakage currents drove up power density, causing excessive heat. Voltage couldn't be scaled down further without compromising performance, and raising voltages to boost clock speeds intensified thermal issues, capping single-core CPU performance.

Instead of abandoning the trajectory of improvement, the industry shifted strategies. By introducing multi-core processors, designers preserved the performance scaling curve through parallelism rather than clock speed. The gains continued - Moore's Law still held in one sense: the number of transistors on a chip continued to double approximately every 18 to 24 months. But instead of using those transistors to make a single core faster, chip designers began using them to add multiple cores on the same chip. The performance scaling remained, but the architecture had fundamentally changed. And as a result, the way we write software started to change. To fully leverage the available computing power, programs were increasingly designed to be multithreaded, enabling them to run tasks in parallel across multiple cores.

It is fair to say the end of Dennard scaling \[2\] marked a pivotal shift in computing that allowed performance to continue to scale.

Similarly, for AI intelligence, particularly in the context of large language models (LLMs), we are reaching a point where simply scaling up model size and computational resources is hitting diminishing returns. And naturally we may ask, what the bottlenecks are in scaling artificial intelligence this time, and what paradigm shift could enable us to scale something else instead of relying on single, monolithic LLMs?

## Bottlenecks in Scaling Artificial Intelligence for LLMs

Scaling AI performance, especially for LLMs, faces several key limitations that mirror the challenges single-core CPUs encountered:

1.  **Diminishing Returns from Model Size and Data**

    As LLMs grow larger, adding more parameters or training on more data does not yield proportional improvements in intelligence. The gains in performance (e.g., accuracy or generalization) taper off, while the computational and data requirements increase exponentially \[29, 30\]. This suggests that simply making models bigger is no longer an efficient path to greater intelligence. Research has shown that while scaling up models does improve performance, there are clear signs of diminishing returns, and the benefits can plateau, especially when using synthetic data \[31\].

2.  **Energy and Computational Costs**

    Training and running massive LLMs demand enormous computational power and energy, making further scaling costly and environmentally unsustainable \[32, 33\]. This parallels the power and heat constraints that ended Dennard scaling for CPUs, where even as transistors got smaller, their power density ceased to decrease, leading to a heat bottleneck \[34, 35\]. For instance, training a single large AI model can emit more than 626,000 pounds of carbon dioxide, equivalent to the lifetime emissions of five cars \[32\].

3.  **Data Quality and Availability**

    LLMs rely on vast, high-quality, and diverse datasets to perform well. However, sourcing and curating such data at the necessary scale is increasingly difficult \[36\]. Researchers predict that the stock of high-quality text data may be exhausted soon, a problem often referred to as the "data wall" \[40\]. Furthermore, models are at risk of "data contamination," where they are inadvertently trained on data that is similar to the benchmarks used to evaluate them, leading to inflated performance metrics \[38\].

4.  **Architectural Constraints**

    The transformer architecture, foundational to most LLMs, has inherent inefficiencies, such as quadratic complexity with sequence length \[39\]. The self-attention mechanism, a core component of transformers, requires computations that scale quadratically with the length of the input sequence. This means that doubling the input length quadruples the computation time, making it very expensive to process long contexts \[40\].

5.  **Lack of Flexibility and Modularity**

    Monolithic LLMs are trained end-to-end as single units, making it hard to update, specialize, or adapt them to new tasks without retraining the entire model \[41\]. This rigidity hampers scalability and practical deployment, as continuous updates and maintenance are challenging and costly in production environments \[42\]. In contrast, more modular approaches like Mixture-of-Experts (MoE) are gaining traction because they allow for more efficient scaling and specialization \[43\].

6.  **Evaluation Challenges**

    As LLMs grow more capable, measuring their intelligence becomes trickier. Current benchmarks may not fully capture general intelligence, and many are suffering from "benchmark saturation," where models have become so good at the specific tasks that the benchmarks are no longer effective at differentiating between them \[44, 45\]. This complicates efforts to assess whether scaling efforts are truly effective. These bottlenecks are indicators that the single-model scale-up strategy is running out of steam and that the current approach of building ever-larger monolithic LLMs could be nearing its limits \[46\]. Therefore, just as the CPU industry found its solution in parallelism, the AI field is finding its own in modularity and more holistic scaling strategies that include "scaling down" (improving efficiency) and "scaling out" (distributed and modular systems) \[46\].

These bottlenecks are indicators that the single-model scale-up strategy is running out of steam and that the current approach of building ever-larger monolithic LLMs could be nearing its limits. Therefore, just as the CPU industry found its solution in parallelism, the AI field is finding its own in modularity.

## Paradigm Shift: Modular, Composable AI Systems

Just as multi-core CPUs enabled continued performance gains by distributing tasks across multiple specialized cores, the future of scaling AI intelligence lies in moving away from single, monolithic LLMs toward **modular, composable AI systems**. In fact, this shift is something we are already beginning to see: systems composed of many specialized, sometimes smaller models that work in concert. Here are some real-world examples:

## Key Features of Modular AI Systems

1.  **Specialized Modules - Mixture-of-experts (MoE) architectures**

    Instead of one massive model, AI systems consist of smaller models or modules, each specialized for a particular task or domain. A real-world example is Google's Pathways system \[4\], which aims to build a single model that can generalize across tasks by activating only relevant parts of the network. Similarly, Anthropic's Claude \[5\] leverages specialized prompt pipelines internally to modularize processing across contexts. Developers now have access to robust frameworks that streamline the creation of mixture-of-experts (MoE) architectures \[3\]. For instance, Hugging Face Transformers \[6\] makes it straightforward to fine-tune and deploy task-specific models for areas like natural language processing or computer vision. DeepSparse \[7\] optimizes sparse neural networks for efficient module activation, and Megatron-LM \[8\] simplifies the training of large-scale MoE models, enabling systems that dynamically route tasks to specialized components with precision.

2.  **Dynamic Composition - Multi-agent planners and tool-using LLMs**

    Modules are combined dynamically based on the task, with a lead agent coordinating specialized sub-agents or tools in real time. A real-world example is **xAI's Grok** \[9\], which assists astronomers by dynamically assembling AI agents to handle specific tasks. For instance, when analyzing telescope data, a lead agent delegates subtasks like image processing to a computer vision agent, data retrieval to a database query agent, and orbital calculations to a numerical computation agent. These agents collaborate seamlessly, using tools like star catalog APIs and mathematical solvers, adapting to the user's query in real time. Building dynamic multi-agent systems is made easier by a range of intuitive tools designed for collaborative workflows. LangGraph \[10\], for example, allows developers to create graph-based systems that coordinate multiple LLMs and tools effectively. AutoGen \[11\] supports the design of lead agents that manage specialized sub-agents, while CrewAI \[12\] offers a practical way to build multi-agent systems, enabling smooth task delegation and real-time collaboration for complex applications.

3.  **Parallel and Distributed Processing**

    Multi-agent frameworks like OmniNova \[13\] or LAMs (Large Agentic Models) \[14\] distribute cognitive tasks across a hierarchy of agents or across devices. These architectures allow different agents to handle subtasks like retrieval, reasoning, and planning simultaneously, speeding up overall system throughput. A variety of frameworks make it practical to develop systems that handle parallel and distributed processing for scalable AI workloads. Ray \[15\], for instance, simplifies distributed task execution across multiple agents or devices, making it well-suited for large-scale multi-agent systems. TensorFlow Distributed \[16\] supports parallel training and inference for AI models, and Apache Spark \[17\] efficiently manages large datasets, complementing agent-based workflows by enabling concurrent processing across diverse environments.

4.  **Unified Knowledge Access: Shared Memory and RAG**

    Modular systems require efficient knowledge sharing to function effectively. This is achieved through two primary patterns: structured memory systems, such as MIRIX \[18\], which provide persistent context accessible across modules, and retrieval-based approaches like RAG \[19\], which fetch relevant external knowledge at inference time using tools like LlamaIndex \[20\] or Haystack \[21\].

5.  **Hybrid Approaches**

    Systems like Voyager \[22\] combine neural language models with symbolic planning and reinforcement learning to create agents that autonomously explore environments (e.g., in Minecraft) and write their own code. Another example is DeepMind's AlphaCode \[23\], which integrates neural models with search-based planning for programming tasks. A collection of versatile tools supports the creation of hybrid systems that integrate neural, symbolic, and reinforcement learning approaches. Gymnasium \[24\], developed by OpenAI, provides reinforcement learning environments that work well with LLMs for exploratory tasks like those in Voyager. LangChain \[25\] enables the integration of LLMs with symbolic reasoning tools and external APIs, supporting hybrid systems for tasks like code generation. Stable Baselines3 \[26\], a library for reinforcement learning algorithms, also facilitates the development of hybrid systems by providing reliable RL components that complement neural models.

### The benefits are obvious

Modular AI systems offer clear advantages in scalability, efficiency, flexibility, and interpretability. By structuring intelligence as a set of specialized, cooperating components, these architectures avoid the rigidities and inefficiencies of monolithic models. Tasks are distributed, computation is targeted, and individual parts can evolve independently-just as in software engineering. This modularity also benefits AI developers: monitoring becomes more granular, debugging is localized to specific modules, and updates or patches can be deployed without touching the entire system.

That doesn't mean this architectural shift is trivial to implement. It introduces new complexities in system design, module coordination, and communication overhead. Standards for interoperability and benchmarking are still maturing. But just as multicore CPUs required a rethink in how software was written and executed, modular AI will require us to rethink how we build, compose, and evaluate intelligent systems.

### Scaling Intelligence not just compute

Evidence shows that multi-module systems meaningfully boost intelligence - not just raw capability. For example:

- Anthropic's research leverages a lead agent and multiple specialized subagents operating in parallel. It records a 90%+ uplift over a solo Claude Opus 4 model on complex research tasks \[47\], demonstrating how structured collaboration between models unlocks deeper understanding.

- AgentGroupChat‑V2 uses a divide-and-conquer mechanism across agent groups, achieving 91.5% on GSM8K (+5.6 points), nearly doubling accuracy on AIME, and 79.2% pass@1 on HumanEval-without scaling the model size \[48\].

- A survey of multi-agent LLMs \[49\] shows consistent gains in reasoning, programming, and summarizing tasks thanks to diverse agent perspectives and agent feedback loops-even small multi-agent setups outperform individual models.

What we've seen so far aren't just implementation hacks. They reflect a shift in thinking: from "How do I make one model smarter?" to "How do I compose intelligent behavior from systems?" These architectures enable us to scale capabilities horizontally by combining specialized components, rather than vertically by growing a single LLM monolith.

---

## Implications for AI Engineers

### Focus Shift

For engineers, the focus shifts from writing single prompts to designing and orchestrating intelligent systems. The unit of work is no longer the model; it is the system. This architectural shift requires moving beyond hyperparameter tuning to mastering system composition, tackling integration complexity, and designing for emergent behavior. This shift introduces challenges-particularly in integration and complexity-that require practical strategies and innovative design principles. To achieve seamless integration of modules, engineers should emphasize robust communication protocols and coordination mechanisms. This can be accomplished using standardized APIs, message-passing systems, or event-driven architectures. Likewise, tackling the complexity of interactions among numerous modules demands modular design principles, visualization tools to track interactions, and logging, monitoring, and automated testing frameworks to identify and fix issues early. All of these techniques are well established and time-tested software engineering practices that are as essential for building reliable and maintainable AI systems as they are for other software systems.

### Staying Current

Given the rapid evolution of AI, experimentation is key to staying not only ahead but current. Engineers should explore new techniques and approaches to keep pace with the field's advancements. Early adopters gain an edge because they are the ones who will be able to decide which techniques and frameworks to adopt in production and which to revisit later when they are more mature. Beyond addressing these challenges, engineers should embrace system composition to orchestrate multiple agents or subsystems effectively and experiment with new libraries hands-on. They must shift focus toward inference-time architecture rather than relying solely on pretraining scale, explore memory-aware and sparsity-first designs to optimize (e.g., with libraries like SparseML \[27\] or Mem0 \[28\]), and plan for heterogeneous models that communicate and cooperate seamlessly (e.g., utilizing frameworks like Ray \[15\] or Hugging Face Transformers \[6\]). The next breakthrough in AI will come not from deeper networks but from systems designed to collaborate more intelligently.

---

## Implications for AI Leadership

### Focus Shift

The shift toward modular, system-level AI also brings new considerations and clarity for engineering leadership. Traditional team structures built around training or maintaining a single model must evolve. Teams need to be organized around system capabilities-reasoning, retrieval, interaction-not just around specific models. Leadership must prioritize hiring for complementary expertise, such as distributed systems, orchestration, memory management, LLM application building, and evaluating agents.

### Cultural Shift

Equally important is the cultural shift: embracing experimentation, iteration, and interface standardization over centralized, top-down control of a single model pipeline. AI projects are not software projects - even if they share many practices - management of AI projects is fundamentally different because of the probabilistic nature of LLMs. They require an iterative and experimental, trial-and-error approach to testing a model's capabilities and ensuring its output aligns with user intent. For leaders, this means cultivating a culture of iteration, trust in experimentation, and feedback-driven refinement across all stages of the AI system development lifecycle.

Leaders must foster collaboration between traditionally siloed roles-ML engineers, backend developers, and infra specialists-to deliver cohesive, modular AI systems that are robust and maintainable.

### Portfolio Mindset

Finally, AI leaders must rethink roadmap planning. Scaling via a monolith involves a linear growth mindset: more data, more compute, and bigger models. Modular AI requires a portfolio mindset: which subsystems need to be optimized or swapped? Which new capabilities should be integrated? This demands cross-functional coordination and a more architectural view of progress.

## Conclusion

Moore's Law didn't end-it evolved. The exponential curve lived on through architectural change. AI might be at that same inflection point. If so, the future belongs not to the biggest model but to the best system of models, aka the best agents.

---

## Resources

1.  [Cramming more components onto integrated circuits (Moore, G. E., 1965)](https://download.intel.com/newsroom/2023/manufacturing/moores-law-electronics.pdf)
2.  [Dennard scaling - Wikipedia](https://en.wikipedia.org/wiki/Dennard_scaling)
3.  [Adaptive Mixture of Local Experts (Jacobs, R. A., et al., 1991)](https://www.cs.toronto.edu/~hinton/absps/amle.pdf)
4.  [Pathways: A next-generation AI architecture](https://blog.google/technology/ai/pathways-next-generation-ai-architecture/)
5.  [Anthropic | Claude](https://www.anthropic.com/claude)
6.  Hugging Face Transformers [GitHub](https://github.com/huggingface/transformers) Repository
7.  [DeepSparse (Note: Deprecated by Neural Magic post-Red Hat acquisition)](https://pypi.org/project/deepsparse/)
8.  [NVIDIA Megatron-LM](https://nvidia.github.io/Megatron-LM/index.html)
9.  [xAI | Grok](https://x.ai/grok)
10. [LangGraph: Multi-Agent Workflows](https://www.langchain.com/langgraph)
11. Microsoft AutoGen [GitHub](https://github.com/microsoft/autogen) Repository
12. CrewAI [GitHub](https://github.com/joaomdmoura/crewAI) Repository
13. [OmniNova: A Generalist World Model for Tool-Augmented Agent](https://arxiv.org/abs/2406.06834)
14. [What are Large Agentic Models (LAMs)?](https://www.tech4future.com/en/large-agentic-models-lams/)
15. [What is Ray? - Anyscale](https://www.anyscale.com/ray-overview/what-is-ray)
16. [Distributed training - Databricks](https://docs.databricks.com/en/machine-learning/train-model/distributed-training/index.html)
17. [Apache Spark](https://spark.apache.org/)
18. [MIRIX: A Multi-Agent Transpiler for Information Retrieval Systems](https://huggingface.co/papers/2407.03983)
19. [Retrieval-augmented generation - Wikipedia](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
20. [LlamaIndex](https://www.llamaindex.ai/)
21. [Haystack | The Open Source LLM Framework](https://haystack.deepset.ai/)
22. [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://voyager.minedojo.org/)
23. [AlphaCode 2 Technical Report - Google DeepMind](https://storage.googleapis.com/deepmind-media/AlphaCode2/AlphaCode2_Tech_Report.pdf)
24. [Gymnasium - An API for Reinforcement Learning (Farama Foundation)](https://gymnasium.farama.org/)
25. [LangChain Documentation](https://www.langchain.com/docs)
26. [Stable Baselines3 - Docs](https://stable-baselines3.readthedocs.io/en/master/)
27. SparseML [GitHub](https://github.com/neuralmagic/sparseml) Repository (Note: Deprecated by Neural Magic post-Red Hat acquisition)
28. Mem0 - The Memory Layer for Language Models [GitHub](https://github.com/mem0ai/mem0) Repository
29. [Position: Enough of Scaling LLMs! Let's Focus on Downscaling – arXiv (Sengupta, A., Goel, Y., & Chakraborty, T., 2025)](https://arxiv.org/abs/2505.00985)
30. [Scaling Laws of Synthetic Data for Language Models – arXiv (Zhu, Z. et al., 2025)](https://arxiv.org/abs/2503.19551)
31. [AI Large Language Models: new report shows small changes can reduce energy use by 90% – UNESCO (2025)](https://www.unesco.org/en/articles/ai-large-language-models-new-report-shows-small-changes-can-reduce-energy-use-90)
32. [Explained: Generative AI's environmental impact – MIT News (January 17, 2025)](https://news.mit.edu/2025/explained-generative-ai-environmental-impact-0117)
33. [Dennard scaling – Wikipedia (2024)](https://en.wikipedia.org/wiki/Dennard_scaling)
34. [Looking beyond Dennard Scaling – Rambus (2016)](https://www.rambus.com/blogs/looking-beyond-dennard-scaling-2/)
35. [LLM Data Quality: Old School Problems, Brand New Challenges – Gable.ai (January 22, 2025)](https://www.gable.ai/blog/llm-data-quality)
36. [What Happens When LLM's Run Out Of Useful Data? – Forbes (June 25, 2025)](https://www.forbes.com/sites/sap/2025/06/25/what-happens-when-llms-run-out-of-useful-data/)
37. [An Overview of Data Contamination: The Causes, Risks, Signs, and Defenses – Holistic AI (July 16, 2024)](https://www.holisticai.com/blog/overview-of-data-contamination)
38. [On The Computational Complexity of Self-Attention – PMLR (Duman-Keles, C., 2023)](https://proceedings.mlr.press/v201/duman-keles23a.html)
39. [The Problem with Quadratic Attention in Transformer Architectures – Weights & Biases (2024)](https://wandb.ai/wandb_fc/tips/reports/The-Problem-with-Quadratic-Attention-in-Transformer-Architectures--Vmlldzo3MDE0Mzcz)
40. [Monolithic Code vs. Modularized Code: Choosing the Right Fit for Your AI Project – DEV Community (Lima, C., 2024)](https://dev.to/limacodes/monolithic-code-vs-modularized-code-choosing-the-right-fit-for-your-ai-project-dl)
41. [The Challenges of Deploying LLMs – A3Logics (2024)](https://www.a3logics.com/blog/challenges-of-deploying-llms)
42. [Mixture of Experts LLMs: Key Concepts Explained – Neptune.ai (2024)](https://neptune.ai/blog/mixture-of-experts-llms)
43. [Avoiding Common Pitfalls in LLM Evaluation – HoneyHive (2024)](https://www.honeyhive.ai/post/avoiding-common-pitfalls-in-llm-evaluation)
44. [Language model benchmark – Wikipedia (2024)](https://en.wikipedia.org/wiki/Language_model_benchmark)
45. [Will LLMs Scaling Hit the Wall? Breaking Barriers via Distributed Resources on Massive Edge Devices – arXiv (Zhang, Y. et al., 2024)](https://arxiv.org/abs/2403.08223)
46. [Position: AI Scaling: From Up to Down and Out – arXiv (Bansal, H. et al., 2024)](https://arxiv.org/abs/2402.01677)
47. [How we built our multi-agent research system](https://www.anthropic.com/engineering/built-multi-agent-research-system)
48. [AgentGroupChat-V2: Divide-and-Conquer Is What LLM-Based Multi-Agent System Need](https://arxiv.org/abs/2506.15451)
49. [A Survey on Large Language Model based Autonomous Agents](https://arxiv.org/abs/2308.11432)
