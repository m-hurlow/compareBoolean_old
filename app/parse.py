from .lex import Token, TokenType

class Term:
    def __init__(self, term, op: bool = False):
        self.term = term
        self.op = op

    def __str__(self) -> str:
        out = "" if not self.op else "!"
        return out + str(self.term)

class Prod:
    def __init__(self, left: Term, right: list[Term] = None):
        self.left = left
        self.right = right
    
    def __str__(self) -> str:
        out = "(" + str(self.left)
        for right in self.right:
            out += f" & {str(right)}"
        return out + ")"

class Expr:
    def __init__(self, left: Prod, right: list[bool, Prod] = None):
        self.left = left
        self.right = right
    
    def __str__(self) -> str:
        out = "(" + str(self.left)
        for xor, right in self.right:
            out += f" {'^' if xor else '|'} {str(right)}"
        return out + ")"
 
def expect(tokens: list[Token], type: TokenType) -> bool:
    token = tokens.pop()
    if token.type == type:
        return True
    else:
        tokens.append(token)
        return False

# Grammar:
# expr = prod ([or | xor] prod)*
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
    next_token = tokens[-1].type
    while expect(tokens, TokenType.OR) or expect(tokens, TokenType.XOR):
        new_right = parse_prod(tokens)
        if new_right == None:
            return None
        print(f"New right: {new_right}")
        right.append((next_token == TokenType.XOR, new_right))
        next_token = tokens[-1].type
    
    return Expr(left, right)
