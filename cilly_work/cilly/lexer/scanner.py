from .tokens import (
    OPERATORS_SINGLE,
    OPERATORS_DOUBLE,
    KEYWORDS,
    create_token,
    EOF_TOKEN,
)
from ..exceptions import LexerError


class Scanner:
    def __init__(self, source):
        self.source = source
        self.position = -1
        self.current_char = None
        self.advance()

    def advance(self):
        """移动到源代码中的下一个字符"""
        self.position += 1
        if self.position >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.position]

    def peek(self, offset=1):
        """查看源代码中指定偏移量的位置的字符"""
        peek_position = self.position + offset
        if peek_position >= len(self.source):
            return None
        return self.source[peek_position]

    def skip_whitespace(self):
        """跳过空白字符"""
        while self.current_char in [" ", "\t", "\r", "\n"]:
            self.advance()

    def scan_number(self):
        """获取数字类型token。"""
        result = ""
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == ".":
            result += self.current_char
            self.advance()
            while self.current_char and self.current_char.isdigit():
                result += self.current_char
                self.advance()

        if "." in result:
            return create_token("num", float(result))
        else:
            return create_token("num", int(result))

    def scan_string(self):
        """获取字符串类型token"""
        result = ""
        self.advance()  # 开头引号
        while self.current_char and self.current_char != '"':
            result += self.current_char
            self.advance()

        if self.current_char != '"':
            raise LexerError("未终结字符串")

        self.advance()  # 结尾引号
        return create_token("str", result)

    def scan_identifier(self):
        """获取标识符或关键词token"""
        result = ""
        while self.current_char and (
            self.current_char.isalnum() or self.current_char == "_"
        ):
            result += self.current_char
            self.advance()

        if result in KEYWORDS:
            return create_token(result)
        return create_token("id", result)

    def get_next_token(self):
        """获取下一个token"""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                if self.current_char is None:  # 如果跳过空白字符后到达了输入末尾
                    return EOF_TOKEN
                continue

            if self.current_char.isdigit():
                return self.scan_number()

            if self.current_char == '"':
                return self.scan_string()

            if self.current_char.isalpha() or self.current_char == "_":
                return self.scan_identifier()

            # 双运算符
            if self.current_char in OPERATORS_DOUBLE:
                next_char = self.peek()
                if next_char is not None:
                    double_op = self.current_char + next_char
                    if double_op == OPERATORS_DOUBLE[self.current_char]:
                        token = create_token(double_op)
                        self.advance()  # 跳过第一个字符
                        self.advance()  # 跳过第二个字符
                        return token

                # 单运算符
                token = create_token(self.current_char)
                self.advance()
                return token

            # 检查单字符运算符
            if self.current_char in OPERATORS_SINGLE:
                token = create_token(self.current_char)
                self.advance()
                return token

            raise LexerError(f"非法字符: {self.current_char}")

        return EOF_TOKEN


def tokenize(source):
    """源代码分解"""
    scanner = Scanner(source)
    tokens = []
    while True:
        token = scanner.get_next_token()
        tokens.append(token)
        if token == EOF_TOKEN:
            break
    return tokens
