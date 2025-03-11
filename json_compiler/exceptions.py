"""自定义异常类"""


class JSONError(Exception):

    def __init__(self, line: int, column: int, message: str):
        super().__init__(f"[行 {line}, 列 {column}] {message}")
        self.line = line
        self.column = column


class JSONLexError(JSONError):
    pass


class JSONParseError(JSONError):
    pass
