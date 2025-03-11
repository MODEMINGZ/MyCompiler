"""Token定义"""


class Token:

    def __init__(
        self, token_type: str, value: any = None, line: int = None, column: int = None
    ):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        # 自定义返回内容
        return f"<Token {self.token_type} {repr(self.value)}>"


class TokenType:
    NUMBER = "NUMBER"
    STRING = "STRING"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NULL = "NULL"
    LBRACKET = "["
    RBRACKET = "]"
    COMMA = ","
    LBRACE = "{"
    RBRACE = "}"
    COLON = ":"
    EOF = "EOF"
