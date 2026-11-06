"""Retrieve organization discussions from their GitHub repository."""

import json
import subprocess


DISCUSSIONS_QUERY = """
query($owner: String!, $repository: String!, $cursor: String) {
  repository(owner: $owner, name: $repository) {
    discussions(first: 50, after: $cursor) {
      nodes { id number title url body }
      pageInfo { hasNextPage endCursor }
    }
  }
}
"""

DETAILS_QUERY = """
query($id: ID!, $labelsCursor: String, $commentsCursor: String) {
  node(id: $id) {
    ... on Discussion {
      labels(first: 100, after: $labelsCursor) {
        nodes { name description }
        pageInfo { hasNextPage endCursor }
      }
      comments(first: 100, after: $commentsCursor) {
        nodes { body }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}
"""


class GitHubError(RuntimeError):
    """The source cannot be read reliably from GitHub."""


def graphql(query, variables):
    command = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if value is not None:
            command.extend(["-f", f"{key}={value}"])
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode:
        raise GitHubError(f"GitHub GraphQL request failed: {result.stderr.strip()}")
    try:
        response = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise GitHubError("GitHub GraphQL returned invalid JSON") from exc
    if response.get("errors"):
        raise GitHubError(f"GitHub GraphQL errors: {response['errors']}")
    if not isinstance(response.get("data"), dict):
        raise GitHubError("GitHub GraphQL returned no data")
    return response["data"]


def next_cursor(connection):
    page = connection["pageInfo"]
    if not page["hasNextPage"]:
        return None
    cursor = page["endCursor"]
    if not cursor:
        raise GitHubError("GitHub reported another page without a cursor")
    return cursor


def fetch_discussions(request=graphql, owner="KhiopsML", repository="khiops"):
    """Return all discussions and their labels and chronological replies."""
    cursor = None
    discussions = []
    while True:
        data = request(
            DISCUSSIONS_QUERY,
            {"owner": owner, "repository": repository, "cursor": cursor},
        )
        repo = data.get("repository")
        if repo is None:
            raise GitHubError(f"Cannot access discussion repository {owner}/{repository}")
        connection = repo["discussions"]
        for discussion in connection["nodes"]:
            discussions.append(fetch_details(discussion, request))
        following = next_cursor(connection)
        if following is None:
            return discussions
        if following == cursor:
            raise GitHubError("GitHub returned a repeated discussions cursor")
        cursor = following


def fetch_details(discussion, request):
    labels = []
    comments = []
    cursors = {"labels": None, "comments": None}
    complete = {"labels": False, "comments": False}
    while not all(complete.values()):
        data = request(
            DETAILS_QUERY,
            {
                "id": discussion["id"],
                "labelsCursor": cursors["labels"],
                "commentsCursor": cursors["comments"],
            },
        )
        node = data.get("node")
        if node is None:
            raise GitHubError(f"Cannot access discussion {discussion['url']}")
        for key, output in (("labels", labels), ("comments", comments)):
            if complete[key]:
                continue
            connection = node[key]
            output.extend(connection["nodes"])
            following = next_cursor(connection)
            if following is None:
                complete[key] = True
            elif following == cursors[key]:
                raise GitHubError(f"GitHub returned a repeated {key} cursor")
            else:
                cursors[key] = following
    return {**discussion, "labels": labels, "comments": comments}
