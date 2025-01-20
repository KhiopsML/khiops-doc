from pygments.lexer import RegexLexer, words, bygroups, include
from pygments.token import (
    Comment,
    Name,
    String,
    Number,
    Operator,
    Keyword,
    Punctuation,
    Whitespace,
)

__all__ = ["KdicLexer", "KdicApiDocsLexer"]


def float_regex():
    return r"([+-]?)(\d+\.\d*|\.\d+|\d+)([eE][+-]?\d+)?"

def identifier_regex():
    return r"[a-zA-Z][a-zA-Z0-9_]*|`.+?`"

def dictionary_declaration_regex():
    return fr"\b(Root)?(\s+)?(Dictionary)(\s+)({identifier_regex()})"

class KdicLexer(RegexLexer):
    """Khiops Dictionary Language Lexer"""
    name = "Khiops Dictionary Language"
    aliases = ["kdic"]
    filenames = ["*.kdic"]
    tokens = {
        "root": [
            # Whitespace and comments
            (r"\s+", Whitespace),
            include("comments"),
            # Dictionary declaratio with and without key list
            (
                fr"{dictionary_declaration_regex()}(\s*)(\()",
                bygroups(
                    Keyword.Reserved,
                    Whitespace,
                    Keyword.Declaration,
                    Whitespace,
                    Name.Class,
                    Whitespace,
                    Punctuation,
                ),
                "key_list",
            ),
            (
                dictionary_declaration_regex(),
                bygroups(
                    Keyword.Reserved,
                    Whitespace,
                    Keyword.Declaration,
                    Whitespace,
                    Name.Class,
                ),
            ),
            # Type declarations
            (
                r"\b(Unused)?(\s*)(Numerical|Categorical|Date|Time|Timestamp|TimestampTZ|Text|TextList)\b",
                bygroups(Keyword.Declaration, Whitespace, Keyword.Type),
            ),
            (
                fr"(Unused)?(\s*)(Table|Entity)(\s*)(\()({identifier_regex()})(\))",
                bygroups(
                    Keyword.Declaration,
                    Whitespace,
                    Keyword.Type,
                    Whitespace,
                    Punctuation,
                    Name.Class,
                    Punctuation,
                ),
            ),
            (
                r"(Unused)?(\s*)(Structure)(\s*)(\()([a-zA-Z0-9_]+)(\))",
                bygroups(
                    Keyword.Declaration,
                    Whitespace,
                    Keyword.Type,
                    Whitespace,
                    Punctuation,
                    Name.Function,
                    Punctuation,
                ),
            ),
            # Variable names and optional start of rule declaration
            (
                fr"({identifier_regex()})(\s*)(=)",
                bygroups(Name.Attribute, Whitespace, Operator),
                "rule_declaration",
            ),
            (
                identifier_regex(),
                Name.Attribute,
            ),
            # Meta data
            (r"<", Punctuation, "meta_data"),
            # Punctuation
            (r"[\{\};]", Punctuation),
        ],
        "comments": [
            (r"^#.*?$", Comment.Single),
            (r"//.*?$", Comment.Single),
        ],
        "key_list": [
            (r"\s+", Whitespace),
            (r"[a-zA-Z][a-zA-Z0-9_]*", Name.Attribute),
            (r"`.+?`", Name.Attribute),
            (r",", Punctuation),
            (r"\)", Punctuation, "#pop"),
        ],
        "meta_data": [
            (r"\w", Name.Property),
            (r"\s+", Whitespace),
            (
                fr"(=){float_regex()}",
                bygroups(Operator, Number.Float, Number.Float, Number.Float),
            ),
            (r"(=)(\d+)", bygroups(Operator, Number.Integer)),
            (r'(=)(".*?")', bygroups(Operator, String)),
            (r">", Punctuation, "#pop"),
        ],
        "rule_declaration": [
            (r"\s+", Whitespace),
            (
                r"([a-zA-Z][a-zA-Z0-9_]*)(\s*)(\()",
                bygroups(Name.Function, Whitespace, Punctuation),
                "#push",
            ),
            (identifier_regex(), Name.Attribute),
            (r"\s+", Whitespace),
            (float_regex(), Number.Float),
            (r"\d+", Number.Integer),
            (r'".*?"', String),
            (r",", Punctuation),
            (r"\)", Punctuation, "#pop"),
            (r";", Punctuation, "#pop"),
        ],
    }


class KdicApiDocsLexer(RegexLexer):
    """Simple Lexer for the Khiops Dictionary Language Rule Documentation"""

    def non_structure_types_regex():
        return "|".join(
            [
                "Numerical",
                "Categorical",
                "Date",
                "Time",
                "Timestamp",
                "TimestampTZ",
                "Text",
                "TextList",
                "Table",
                "Entity",
                "SimpleType",
            ]
        )

    name = "Khiops Dictionary Language API Docs"
    aliases = ["kdic-api-docs"]
    tokens = {
        "root": [
            (r"\s+", Whitespace),
            (
                r"(Structure)(\s*)(\()([a-zA-Z][a-zA-Z0-9_]*)(\))(\s*)([a-zA-Z0-9_]+)(\()",
                bygroups(
                    Keyword.Type,
                    Whitespace,
                    Punctuation,
                    Name.Function,
                    Punctuation,
                    Whitespace,
                    Name.Function,
                    Punctuation,
                ),
                "arg_list",
            ),
            (
                f"({non_structure_types_regex()})" + r"(\s+)([a-zA-Z0-9_]+)(\s*)(\()",
                bygroups(
                    Keyword.Type, Whitespace, Name.Function, Whitespace, Punctuation
                ),
                "arg_list",
            ),
        ],
        "arg_list": [
            (r"\s+", Whitespace),
            (
                r"(Structure)(\s*)(\()([a-zA-Z][a-zA-Z0-9_]*)(\))(\s+)([a-zA-Z0-9_]+)(\s*)(,?)",
                bygroups(
                    Keyword.Type,
                    Whitespace,
                    Punctuation,
                    Name.Class,
                    Punctuation,
                    Whitespace,
                    Name.Attribute,
                    Whitespace,
                    Punctuation,
                ),
            ),
            (
                f"({non_structure_types_regex()})" + r"(\s+)([a-zA-Z0-9_]+)(\s*)(,?)",
                bygroups(
                    Keyword.Type, Whitespace, Name.Attribute, Whitespace, Punctuation
                ),
            ),
            (r".\[\]", Punctuation),
            (r"\)", Punctuation, "#pop"),
        ],
    }
