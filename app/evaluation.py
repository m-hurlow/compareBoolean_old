from typing import Any, TypedDict

from .lex import Lexer
from .parse import parse_boolean, print_expr

class Params(TypedDict):
    pass


class Result(TypedDict):
    is_correct: bool
    

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

    tokens = Lexer(response).lex()
    for token in tokens:
        print(str(token))
    expr = parse_boolean(list(reversed(tokens)))
    print(print_expr(expr))

    return Result(is_correct=True)
