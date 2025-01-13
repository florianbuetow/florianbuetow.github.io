find . -type f -name ".DS_Store" -delete -print
pip install -r requirements-doc.txt
./build_notebooks.sh
mkdocs build