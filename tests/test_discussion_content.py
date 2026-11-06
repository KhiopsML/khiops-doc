import unittest

from scripts.discussion_content import InvalidDiscussion, extract, summary_section


def discussion(**overrides):
    return {
        "id": "id",
        "number": 123,
        "url": "https://github.com/orgs/example/discussions/123",
        "title": "Original title",
        "body": "Original content",
        "labels": [{"name": "Topic/A", "description": "Topic A"}],
        "comments": [],
        **overrides,
    }


class DiscussionContentTests(unittest.TestCase):
    def test_ready_to_use_with_no_reply_or_no_marker(self):
        for comments in ([], [{"body": "A reply without a summary"}]):
            item = extract(discussion(comments=comments))
            self.assertEqual((item.title, item.content), ("Original title", "Original content"))

    def test_first_reply_summary_and_remaining_content(self):
        item = extract(discussion(comments=[
            {"body": "Before\n\n### Question summary\nA question?\n\n### Answer\nAnswer text\n"},
            {"body": "### Question summary\nWrong reply"},
        ]))
        self.assertEqual(item.title, "A question?")
        self.assertEqual(item.content, "Before\n\n### Answer\nAnswer text")

    def test_summary_inside_code_fence_is_not_heading(self):
        self.assertIsNone(summary_section("```\n### Question summary\nnot a heading\n```\n"))

    def test_empty_or_multiple_summary_sections_are_invalid(self):
        for body in ("### Question summary\n\n### Answer\nx", "### Question summary\na\n### Question summary\nb"):
            with self.subTest(body=body), self.assertRaises(InvalidDiscussion):
                extract(discussion(comments=[{"body": body}]))

    def test_topic_validation(self):
        self.assertIsNone(extract(discussion(labels=[{"name": "Other", "description": ""}])))
        with self.assertRaisesRegex(InvalidDiscussion, "no description"):
            extract(discussion(labels=[{"name": "Topic/A", "description": ""}]))
        with self.assertRaisesRegex(InvalidDiscussion, "Topic/A, Topic/B"):
            extract(discussion(labels=[
                {"name": "Topic/B", "description": "B"},
                {"name": "Topic/A", "description": "A"},
            ]))


if __name__ == "__main__":
    unittest.main()
