from CustomeExceptions import *
from OperatorFactory import *


def check_parentheses(expression_list):
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


def check_valid_nums(expression_list):
    if not expression_list:
        raise ValueError("input empty")

    def is_valid_number(num):

        has_decimal = False
        has_digit = False

        for char in num:
            if char.isdigit():
                has_digit = True
            elif char == '.':
                if has_decimal:
                    raise InvalidNumberError("a number cannot have more than 1 decimal point", num)
                elif not has_digit:
                    raise InvalidNumberError("a number must have a value before the decimal point", num)

                has_decimal = True
            else:
                raise InvalidNumberError("invalid character in number", num)
        return True

    op_factory = OperatorFactory()
    for item in expression_list:
        if item in op_factory.operators or item in ['(', ')']:
            continue
        is_valid_number(item)
