#!/bin/bash
# Convert all notebooks to Markdown
for notebook in docs/examples/*.ipynb; do
    jupyter nbconvert --to markdown "$notebook"
done