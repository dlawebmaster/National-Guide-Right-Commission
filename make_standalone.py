#!/usr/bin/env python3
"""
Build self-contained copies of every page into standalone/.

Each output file carries its own stylesheet, its own scripts, the chapter
dataset where the locator needs it, and the emblem and favicons as data URIs.
Drop one in on its own and it renders correctly even when the shared
assets/css/site.css on the server is out of date.

Photographs stay as relative paths. They are content you upload anyway, and
embedding them would add roughly 600 KB per page.

Run: python3 make_standalone.py
"""

import base64
import glob
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'standalone')

BANNER = """<!--
  Self-contained build. Styles, scripts and the header emblem are inlined, so
  this page renders on its own with no dependency on assets/css/site.css or
  assets/js/*. Photographs still load from assets/img/.

  Use these files when you are updating the site one page at a time. Once the
  shared stylesheet is deployed, switch back to the linked pages in the parent
  folder so a palette change reaches every page at once.
-->
"""


def read(path):
    return io.open(os.path.join(HERE, path), encoding='utf-8').read()


def datauri(path, mime='image/png'):
    with open(os.path.join(HERE, path), 'rb') as f:
        return 'data:%s;base64,%s' % (mime, base64.b64encode(f.read()).decode())


def main():
    os.makedirs(OUT, exist_ok=True)

    css = read('assets/css/site.css')
    scripts = {
        'assets/js/site.js': read('assets/js/site.js'),
        'assets/js/locator.js': read('assets/js/locator.js'),
        'assets/js/history.js': read('assets/js/history.js'),
    }
    chapters = read('assets/data/chapters.json')

    emblem = datauri('assets/img/guide-right-emblem-320.png')
    fav32 = datauri('assets/img/favicon-32.png')
    fav180 = datauri('assets/img/favicon-180.png')

    built = []
    for path in sorted(glob.glob(os.path.join(HERE, '*.html'))):
        name = os.path.basename(path)
        if name.startswith('history-standalone'):
            continue
        html = io.open(path, encoding='utf-8').read()

        html = html.replace('<link rel="stylesheet" href="assets/css/site.css">',
                            '<style>\n' + css + '\n</style>')

        # the locator reads its dataset from a global when one is present
        if 'assets/js/locator.js' in html:
            html = html.replace(
                '<script src="assets/js/locator.js"></script>',
                '<script>window.__NGRC_CHAPTERS__ = ' + chapters.strip() + ';</script>\n'
                '<script>\n' + scripts['assets/js/locator.js'] + '\n</script>')

        for src, code in scripts.items():
            html = html.replace('<script src="%s"></script>' % src,
                                '<script>\n' + code + '\n</script>')

        html = html.replace('src="assets/img/guide-right-emblem-320.png"', 'src="' + emblem + '"')
        html = html.replace('href="assets/img/favicon-32.png"', 'href="' + fav32 + '"')
        html = html.replace('href="assets/img/favicon-180.png"', 'href="' + fav180 + '"')

        html = html.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n' + BANNER, 1)

        io.open(os.path.join(OUT, name), 'w', encoding='utf-8').write(html)
        leftover = re.findall(r'(?:href|src)="(assets/(?:css|js|data)/[^"]+)"', html)
        built.append((name, len(html.encode()) / 1024, leftover))

    print('Built %d self-contained pages in standalone/' % len(built))
    for name, kb, leftover in built:
        flag = '  UNRESOLVED: %s' % leftover if leftover else ''
        print('  %-22s %6.0f KB%s' % (name, kb, flag))


if __name__ == '__main__':
    main()
