"""Check complete article, score/audit parity and public artifact boundaries."""
from html.parser import HTMLParser
from pathlib import Path
import importlib.util
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('public_experiment_build', ROOT/'site/build.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)
spec = importlib.util.spec_from_file_location('previous_article_test', ROOT/'site/test_experiment.py')
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)

def article():
    parser = previous.Article()
    parser.feed(build.render_page(ROOT, 'public-project-experiment.html', 'Public-project experiment'))
    return parser

def interval(value):
    return str(value['low']) if value['low'] == value['high'] else str(value['low']) + chr(8211) + str(value['high'])

class PublicProjectExperimentTests(unittest.TestCase):
    def test_complete_article_matches_canonical_report(self):
        markdown = (ROOT/'docs/evaluation-2026-11-14-public-project-docs.md').read_text()
        markdown = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', markdown)
        content = []
        for line in markdown.splitlines():
            if re.fullmatch(r'\|(?:\s*:?-+:?\s*\|)+', line):
                continue
            line = re.sub(r'^(?:#{1,6} |- )', '', line)
            if line.startswith('|'):
                line = line.replace('|', ' ')
            content.append(line.replace('**', '').replace('`', ''))
        self.assertEqual(previous.tokens(' '.join(article().text)), previous.tokens(' '.join(content)))

    def test_every_score_and_audit_row_matches_public_evidence(self):
        score_rows, audit_rows = [], []
        for cid in ('P01', 'P02', 'P03'):
            data = json.loads((ROOT/'evals/results/2026-11-14-public-project-docs'/f'{cid}.json').read_text())
            for condition, label in (('original-docs', 'Original docs'), ('ordinary', 'Ordinary Markdown'), ('context-docs', 'Context Docs')):
                value = data['reconciliation']['reconcile']['conditions'][condition]
                score_rows.append([cid, label] + [interval(value['intervals'][key]) for key in
                                  ('supported_correct', 'supported_partial', 'useful_cited_correct', 'unknown_correct')])
                flags = value['doc_claim_audit_pass2_only']
                audit_rows.append([cid, label] + [str(flags[key]['count']) + '/' + str(flags[key]['critical']) for key in
                                  ('contradicted', 'unsupported', 'fabricated_authority', 'lost_constraint')])
        tables = article().tables
        self.assertEqual(tables[2][1:], score_rows)
        self.assertEqual(tables[3][1:], audit_rows)

    def test_evidence_stays_in_repository_and_route_is_discoverable(self):
        links = article().links
        self.assertIn('https://github.com/jaredchu/context-docs/blob/main/evals/results/2026-11-14-public-project-docs/README.md', links)
        self.assertIn('experiments/public-project-docs/', build.CANONICAL_ROUTES)
        self.assertIn('href="experiments/public-project-docs/"', (ROOT/'site/index.html').read_text())
        self.assertTrue(all(url.startswith('https://github.com/') for url in links))
        self.assertNotRegex((ROOT/'site/public-project-experiment.html').read_text(), r'/Users/|/Volumes/|<script|not published|Local draft')

if __name__ == '__main__':
    unittest.main()
