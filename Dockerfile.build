# Use a minimal base image with Quarto, Pandoc, and Python support
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install required dependencies including Python 3 and pip
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    pandoc \
    git \
    python3 \
    python3-pip \
    r-base \
    && apt-get clean

# Install Quarto
RUN wget https://quarto.org/download/latest/quarto-linux-amd64.deb && \
    dpkg -i quarto-linux-amd64.deb && \
    rm quarto-linux-amd64.deb

# Install R packages 'knitr' and 'rmarkdown'
RUN R -e "install.packages(c('knitr', 'rmarkdown'), repos='https://cloud.r-project.org/')"

# Copy requirements.txt to the container
COPY requirements.txt /site/requirements.txt

# Install Python dependencies from requirements.txt
RUN pip3 install --no-cache-dir -r /site/requirements.txt

# Set the working directory to /site
WORKDIR /site

# Clear the docs folder contents before rendering the Quarto website
CMD rm -rf /site/docs/* && quarto render . --output-dir docs
