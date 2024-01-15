from ITPConverter import *
from InputValidation import *


def receive_input():
    expression = input()


def pre_calc_validate(infix_expression):
    converter = ITPConverter()
    expression_list = converter.string_to_list_of_chars(infix_expression)
    new_string = converter.analyze_minuses(expression_list)

    print(new_string)
    try:
        check_parentheses(expression_list)
    except ParenthesesMismatchError as e:
        print(f"Error | {e}. Mismatch found at index {e.index}")

    try:
        check_valid_nums(expression_list)
    except InvalidNumberError as e:
        print(f"Error | {e} - Invalid Item: {e.invalid_num}")




def main():

    try:
        infix_expression = input("Enter an infix expression: ")
        converter = ITPConverter()
        expression_list = converter.string_to_list_of_chars(infix_expression)
        check_parentheses(expression_list)
        check_valid_nums(expression_list)
        fixed_minuses = converter.analyze_minuses(expression_list)
        post_fixed = converter.to_postfix(fixed_minuses)
        res = converter.evaluate_postfix(post_fixed)
        print(res)
    except ParenthesesMismatchError as e:
        print(f"Error | {e}. Mismatch found at index {e.index}")
    except InvalidNumberError as e:
        print(f"Error | {e} - Invalid Item: {e.invalid_num}")
    except OperatorError as e:
        print(f"Error | {e} - operator: {e.op.name}")
    except KeyboardInterrupt:
        print(f"Error | Keyboard Interrupt")
    except EOFError:
        print(f"Error | End Of File Error")
    except ValueError as e:
        print(f"Error | {e}")


if __name__ == "__main__":
    main()
