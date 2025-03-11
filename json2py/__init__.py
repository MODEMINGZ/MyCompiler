__all__ = ["JSONLexer", "JSONParser", "json_to_python"]

from .lexer.scanner import JSONLexer
from .parser.parser import JSONParser


def json_to_python(json_str: str) -> any:
    """将 JSON 字符串转换为 Python 对象"""
    lexer = JSONLexer(json_str)
    tokens = lexer.scan_tokens()
    parser = JSONParser(tokens)
    return parser.parse()
