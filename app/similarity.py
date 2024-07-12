from sympy.logic.boolalg import Boolean, And, Or, Not, Xor
from sympy.core.symbol import symbols

from .parse import Expr, Prod, Term

def conv_term(term: Term) -> Boolean:
    out = None
    # Is this term a variable?
    if isinstance(term.term, str):
        # If so, create a sympy symbol for it
        out = symbols(term.term)
    else:
        # If it isnt a variable, it must be a nested expression
        out = conv_expr(term.term)
    return Not(out) if term.op else out

def conv_prod(prod: Prod) -> Boolean:
    left = conv_term(prod.left)
    right_list = []
    for right in prod.right:
        right_list.append(conv_term(right))
    return And(left, *right_list)

def conv_expr(expr: Expr) -> Boolean:
    result = conv_prod(expr.left)
    for xor, right in expr.right:
        right = conv_prod(right)
        if xor:
            result = Xor(result, right)
        else:
            result = Or(result, right)
    return result
