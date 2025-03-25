from ..exceptions import ParserError
from ..lexer.tokens import get_token_tag, get_token_value, EOF_TOKEN


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.position = -1
        self.advance()

    def advance(self):
        """移动到下个token"""
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = EOF_TOKEN

    def peek(self, offset=0):
        """查看前面的token"""
        peek_position = self.position + offset
        if peek_position >= len(self.tokens):
            return EOF_TOKEN
        return get_token_tag(self.tokens[peek_position])

    def match(self, expected_tag):
        """匹配当前token和预期token"""
        current_tag = get_token_tag(self.current_token)
        if current_tag != expected_tag:
            raise ParserError(f"意外 {expected_tag}, 发现 {current_tag}")
        token = self.current_token
        self.advance()
        return token

    def parse(self):
        """解析入口"""
        return self.program()

    def program(self):
        """解析源代码程序"""
        statements = []
        while get_token_tag(self.current_token) != "eof":
            statements.append(self.statement())
        return ["program", statements]

    def statement(self):
        """解析语句"""
        if self.peek() == "var":
            return self.define_statement()
        elif self.peek() == "id" and self.peek(1) == "=":
            return self.assign_statement()
        elif self.peek() == "print":
            return self.print_statement()
        elif self.peek() == "if":
            return self.if_statement()
        elif self.peek() == "while":
            return self.while_statement()
        elif self.peek() == "break":
            return self.break_statement()
        elif self.peek() == "continue":
            return self.continue_statement()
        elif self.peek() == "return":
            return self.return_statement()
        elif self.peek() == "for":
            return self.for_statement()
        elif self.peek() == "fun":
            return self.fun_statement()
        elif self.peek() == "{":
            return self.block_statement()
        else:
            return self.expr_statement()

    def define_statement(self):
        """定义语句"""
        self.match("var")
        identifier = get_token_value(self.match("id"))
        self.match("=")
        expr = self.expr()
        self.match(";")
        return ["define", identifier, expr]

    def assign_statement(self):
        """赋值语句"""
        identifier = get_token_value(self.match("id"))
        self.match("=")
        expr = self.expr()
        self.match(";")
        return ["assign", identifier, expr]

    def print_statement(self):
        """打印语句"""
        self.match("print")
        self.match("(")
        args = self.args() if self.peek() != ")" else []
        self.match(")")
        self.match(";")
        return ["print", args]

    def if_statement(self):
        """条件语句"""
        self.match("if")
        self.match("(")
        condition = self.expr()
        self.match(")")
        true_branch = self.statement()
        false_branch = None
        if self.peek() == "else":
            self.match("else")
            false_branch = self.statement()
        return ["if", condition, true_branch, false_branch]

    def while_statement(self):
        """循环语句"""
        self.match("while")
        self.match("(")
        condition = self.expr()
        self.match(")")
        body = self.statement()
        return ["while", condition, body]

    def break_statement(self):
        """中断语句"""
        self.match("break")
        self.match(";")
        return ["break"]

    def continue_statement(self):
        """继续语句"""
        self.match("continue")
        self.match(";")
        return ["continue"]

    def return_statement(self):
        """返回语句"""
        self.match("return")
        expr = self.expr() if self.peek() != ";" else None
        self.match(";")
        return ["return", expr]

    def block_statement(self):
        """块语句"""
        self.match("{")
        statements = []
        while self.peek() != "}":
            statements.append(self.statement())
        self.match("}")
        return ["block", statements]

    def expr_statement(self):
        """表达式语句"""
        expr = self.expr()
        self.match(";")
        return ["expr_statement", expr]

    def for_statement(self):
        """循环语句"""
        self.match("for")
        self.match("(")
        init = self.statement()
        condition = self.statement()
        update = self.statement()
        self.match(")")
        body = self.statement()
        return ["for", init, condition, update, body]

    def fun_statement(self):
        """函数定义语句"""
        self.match("fun")
        name = get_token_value(self.match("id"))
        self.match("(")
        params = self.params() if self.peek() != ")" else []
        self.match(")")
        body = self.block_statement()
        return ["fun_def", name, params, body]

    def expr(self, bp=0):
        """解析表达式"""
        token = self.current_token
        self.advance()

        left = self.nud(token)

        while (
            bp < self.lbp(self.current_token)
            and get_token_tag(self.current_token) != ";"
        ):
            token = self.current_token
            self.advance()
            left = self.led(left, token)

        return left

    def nud(self, token):
        """处理前缀运算符，不需要右侧表达式部分，空标记null denotation"""
        """"""
        tag = get_token_tag(token)
        if tag in ["num", "id", "str", "true", "false", "null"]:
            return token
        elif tag == "(":
            expr = self.expr()
            self.match(")")
            return expr
        elif tag in ["-", "!"]:
            return ["unary", tag, self.expr(90)]
        elif tag == "fun":
            # 函数表达式：fun(params) { body }
            self.match("(")
            params = self.params() if self.peek() != ")" else []
            self.match(")")
            body = self.block_statement()
            return ["fun", params, body]
        else:
            raise ParserError(f"意外的token: {tag}")

    def led(self, left, token):
        """处理中缀运算符左标记Left Denotation"""
        tag = get_token_tag(token)
        if tag == "(":
            args = self.args() if self.peek() != ")" else []
            self.match(")")
            return ["call", left, args]
        elif tag == "?":
            middle = self.expr()
            self.match(":")
            right = self.expr(self.lbp(token) - 1)  # 右结合
            return ["ternary", left, middle, right]
        elif tag == "^":
            right = self.expr(self.lbp(token) - 1)
            return ["binary", tag, left, right]
        elif tag in ["*", "/", "+", "-", ">", ">=", "<", "<=", "==", "!=", "&&", "||"]:
            right = self.expr(self.lbp(token))
            return ["binary", tag, left, right]
        else:
            raise ParserError(f"意外的token: {tag}")

    def lbp(self, token):
        """返回token左结合的权值left binding power"""
        tag = get_token_tag(token)
        if tag == "?":
            return 5
        elif tag in ["||"]:
            return 10
        elif tag in ["&&"]:
            return 20
        elif tag in ["==", "!="]:
            return 30
        elif tag in [">", ">=", "<", "<="]:
            return 40
        elif tag in ["+", "-"]:
            return 50
        elif tag in ["*", "/"]:
            return 60
        elif tag == "^":
            return 70
        elif tag == "(":
            return 80
        else:
            return 0

    def fun_expr(self):
        """函数表达式"""
        self.match("fun")
        self.match("(")
        params = self.params() if self.peek() != ")" else []
        self.match(")")
        body = self.block_statement()
        return ["fun", params, body]

    def args(self):
        """函数参数"""
        args = [self.expr()]
        while self.peek() == ",":
            self.match(",")
            args.append(self.expr())
        return args

    def params(self):
        """函数参数"""
        params = [get_token_value(self.match("id"))]
        while self.peek() == ",":
            self.match(",")
            params.append(get_token_value(self.match("id")))
        return params


def parse(tokens):
    """解析token到抽象语法树"""
    parser = Parser(tokens)
    return parser.parse()
