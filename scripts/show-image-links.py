#!/usr/bin/env python3
"""Display all image references found in content/ markdown files as an ASCII table."""

import os
import re
from collections import defaultdict

_IMAGE_EXT = re.compile(r'\.(png|jpg|jpeg|gif|svg|webp|avif|bmp|ico|tiff)$', re.IGNORECASE)
_IMG_REF   = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')

_GREY  = '\033[90m'
_WHITE = '\033[97m'
_RESET = '\033[0m'


def _project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _normalize(ref):
    ref = ref.split('?', 1)[0]
    ref = ref.split('#', 1)[0]
    ref = ref.split(' "', 1)[0].strip()
    return ref


def _is_draft(md_abs):
    try:
        with open(md_abs, encoding='utf-8', errors='replace') as f:
            in_front = False
            for i, line in enumerate(f):
                line = line.rstrip()
                if i == 0 and line == '---':
                    in_front = True
                    continue
                if in_front:
                    if line == '---':
                        break
                    if re.match(r'^draft:\s*true', line):
                        return True
    except OSError:
        pass
    return False


def _collect(root):
    refs = defaultdict(list)
    content_dir = os.path.join(root, 'content')
    for dirpath, _, filenames in os.walk(content_dir):
        for fn in sorted(filenames):
            if not fn.endswith('.md'):
                continue
            md_abs = os.path.join(dirpath, fn)
            rel_md = os.path.relpath(md_abs, root)
            draft  = _is_draft(md_abs)
            with open(md_abs, encoding='utf-8', errors='replace') as f:
                text = f.read()
            for m in _IMG_REF.finditer(text):
                ref = _normalize(m.group(1))
                if ref.startswith(('http://', 'https://')):
                    continue
                if not _IMAGE_EXT.search(ref):
                    continue
                if ref.startswith('/'):
                    img_path = 'static' + ref
                else:
                    img_path = os.path.relpath(os.path.join(dirpath, ref), root)
                entry = (rel_md, draft)
                if entry not in refs[img_path]:
                    refs[img_path].append(entry)
    return refs


def _color_path(path, width):
    """
    Pad path to width; grey up to the parent folder, white from parent folder onwards.
    """
    padding = ' ' * (width - len(path))
    second_last = path.rfind('/', 0, path.rfind('/'))
    if second_last >= 0:
        return _GREY + path[:second_last + 1] + _WHITE + path[second_last + 1:] + _RESET + padding
    last = path.rfind('/')
    if last >= 0:
        return _GREY + path[:last + 1] + _WHITE + path[last + 1:] + _RESET + padding
    return _WHITE + path + _RESET + padding


def _color_md(rel_md, draft, width):
    """
    Pad to width; directory part grey, filename white, [draft] tag in grey.
    """
    tag     = ' [draft]' if draft else ''
    visible = len(rel_md) + len(tag)
    padding = ' ' * (width - visible)
    second_last = rel_md.rfind('/', 0, rel_md.rfind('/'))
    if second_last >= 0:
        colored = _GREY + rel_md[:second_last + 1] + _WHITE + rel_md[second_last + 1:] + _RESET
    else:
        last = rel_md.rfind('/')
        if last >= 0:
            colored = _GREY + rel_md[:last + 1] + _WHITE + rel_md[last + 1:] + _RESET
        else:
            colored = _WHITE + rel_md + _RESET
    if draft:
        colored += _GREY + ' [draft]' + _RESET
    return colored + padding


def _render(refs):
    rows = sorted(refs.items())
    if not rows:
        print('  (no image references found in content/)')
        return

    H1 = 'Image Path'
    H2 = 'Referenced by (Markdown files)'

    def _plain_label(rel_md, draft):
        return rel_md + (' [draft]' if draft else '')

    col1_w = max(len(H1), max(len(img) for img, _ in rows))
    col2_w = max(
        len(H2),
        max(max(len(_plain_label(f, d)) for f, d in files) for _, files in rows),
    )

    def hline(l, m, r):
        return l + '─' * (col1_w + 2) + m + '─' * (col2_w + 2) + r

    def vline(c1, c2):
        return '│ ' + c1 + ' │ ' + c2 + ' │'

    header_c1 = _GREY + H1.ljust(col1_w) + _RESET
    header_c2 = _GREY + H2.ljust(col2_w) + _RESET

    print(hline('┌', '┬', '┐'))
    print(vline(header_c1, header_c2))
    print(hline('├', '┼', '┤'))

    for i, (img, entries) in enumerate(rows):
        drafts     = sorted((f, d) for f, d in entries if d)
        non_drafts = sorted((f, d) for f, d in entries if not d)
        ordered    = drafts + non_drafts

        for j, (rel_md, draft) in enumerate(ordered):
            c1 = _color_path(img, col1_w) if j == 0 else ' ' * col1_w
            c2 = _color_md(rel_md, draft, col2_w)
            print(vline(c1, c2))

        if i < len(rows) - 1:
            print(hline('├', '┼', '┤'))

    print(hline('└', '┴', '┘'))


def main():
    root = _project_root()
    refs = _collect(root)
    _render(refs)


if __name__ == '__main__':
    main()
