from .lex import Token, TokenType

class Term:
    def __init__(self, term, op: bool = False):
        self.term = term
        self.op = op

    def __str__(self) -> str:
        return f"!{str(self.term)}" if self.op else str(self.term)

class Prod:
    def __init__(self, left: Term, right: list[Term] = None):
        self.left = left
        self.right = right
    
    def __str__(self) -> str:
        return f"({str(self.left)}{f' & {str(self.right)}' if self.right == None else '' })"

class Expr:
    def __init__(self, left: Prod, right: list[Prod] = None):
        self.left = left
        self.right = right
    
    def __str__(self) -> str:
        return f"({str(self.left)}{f' | {str(self.right)}' if self.right == None else '' })"
 
def expect(tokens: list[Token], type: TokenType) -> bool:
    token = tokens.pop()
    if token.type == type:
        return True
    else:
        tokens.append(token)
        return False

# Grammar:
# expr = prod (or prod)*
# prod = term (and term)*
# term = (unary) [variable | '(' expr ')']

def parse_term(tokens: list[Token]) -> Term:
    print("Parsing term")
    op = expect(tokens, TokenType.NOT)
    print(f"Op: {op}")
    if tokens[-1].type == TokenType.VARIABLE:
        print("Attempting to parse variable")
        term = tokens.pop().value
        print(f"Term: {term}")
        return Term(term, op)
    elif expect(tokens, TokenType.LBRACKET):
        print("Attempting to parse bracketed expr")
        term = parse_boolean(tokens)
        if term == None:
            return None
        if not expect(tokens, TokenType.RBRACKET):
            return None
        print(f"Term: {term}")
        return Term(term, op)
    else:
        return None

def parse_prod(tokens: list[Token]) -> Prod:
    print("Parsing product")

    left = parse_term(tokens)
    if left == None:
        return None
    print(f"Left: {left}")
    right = []
    while expect(tokens, TokenType.AND):
        new_right = parse_term(tokens)
        if new_right == None:
            return None
        print(f"New right: {right}")
        right.append(new_right)
    
    return Prod(left, right)

# A recursive descent parser
def parse_boolean(tokens: list[Token]) -> Expr:
    print("Parsing boolean")

    left = parse_prod(tokens)
    if left == None:
        return None
    print(f"Left: {left}")
    right = []
    while expect(tokens, TokenType.OR):
        new_right = parse_prod(tokens)
        if new_right == None:
            return None
        print(f"New right: {new_right}")
        right.append(new_right)
    
    return Expr(left, right)

def print_term(term: Term):
    out = ""
    if term.op:
        out += '!'
    if isinstance(term.term, str):
        out += term.term
    else:
        out += print_expr(term.term, rec=True)
    return out

def print_prod(prod: Prod):
    out = "(" + print_term(prod.left)
    for right in prod.right:
        out += f" & {print_term(right)}"
    return out + ")"

def print_expr(expr: Expr, rec=False):
    out = "(" + print_prod(expr.left)
    for right in expr.right:
        out += f" | {print_prod(right)}"
    return out + ")" + ("" if rec else "\n")