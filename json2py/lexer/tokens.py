"""Token定义"""


class Token:
    type: str
    value: any = None
    # 行号和列号,用于定位错误
    line: int
    column: int

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
