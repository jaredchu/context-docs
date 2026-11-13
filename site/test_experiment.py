"""Keep the published article faithful to the reviewed Markdown and frozen scores."""
from html.parser import HTMLParser
import importlib.util
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('experiment_build', ROOT / 'site/build.py')
build = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build)


class Article(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.active = False
        self.text = []
        self.links = []
        self.tables = []
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'article' and attrs.get('id') == 'experiment-report':
            self.active = True
        if not self.active:
            return
        if tag == 'a':
            self.links.append(attrs['href'])
        if tag == 'table':
            self.tables.append([])
        if tag == 'tr':
            self.row = []
        if tag in ('td', 'th'):
            self.cell = []

    def handle_data(self, data):
        if self.active:
            self.text.append(data)
            if self.cell is not None:
                self.cell.append(data)

    def handle_endtag(self, tag):
        if not self.active:
            return
        if tag in ('td', 'th'):
            self.row.append(''.join(self.cell).strip())
            self.cell = None
        if tag == 'tr':
            self.tables[-1].append(self.row)
            self.row = None
        if tag == 'article':
            self.active = False


def article():
    parser = Article()
    parser.feed(build.render_page(ROOT, 'experiment.html', 'Experiment'))
    return parser


def tokens(text):
    return re.findall(r'\w+|[^\w\s]', text)


class ExperimentPublicationTests(unittest.TestCase):
    def test_complete_article_matches_canonical_markdown(self):
        markdown = (ROOT / 'docs/evaluation-2026-11-13-markdown-maintenance.md').read_text()
        markdown = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', markdown)
        content = []
        for line in markdown.splitlines():
            if re.fullmatch(r'\|(?:\s*:?-+:?\s*\|)+', line):
                continue
            line = re.sub(r'^(?:#{1,6} |- )', '', line)
            if line.startswith('|'):
                line = line.replace('|', ' ')
            content.append(line.replace('**', '').replace('`', ''))
        self.assertEqual(tokens(' '.join(article().text)), tokens(' '.join(content)))

    def test_all_six_score_rows_include_the_excluded_cell(self):
        self.assertEqual(article().tables[1][1:], [
            ['A', 'Ordinary Markdown', '3', '4', '8', '7', '2', 'Yes'],
            ['A', 'Context Docs', '2', '4', '8', '6', '2', 'Yes'],
            ['B', 'Ordinary Markdown', '2', '4', '8', '5', '2', 'Yes'],
            ['B', 'Context Docs', '2', '3', '7', '5', '2', 'No: required read output missing'],
            ['C', 'Ordinary Markdown', '2', '4', '8', '6', '2', 'Yes'],
            ['C', 'Context Docs', '1', '4', '8', '5', '2', 'Yes'],
        ])

    def test_public_evidence_links_use_repository_sources(self):
        links = article().links
        self.assertIn('https://github.com/jaredchu/context-docs/blob/main/evals/results/2026-11-13-markdown-maintenance/README.md', links)
        self.assertTrue(all(url.startswith('https://github.com/jaredchu/context-docs/blob/main/') for url in links))
        self.assertIn('experiments/markdown-maintenance/', build.CANONICAL_ROUTES)
        self.assertIn('href="experiments/markdown-maintenance/"', (ROOT / 'site/index.html').read_text())
        self.assertNotRegex((ROOT / 'site/experiment.html').read_text(), r'/Users/|/Volumes/|<script|Local publication draft')


if __name__ == '__main__':
    unittest.main()
