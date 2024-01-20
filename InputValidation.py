from CustomeExceptions import *
from OperatorFactory import *


def check_parentheses(expression_list):
    """
    Checks for mismatched or empty parentheses in an expression list.

    This function iterates through each character in the expression list to ensure that all parentheses are
    correctly matched and none are empty. It raises an error if it finds mismatched or empty parentheses.

    :param expression_list: A list of strings representing mathematical expression elements.
    :raises ParenthesesMismatchError: If mismatched parentheses are found, specifying the type of mismatch.
    """
    open_parentheses_count = 0

    index = 0
    dist = 0
    for char in expression_list:
        if char == '(':
            dist = 0
            open_parentheses_count += 1
        elif char == ')':
            if dist == 1:
                raise ParenthesesMismatchError("Mismatched parentheses: Empty Parenthesis", index)

            if open_parentheses_count == 0:
                raise ParenthesesMismatchError("Mismatched parentheses: Extra closing parenthesis detected", index)
            open_parentheses_count -= 1
        index += 1
        dist += 1
    if open_parentheses_count != 0:
        raise ParenthesesMismatchError("Mismatched parentheses: missing closing parenthesis", len(expression_list))


