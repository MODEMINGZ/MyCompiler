"""Token类型定义"""

OPERATORS_SINGLE = ["(", ")", "{", "}", ",", ";", "+", "-", "*", "/"]

OPERATORS_DOUBLE = {
    ">": ">=",
    "<": "<=",
    "=": "==",
    "!": "!=",
    "&": "&&",
    "|": "||",
}

KEYWORDS = [
    "var",
    "if",
    "else",
    "while",
    "break",
    "continue",
    "return",
    "fun",
    "print",
]


def create_token(tag, value=None):
    return [tag, value]


def get_token_tag(token):
    return token[0]


def get_token_value(token):
    return token[1]


# EOF
EOF_TOKEN = create_token("eof")
