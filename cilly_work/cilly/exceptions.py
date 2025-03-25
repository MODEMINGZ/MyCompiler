class CillyError(Exception):
    def __init__(self, message, source=None):
        self.message = message
        self.source = source
        super().__init__(f"{source + ' : ' if source else ''}{message}")


class LexerError(CillyError):
    def __init__(self, message):
        super().__init__(message, "cilly lexer")


class ParserError(CillyError):
    def __init__(self, message):
        super().__init__(message, "cilly parser")
