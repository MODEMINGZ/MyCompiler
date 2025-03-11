"""将JSON字符串转换成TOKEN流"""

from .tokens import Token, TokenType
from ..exceptions import JSONLexError


class JSONLexer:
    def __init__(self, source: str):
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def get_tokens(self) -> list[Token]:
        if len(self.tokens) == 0:
            self.scan_tokens()

        return self.tokens

    def scan_tokens(self) -> list[Token]:
        while not self._is_end():
            self.start = self.current
            char = self._next()

            if char in " \r\t":
                self.column += 1
                continue
            elif char == "\n":
                self.line += 1
                self.column = 1
            elif char == '"':
                self._string()
            elif char.isdigit() or char == "-" or char == ".":
                self._number()
            elif char == "t":
                self._keyword("true", TokenType.TRUE, True)
            elif char == "f":
                self._keyword("false", TokenType.FALSE, False)
            elif char == "n":
                self._keyword("null", TokenType.NULL, None)
            elif char == "{":
                self._add_token(TokenType.LBRACE)
            elif char == "}":
                self._add_token(TokenType.RBRACE)
            elif char == "[":
                self._add_token(TokenType.LBRACKET)
            elif char == "]":
                self._add_token(TokenType.RBRACKET)
            elif char == ",":
                self._add_token(TokenType.COMMA)
            elif char == ":":
                self._add_token(TokenType.COLON)
            else:
                raise JSONLexError(self.line, self.column, f"非法字符 '{char}'")

        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))

        return self.tokens

    def _string(self):
        start_line = self.line
        start_column = self.column
        value = ""

        char = self._peek()
        while char != '"' and not self._is_end():
            if char == "\\":
                self._next()
                next_char = self._next()
                value += self._escape_char(next_char)
            else:
                value += self._next()
            char = self._peek()

        if self._is_end():
            raise JSONLexError(start_line, start_column, f"未闭合字符串")

        self._next()  # 跳过闭合的"
        self._add_token(TokenType.STRING, value)

    def _escape_char(self, char: str) -> str:
        escapes = {'"': '"', "\\": "\\", "n": "\n", "r": "\r", "t": "\t"}
        return escapes.get(char, char)

    def _keyword(self, target: str, token_type: str, value: any):
        for ch in target[1:]:  # 第一个字符已匹配
            if self._peek() != ch:
                raise JSONLexError(self.line, self.column, f"无效关键字")
            self._next()
        self._add_token(token_type, value)

    def _number(self):
        value_str = ""
        is_float = False

        # 处理第一个字符（负号或数字）
        first_char = self._peek_prev()
        if first_char == "-":
            value_str = "-"
        elif first_char.isdigit():
            value_str = first_char

        # 处理整数部分
        if not first_char.isdigit() and not self._peek().isdigit():
            raise JSONLexError(self.line, self.column, "数字必须包含整数部分")

        while self._peek().isdigit():
            value_str += self._next()

        # 处理小数点和小数部分
        if self._peek() == ".":
            is_float = True
            value_str += self._next()
            # 确保小数点后面有至少一个数字
            if not self._peek().isdigit():
                raise JSONLexError(self.line, self.column, "小数点后必须有数字")
            while self._peek().isdigit():
                value_str += self._next()

        # 处理指数部分
        if self._peek().lower() == "e":
            is_float = True
            value_str += self._next()
            if self._peek() in ("+", "-"):
                value_str += self._next()
            if not self._peek().isdigit():
                raise JSONLexError(self.line, self.column, "指数部分必须有数字")
            while self._peek().isdigit():
                value_str += self._next()

        try:
            value = float(value_str) if is_float else int(value_str)
            self._add_token(TokenType.NUMBER, value)
        except ValueError:
            raise JSONLexError(self.line, self.column, f"无效的数字格式: {value_str}")

    def _is_end(self) -> bool:
        return self.current >= len(self.source)

    def _next(self) -> str:
        char = self.source[self.current]
        self.current += 1
        self.column += 1
        return char

    def _add_token(self, token_type: str, value: any = None):
        token = Token(
            token_type=token_type,
            value=value,
            line=self.line,
            column=self.column - (self.current - self.start),
        )
        self.tokens.append(token)

    def _peek(self, offset: int = 0) -> str:
        pos = self.current + offset
        if pos < 0 or pos >= len(self.source):
            return "\0"
        else:
            return self.source[pos]

    def _peek_prev(self) -> str:
        return self.source[self.current - 1] if self.current > 0 else "\0"
