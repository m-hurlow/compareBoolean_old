from typing import Any, TypedDict

from sympy.logic.boolalg import Boolean, simplify_logic

from .lex import Lexer
from .parse import parse_boolean
from .similarity import conv_expr

class Params(TypedDict):
    pass


class Result(TypedDict):
    is_correct: bool
    
def get_sympy_expr(input: str) -> Boolean:
    # Tokenise the input string
    tokens = Lexer(input).lex()
    for token in tokens:
        print(str(token))
    # Attempt to parse the tokens into an AST
    expr = parse_boolean(list(reversed(tokens)))
    print(expr)

    if expr == None:
        return None

    # Walk the tree, converting the result into a sympy boolean expression
    sympy_expr = conv_expr(expr)
    print(sympy_expr)
    return sympy_expr

def evaluation_function(response: Any, answer: Any, params: Params) -> Result:
    """
    Function used to evaluate a student response.
    ---
    The handler function passes three arguments to evaluation_function():

    - `response` which are the answers provided by the student.
    - `answer` which are the correct answers to compare against.
    - `params` which are any extra parameters that may be useful,
        e.g., error tolerances.

    The output of this function is what is returned as the API response
    and therefore must be JSON-encodable. It must also conform to the
    response schema.

    Any standard python library may be used, as well as any package
    available on pip (provided it is added to requirements.txt).

    The way you wish to structure you code (all in this function, or
    split into many) is entirely up to you. All that matters are the
    return types and that evaluation_function() is the main function used
    to output the evaluation response.
    """

    response_expr = get_sympy_expr(response)
    answer_expr = get_sympy_expr(answer)

    return Result(is_correct=simplify_logic(response_expr, form="cnf").equals(simplify_logic(answer_expr, form="cnf")))
