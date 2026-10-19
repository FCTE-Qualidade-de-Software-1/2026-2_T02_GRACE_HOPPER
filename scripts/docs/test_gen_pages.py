#!/usr/bin/env python3
"""Testes unitários para a função rewrite_links de gen_pages.py."""

import sys
import unittest
from pathlib import Path

# Garantir que o repositório esteja no sys.path para importação
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.docs.gen_pages import rewrite_links


class TestRewriteLinks(unittest.TestCase):
    def test_rewrite_docs_link(self):
        self.assertEqual(rewrite_links("[a](docs/x.md)"), "[a](x.md)")

    def test_rewrite_contributing_link(self):
        self.assertEqual(rewrite_links("[c](CONTRIBUTING.md)"), "[c](contributing.md)")

    def test_rewrite_readme_link(self):
        self.assertEqual(rewrite_links("[r](README.md)"), "[r](index.md)")

    def test_external_urls_remain_unchanged(self):
        url = "https://example.com/docs/x.md"
        self.assertEqual(rewrite_links(f"[link]({url})"), f"[link]({url})")
        http_url = "http://example.com/CONTRIBUTING.md"
        self.assertEqual(rewrite_links(f"[link]({http_url})"), f"[link]({http_url})")

    def test_text_outside_links_unchanged(self):
        text = "Veja docs/x.md e CONTRIBUTING.md aqui: [a](docs/x.md)"
        expected = "Veja docs/x.md e CONTRIBUTING.md aqui: [a](x.md)"
        self.assertEqual(rewrite_links(text), expected)

    def test_link_with_anchor(self):
        self.assertEqual(rewrite_links("[a](docs/x.md#secao)"), "[a](x.md#secao)")
        self.assertEqual(rewrite_links("[c](CONTRIBUTING.md#regras)"), "[c](contributing.md#regras)")
        self.assertEqual(rewrite_links("[r](README.md#topo)"), "[r](index.md#topo)")

    def test_badge_image_inside_link(self):
        badge = "[![Badge](https://img.shields.io/badge.svg)](docs/gestao_projeto_releases_milestones_issues.md)"
        expected = "[![Badge](https://img.shields.io/badge.svg)](gestao_projeto_releases_milestones_issues.md)"
        self.assertEqual(rewrite_links(badge), expected)

    def test_code_formatted_link_text(self):
        code_link = "[`docs/relatorio.md`](docs/relatorio.md)"
        expected = "[`docs/relatorio.md`](relatorio.md)"
        self.assertEqual(rewrite_links(code_link), expected)


if __name__ == "__main__":
    unittest.main()
