---
title: "uv - An Extremely Fast Python Package and Project Manager, Written in Rust"
date: 2025-02-23
draft: false
slug: dev-tools-uv
description: "Discover uv, an ultra fast package manager for Python that simplifies dependency management and enhances project setup efficiency."
author: "Florian Buetow"
readTime: "5 min read"
categories: ["Tools"]
tags: ["Python", "uv", "Rust", "Package Manager", "pip", "virtualenv", "Astral", "Docker"]
---

There exist a broad selection of package managers that manage virtual environments and packages for us. Some of the most popular ones are [conda](https://anaconda.org/anaconda/conda), [pip](https://pypi.org/project/pip/) and [virtualenv](https://virtualenv.pypa.io/en/latest/) or [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/). They can almost all do the same things:

- Install packages
- Resolve dependencies
- Managing package versions
- Managing virtual environments

<!--more-->

## Why uv?

You might ask yourself the question of why do we need yet another tool for this? Because it is faster and faster is better. How fast you ask? Between 10 and 100x faster, depending on the task. Besides that it is also fun to use and support something new. But before we get started with some examples, let's go over the key design decisions that make uv so fast.

## Installation

Before we get into the details of uv, if you want to follow along, you can install uv for your OS by following [the official installation guide](https://docs.astral.sh/uv/getting-started/installation/).

## Design Decisions

- uv comes as a standalone binary and was written in Rust
- uv uses a global module cache, that prevents re-downloading of packages when you set up a new project on the same machine
- During download packages are written directly to disk without memory overhead (Copy-on-Write)
- uv is a drop-in replacement for pip, pip-tools and can manage virtual environments like virtualenv and conda.

Next, let's go through the most important commands and at the end we'll upgrade the [Arxiv Publications Tracker](https://github.com/florianbuetow/arxiv_publications_tracker) to use uv instead of pip.

## The most important commands

<table>
<thead>
<tr>
<th>Command</th>
<th>Description</th>
<th>Example</th>
<th>Parameters/Notes</th>
</tr>
</thead>
<tbody>
<tr>
<td>uv pip</td>
<td>Drop-in replacement for pip commands</td>
<td><code>uv pip install requests</code></td>
<td>Accepts all standard pip arguments and flags</td>
</tr>
<tr>
<td>uv pip compile</td>
<td>Resolves dependencies and creates requirements.txt</td>
<td><code>uv pip compile requirements.in</code></td>
<td><code>requirements.in</code> contains direct dependencies without versions (e.g., "requests\nflask"). The output <code>requirements.txt</code> will contain all dependencies with pinned versions</td>
</tr>
<tr>
<td>uv pip sync</td>
<td>Installs packages from requirements.txt</td>
<td><code>uv pip sync requirements.txt</code></td>
<td>Ensures exact versions from requirements.txt are installed. Will remove packages not in requirements.txt</td>
</tr>
<tr>
<td>uv venv</td>
<td>Creates a new virtual environment</td>
<td><code>uv venv</code></td>
<td>Creates in current directory as <code>.venv</code> by default. Use <code>--path</code> to specify different location</td>
</tr>
<tr>
<td>uv sync</td>
<td>Syncs the dependencies to the virtual environment</td>
<td><code>uv sync</code></td>
<td>Reads from <code>requirements.txt</code> or <code>pyproject.toml</code>. Use <code>--python</code> to specify Python version</td>
</tr>
<tr>
<td>uv add</td>
<td>Adds a package to the dependencies</td>
<td><code>uv add requests</code></td>
<td>Can specify version constraints (e.g., <code>requests&gt;=2.28.0</code>). Updates requirements files automatically</td>
</tr>
<tr>
<td>uv remove</td>
<td>Removes a package from the dependencies</td>
<td><code>uv remove requests</code></td>
<td>Removes both the package and its unused dependencies</td>
</tr>
<tr>
<td>uv list</td>
<td>Lists all installed packages</td>
<td><code>uv list</code></td>
<td>Use <code>--freeze</code> to output in requirements.txt format</td>
</tr>
<tr>
<td>uv run</td>
<td>Runs a Python script in an isolated environment</td>
<td><code>uv run script.py</code></td>
<td>Creates temporary venv with dependencies from <code>requirements.txt</code> or <code>pyproject.toml</code>. Use <code>--python</code> to specify version</td>
</tr>
</tbody>
</table>

### About pyproject.toml

The `pyproject.toml` file is a standardized configuration file for Python projects (defined in [PEP 518](https://peps.python.org/pep-0518/)). When using uv, this file can specify your project's dependencies instead of using requirements.txt. Here's an example:

    [project]
    name = "my-project"
    version = "1.0.0"
    dependencies = [
        "requests>=2.28.0",
        "flask~=2.0.0",
        "pandas>=2.0.0"
    ]

    [project.optional-dependencies]
    dev = [
        "pytest>=7.0.0",
        "black>=23.0.0"
    ]

The advantages of using pyproject.toml include:

- Single source of truth for project metadata and dependencies
- Support for optional dependency groups (like development tools)
- Better integration with modern Python packaging tools
- Ability to specify build requirements and project metadata

When using uv commands like `uv sync` or `uv run`, it will automatically detect and use dependencies specified in either pyproject.toml or requirements.txt, with pyproject.toml taking precedence if both exist.

In our demo we'll skip creating a pyproject.toml file and only use requirements.txt.

## Demo

The [Arxiv Publications Tracker](https://github.com/florianbuetow/arxiv_publications_tracker) is a very simple tool you can use to find new papers on [arXiv.org](https://arxiv.org) matching your search criteria. I use it to find new papers on LLM driven AI Agents.

The tool runs inside a Docker container, and it uses pip to fetch python dependencies.

Our original `Dockerfile` looks like this:

    # Use a minimal Python 3.11 image
    FROM python:3.11-slim

    # Set the working directory
    WORKDIR /app

    # Copy the script into the container
    COPY arxiv_tracker.py /app/arxiv_tracker.py
    COPY requirements.txt /app/requirements.txt

    # Install dependencies
    RUN pip install -r requirements.txt

    # Run the script as the entrypoint
    ENTRYPOINT ["python", "/app/arxiv_tracker.py"]

Our `requirements.txt` file contains the dependency to the arxiv python package:

    arxiv

To upgrade this project to uv we'll need to install uv in the docker container and then modify the `RUN pip install -r requirements.txt` command.

Since we know uv pip is a drop-in replacement for pip we simply change the command

    RUN pip install -r requirements.txt

to

    RUN uv pip install -r requirements.txt

If you want to install uv on your machine follow the installation guide for uv on [PyPi](https://pypi.org/project/uv/) or [Astral.sh](https://docs.astral.sh/uv/).

If we run the build script `./build_and_run.sh` we get the following error:

    => ERROR [arxiv_watchdog 5/5] RUN uv pip install -r requirements.txt
    0.250 /bin/sh: 1: uv: not found

It seems that uv is not part of our docker base image `python:3.11-slim` and therefore not found when we try to run it. This can easily be fixed, because uv can be installed using pip, and we know we already had pip available in the container.

We simply have to add the following line to our Dockerfile, before we can use uv.

    RUN uv pip install -r requirements.txt

If we run the build script again, we see a different error:

     => ERROR [arxiv_watchdog 6/6] RUN uv pip install -r requirements.
     .351 error: No virtual environment found; run `uv venv` to create an environment, or pass `--system` to install into a non-virtual environment

This is because uv requires us to create a virtual environment or explicitly specify `--system` if we don't want to use one. Since we have nothing else running in the docker container, we'll be fine using --system.

The updated and final version of our Dockerfile looks like this:

    # Use a minimal Python 3.11 image
    FROM python:3.11-slim

    # Set the working directory
    WORKDIR /app

    # Copy the script into the container
    COPY arxiv_tracker.py /app/arxiv_tracker.py
    COPY requirements.txt /app/requirements.txt

    # Install dependencies
    RUN pip install uv
    RUN uv pip install --system -r requirements.txt

    # Run the script as the entrypoint
    ENTRYPOINT ["uv", "run", "/app/arxiv_tracker.py"]

Notice that we have modified the `ENTRYPOINT` to run the `arxiv_tracker.py` script using `uv` instead of `python` directly.

## Conclusion

This is it! We have successfully upgraded the arXiv publications tracker to use uv instead of pip. If you are interested, you can get the updated version of the arXiv publications tracker [here](https://github.com/florianbuetow/arxiv_publications_tracker) and give it a try. To learn more about what you can do with uv, check out the [official uv documentation](https://docs.astral.sh/uv/).

**Takeaways**

- uv is ultra fast
- uv is a drop in replacement for pip and pip-tools
- uv can replace conda and virtualenv
- read the [official uv documentation](https://docs.astral.sh/uv/) to learn more

## Links and Resources

- [uv: Python packaging in Rust](https://astral.sh/blog/uv) by the creator of uv [Charlie Marsh](https://x.com/charliermarsh)
- [uv on Astral.sh](https://docs.astral.sh/uv/) - The official documentation for uv
- [uv on PyPi](https://pypi.org/project/uv/) - The mirrored documentation for uv on PyPi
- [Arxiv Publications Tracker](https://github.com/florianbuetow/arxiv_publications_tracker) - A Python based tool to incrementally find the latest publications on arXiv

**Other Package Managers**

- [conda](https://anaconda.org/anaconda/conda) - OS-agnostic, system-level binary package and environment manager
- [pip](https://pypi.org/project/pip/) - pip is the package installer for Python
- [pip-tools](https://pypi.org/project/pip-tools/) - A set of command line tools to help you keep your pip-based packages fresh
- [virtualenv](https://virtualenv.pypa.io/) - a tool to create isolated Python environments
- [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/) - a tool to manage virtual environments
