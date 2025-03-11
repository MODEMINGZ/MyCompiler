"""词法分析器"""

__all__ = ["Token", "TokenType", "JSONLexer"]

from .tokens import Token, TokenType
from .scanner import JSONLexer
