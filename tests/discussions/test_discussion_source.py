import json
import subprocess
import unittest
from unittest.mock import patch

from python.discussions import discussion_source as source


def connection(nodes, cursor=None):
    return {
        "nodes": nodes,
        "pageInfo": {"hasNextPage": cursor is not None, "endCursor": cursor},
    }


class DiscussionSourceTests(unittest.TestCase):
    def test_paginated_discussions_and_labels_with_only_first_reply(self):
        discussion = {"id": "id", "url": "https://example.test/1"}
        calls = []

        def request(query, variables):
            calls.append((query, variables.copy()))
            if query == source.DISCUSSIONS_QUERY:
                return {"repository": {"discussions": connection(
                    [discussion] if variables["cursor"] is None else [],
                    "next" if variables["cursor"] is None else None,
                )}}
            if variables["labelsCursor"] is None:
                return {"node": {
                    "labels": connection([{"name": "Topic/A"}], "label-next"),
                    "comments": {"nodes": [{"body": "first"}]},
                }}
            return {"node": {
                "labels": connection([{"name": "other"}]),
                "comments": {"nodes": [{"body": "first"}]},
            }}

        result = source.fetch_discussions(request)
        self.assertEqual([x["name"] for x in result[0]["labels"]], ["Topic/A", "other"])
        self.assertEqual([x["body"] for x in result[0]["comments"]], ["first"])
        self.assertIn("comments(first: 1)", source.DETAILS_QUERY)
        self.assertNotIn("commentsCursor", source.DETAILS_QUERY)
        self.assertEqual(len(calls), 4)

    def test_no_replies_and_repeated_label_cursor(self):
        discussion = {"id": "id", "url": "https://example.test/1"}
        node = {"labels": connection([]), "comments": {"nodes": []}}
        self.assertEqual(source.fetch_details(discussion, lambda *_: {"node": node})["comments"], [])
        node["labels"] = connection([], "same")
        with self.assertRaisesRegex(source.GitHubError, "repeated labels cursor"):
            source.fetch_details(discussion, lambda *_: {"node": node})

    def test_empty_repository(self):
        result = source.fetch_discussions(
            lambda query, variables: {"repository": {"discussions": connection([])}}
        )
        self.assertEqual(result, [])

    def test_missing_repository_and_bad_cursor_fail(self):
        with self.assertRaisesRegex(source.GitHubError, "Cannot access"):
            source.fetch_discussions(lambda query, variables: {"repository": None})
        with self.assertRaisesRegex(source.GitHubError, "without a cursor"):
            source.next_cursor({"pageInfo": {"hasNextPage": True, "endCursor": None}})

    @patch("python.discussions.discussion_source.subprocess.run")
    def test_graphql_surfaces_authentication_and_api_errors(self, run):
        run.return_value = subprocess.CompletedProcess([], 1, "", "authentication required")
        with self.assertRaisesRegex(source.GitHubError, "authentication required"):
            source.graphql("query", {})
        run.return_value = subprocess.CompletedProcess(
            [], 0, json.dumps({"errors": [{"message": "access denied"}]}), ""
        )
        with self.assertRaisesRegex(source.GitHubError, "access denied"):
            source.graphql("query", {})


if __name__ == "__main__":
    unittest.main()
