import json
import tempfile
import unittest
from pathlib import Path

from python.discussions.generate_discussions import BEGIN, END, MANIFEST, OVERSIZED, navigation, synchronize
from python.discussions.discussion_render import topic_slug


def discussion(number, topic="Topic/Test", body="Text", title=None):
    return {
        "id": str(number), "number": number, "title": title or f"Question {number}",
        "body": body, "url": f"https://github.com/orgs/example/discussions/{number}",
        "comments": [], "labels": [{"name": topic, "description": topic.removeprefix("Topic/")}],
    }


class GenerateDiscussionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "zensical.toml").write_text(f"nav = [\n{BEGIN}\n{END}\n]\n")

    def snapshot(self):
        return {
            str(path.relative_to(self.root)): path.read_bytes()
            for path in self.root.rglob("*") if path.is_file()
        }

    def test_idempotence_and_changes_including_move(self):
        first = [discussion(1), discussion(2)]
        report = synchronize(self.root, first)
        self.assertIn("## Added", report)
        self.assertIn("#1", report)
        snapshot = self.snapshot()
        synchronize(self.root, first)
        self.assertEqual(self.snapshot(), snapshot)

        report = synchronize(self.root, [discussion(1, body="Changed"), discussion(2)])
        self.assertIn("## Changed\n\n### Topic/Test\n\n- [#1", report)

        report = synchronize(self.root, [discussion(1, topic="Topic/New"), discussion(3)])
        self.assertIn("### Topic/New", report)
        self.assertIn("#1", report)
        self.assertIn("#2", report)
        self.assertIn("#3", report)
        manifest = json.loads((self.root / MANIFEST).read_text())
        self.assertEqual(set(manifest["discussions"]), {"1", "3"})
        self.assertIn("q-and-a/", (self.root / "zensical.toml").read_text())

    def test_slug_collision_avoidance(self):
        self.assertNotEqual(topic_slug("Topic/A B"), topic_slug("Topic/A-B"))

    def test_missing_and_reversed_navigation_markers_fail(self):
        for text in ("nav = []", f"{END}\n{BEGIN}"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                navigation(text, {})

    def test_oversized_report_is_deterministic(self):
        examples = (
            ("https://github.com/user-attachments/files/123/example.py", "script", ""),
            ("https://github.com/user-attachments/assets/123", "image", "!"),
        )
        for url, name, prefix in examples:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as name:
                root = Path(name)
                (root / "zensical.toml").write_text(f"nav = [\n{BEGIN}\n{END}\n]\n")
                items = [discussion(1, body=f"{prefix}[attachment]({url})")]
                downloader = lambda _: (b"x" * 100_001, "image/png")
                report = synchronize(root, items, downloader)
                self.assertIn(url, report)
                self.assertEqual(len(json.loads((root / OVERSIZED).read_text())), 1)
                snapshot = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
                report = synchronize(root, items, downloader)
                self.assertIn(url, report)
                self.assertEqual(
                    snapshot, {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
                )

    def test_refuses_to_overwrite_unowned_page(self):
        page = self.root / "docs/q-and-a/overview.md"
        page.parent.mkdir(parents=True)
        page.write_text("manual content")
        with self.assertRaisesRegex(ValueError, "unowned"):
            synchronize(self.root, [discussion(1)])
        self.assertEqual(page.read_text(), "manual content")


if __name__ == "__main__":
    unittest.main()
