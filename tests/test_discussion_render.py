import unittest
from unittest.mock import patch

from scripts.discussion_content import PublishedDiscussion
from scripts.discussion_render import (
    MAX_ATTACHMENT_BYTES,
    AttachmentError,
    download_attachment,
    render_content,
    render_pages,
)


IMAGE = "https://github.com/user-attachments/assets/123"
SCRIPT = "https://github.com/user-attachments/files/123/example.py"


def item(content, number=1):
    return PublishedDiscussion(
        id=str(number), number=number, url=f"https://github.com/orgs/example/discussions/{number}",
        topic="Topic/Test", topic_title="Test topic", title="Example question", content=content,
    )


class Response:
    def __init__(self, data, content_type):
        self.data = data
        self.headers = self
        self.content_type = content_type

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def read(self, size):
        return self.data[:size]

    def get_content_type(self):
        return self.content_type


class RenderingTests(unittest.TestCase):
    def test_limit_with_no_declared_length(self):
        with patch("scripts.discussion_render.urllib.request.build_opener") as build:
            for url, content_type in ((IMAGE, "image/png"), (SCRIPT, "text/plain")):
                build.return_value.open.return_value = Response(b"x" * MAX_ATTACHMENT_BYTES, content_type)
                self.assertEqual(len(download_attachment(url)[0]), MAX_ATTACHMENT_BYTES)
                build.return_value.open.return_value = Response(b"x" * (MAX_ATTACHMENT_BYTES + 1), content_type)
                with self.assertRaises(AttachmentError):
                    download_attachment(url)

    def test_image_and_script_are_copied_and_linked(self):
        def download(url):
            return (b"x" * MAX_ATTACHMENT_BYTES, "image/png" if url == IMAGE else "text/plain")

        pages, assets, invalid = render_pages(
            [item(f'<img src="{IMAGE}" alt="example"> [script]({SCRIPT})')], download
        )
        self.assertEqual(invalid, [])
        self.assertEqual(len(assets), 2)
        page = next(value for key, value in pages.items() if key != "q-and-a/overview.md")
        for path in assets:
            self.assertIn("/" + path, page)
        self.assertIn("discussion #1", page)

    def test_oversized_discussion_is_omitted_and_reported(self):
        for url, markup in ((IMAGE, f"![image]({IMAGE})"), (SCRIPT, f"[script]({SCRIPT})")):
            with self.subTest(url=url):
                pages, assets, invalid = render_pages(
                    [item(markup), item("normal", number=2)],
                    lambda _: (b"x" * (MAX_ATTACHMENT_BYTES + 1), "image/png"),
                )
                self.assertEqual(invalid[0]["file"], url)
                self.assertNotIn("discussion #1", "".join(pages.values()))
                self.assertIn("discussion #2", "".join(pages.values()))
                self.assertEqual(assets, {})

    def test_sanitization_and_regular_links(self):
        content, _ = render_content(item(
            '[link](https://example.com) <script>alert(1)</script> '
            '<img src="javascript:alert(1)" onerror="alert(1)"> {{ dangerous }}'
        ))
        self.assertIn('href="https://example.com"', content)
        self.assertNotIn("<script", content)
        self.assertNotIn("onerror", content)
        self.assertNotIn("javascript:", content)
        self.assertNotIn("{{", content)

    def test_output_is_deterministic(self):
        items = [item("Two", 2), item("One", 1)]
        self.assertEqual(render_pages(items), render_pages(list(reversed(items))))


if __name__ == "__main__":
    unittest.main()
