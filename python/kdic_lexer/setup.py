from setuptools import setup, find_packages

setup(
    name="kdic-lexer",
    version="0.1",
    description="A Khiops Dictionary Pygments Lexer",
    author="Your Name",
    author_email="khiops.team@orange.com",
    packages=find_packages(),
    install_requires=["Pygments>=2.0"],
    entry_points={
        "pygments.lexers": [
            "kdic = kdic_lexer:KdicLexer",
            "kdic-api-docs = kdic_lexer:KdicApiDocsLexer",
        ],
    },
)
