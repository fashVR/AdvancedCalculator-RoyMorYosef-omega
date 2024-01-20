from InputHandling.InputProcessingUtilz import *
from InputHandling.InputValidationUtilz import *
from Calculator.ITPConverter import *


def main():
    try:
        operator_factory = OperatorFactory()
        infix_expression = input("Enter an infix expression: ")
        expression_list = InputProcessingUtilz.string_to_list(infix_expression, operator_factory)
        InputProcessingUtilz.clean_list(expression_list)
        InputValidationUtilz.check_parentheses(expression_list)
        fixed_minuses = ITPConverter.analyze_minuses(expression_list)
        InputValidationUtilz.validate_unary_operators(fixed_minuses)
        post_fixed = ITPConverter.to_postfix(fixed_minuses)
        res = ITPConverter.evaluate_postfix(post_fixed)
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
