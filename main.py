from ITPConverter import *
from InputValidation import *


def main():
    try:
        infix_expression = input("Enter an infix expression: ")
        converter = ITPConverter()
        expression_list = converter.string_to_list(infix_expression)
        check_parentheses(expression_list)
        converter.clean_list(expression_list)
        fixed_minuses = converter.analyze_minuses(expression_list)
        converter.validate_unary_operators(fixed_minuses)
        post_fixed = converter.to_postfix(fixed_minuses)
        res = converter.evaluate_postfix(post_fixed)
        print(res)

    except ParenthesesMismatchError as e:
        print(f"Error | {e}. Mismatch found at index {e.index}")
    except OverflowError:
        print(f"Error | Result too large")
    except InvalidNumberError as e:
        print(f"Error | {e} - Item: {e.invalid_num}")
    except OperatorError as e:
        print(f"Error | {e} - operator: {e.op.name}")
    except KeyboardInterrupt:
        print(f"Error | Keyboard Interrupt")
    except EOFError:
        print(f"Error | End Of File Error")
    except ZeroDivisionError as e:
        print(f"Error | {e}")
    except ValueError as e:
        print(f"Error | {e}")


if __name__ == "__main__":
    main()
