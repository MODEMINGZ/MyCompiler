"""递归下降地将Token流解析为Python数据结构list/dict"""

from ..lexer.tokens import Token, TokenType
from ..exceptions import JSONParseError


class JSONParser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> any:
        """入口方法"""
        if not self.tokens:
            return None
        return self._parse_value()

    def _parse_value(self) -> any:
        token = self._next()

        if token.token_type == TokenType.LBRACKET:
            return self._parse_list()
        elif token.token_type == TokenType.LBRACE:
            return self._parse_dict()
        elif token.token_type == TokenType.STRING:
            return token.value
        elif token.token_type == TokenType.NUMBER:
            return token.value
        elif token.token_type == TokenType.TRUE:
            return True
        elif token.token_type == TokenType.FALSE:
            return False
        elif token.token_type == TokenType.NULL:
            return None
        else:
            self._error(token, "语法错误")

    def _parse_dict(self) -> dict:
        obj = {}
        while not self._check(TokenType.RBRACE):
            key = self._consume(TokenType.STRING, "字典键必须是字符串").value
            self._consume(TokenType.COLON, "字典键后缺少冒号")
            value = self._parse_value()
            obj[key] = value
            if not self._match(TokenType.COMMA):
                break
        self._consume(TokenType.RBRACE, "字典缺少闭合'}'")
        return obj

    def _parse_list(self) -> list:
        arr = []
        while not self._check(TokenType.RBRACKET):
            arr.append(self._parse_value())  # 递归调用
            if not self._match(TokenType.COMMA):
                break
        self._consume(TokenType.RBRACKET, "列表缺少闭合']'")
        return arr

    def _consume(self, token_type: str, error_msg: str) -> Token:
        # 必须消费指定类型的Token
        if self._check(token_type):
            return self._next()
        else:
            token = self.tokens[self.current]
            self._error(token, error_msg)

    def _match(self, token_type: str) -> bool:
        if self._check(token_type):
            self.current += 1
            return True
        return False

    def _check(self, token_type: str) -> bool:
        if self.current >= len(self.tokens):
            return False

        return self.tokens[self.current].token_type == token_type

    def _next(self) -> Token:
        if self.current >= len(self.tokens):
            return self.tokens[-1]  # 返回EOF
        token = self.tokens[self.current]
        self.current += 1
        return token

    def _error(self, token: Token, message: str):
        raise JSONParseError(
            line=token.line,
            column=token.column,
            message=f"{message}，实际遇到 {token.token_type}",
        )
