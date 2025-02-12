#regex.py
from collections import deque
from abc import ABC, abstractmethod
"""
RegExpr
"""
class RegExpr(ABC):
    @abstractmethod
    def __str__(self):
        pass

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "__str__" not in cls.__dict__:
           raise NotImplementedError(f"Require student implementation: {cls.__name__}.__str__()")

class RNoString(RegExpr):
    def __str__(self):
        return "RNoString"

class REmptyString(RegExpr):
    def __str__(self):
        return "REmptyString"

class RSingle(RegExpr):
    __match_args__ = ("char",)

    def __init__(self, char: str):
        self.char = char

    def __str__(self):
        return f"RSingle('{self.char}')"

class RConcat(RegExpr):
    __match_args__ = ("left", "right")

    def __init__(self, left: RegExpr, right: RegExpr):
        self.left = left
        self.right = right

    def __str__(self):
        return f"RConcat({self.left},{self.right})"

class RUnion(RegExpr):
    __match_args__ = ("left", "right")

    def __init__(self, left: RegExpr, right: RegExpr):
        self.left = left
        self.right = right

    def __str__(self):
        return f"RUnion({self.left},{self.right})"

class RStar(RegExpr):
    __match_args__ = ("expr",)

    def __init__(self, expr: RegExpr):
        self.expr = expr

    def __str__(self):
        return f"RStar({self.expr})"

class RPlus(RegExpr):
    __match_args__ = ("expr",)

    def __init__(self, expr: RegExpr):
        self.expr = expr

    def __str__(self):
        return f"RPlus({self.expr})"

class ROption(RegExpr):
    __match_args__ = ("expr",)

    def __init__(self, expr: RegExpr):
        self.expr = expr

    def __str__(self):
        return f"ROption({self.expr})"

class RAny(RegExpr):
    def __str__(self):
        return "RAny"
    

"""
Parsing
"""
def parse_regex(regex_string: str) -> RegExpr:
    tokens = deque(regex_string)
    def parse_primary(tokens: deque[str]) -> RegExpr:
        token = tokens.popleft()

        match token:
            case '(':
                expr = parse_union(tokens)
                tokens.popleft()
                return expr

            case '.':
                return RAny()

            case _ if token.isalnum():
                return RSingle(token)

        raise ValueError(f"Unexpected token: {token}")

    def parse_unary(tokens: deque[str]) -> RegExpr:
        expr = parse_primary(tokens)

        while tokens and tokens[0] in '*+?':
            token = tokens.popleft()

            match token:
                case '*':
                    expr = RStar(expr)

                case '+':
                    expr = RPlus(expr)

                case '?':
                    expr = ROption(expr)

        return expr

    def parse_concat(tokens: deque[str]) -> RegExpr:
        expr = parse_unary(tokens)

        while tokens and (tokens[0].isalnum() or tokens[0] in "(."):
            next_expr = parse_unary(tokens)
            if expr is not None:
                expr = RConcat(expr, next_expr)
            else:
                expr = next_expr

        return expr

    def parse_union(tokens: deque[str]) -> RegExpr:
        expr = parse_concat(tokens)

        while tokens and tokens[0] == '|':
            tokens.popleft()
            expr = RUnion(expr, parse_concat(tokens))

        return expr

    return parse_union(tokens)