from InputHandling.InputProcessingUtilz import *
from InputHandling.InputValidationUtilz import *
from Calculator.ITPConverter import *


def calculate(expression):
    expression_list = InputProcessingUtilz.string_to_list(expression)
    InputProcessingUtilz.clean_list(expression_list)
    processed_expression = ''.join(map(str, expression_list))  # Convert list back to string

    InputValidationUtilz.check_parentheses(expression_list)
    ITPConverter.analyze_minuses(expression_list)
    print(expression_list)
    InputValidationUtilz.validate_unary_operators(expression_list)
    post_fixed = ITPConverter.to_postfix(expression_list)
    result = ITPConverter.evaluate_postfix(post_fixed)

    return processed_expression, result


def main():
    while True:
        try:
            infix_expression = input("Insert an expression (insert stop in order to stop): \n")
            if infix_expression == 'stop':
                print("Stopping the program.")
                return

            processed_expression, result = calculate(infix_expression)
            print(f"{processed_expression} = {result}")

        except ParenthesesMismatchError as e:
            print(f"Error | {e}. Mismatch found at index {e.index}")
        except OverflowError:
            print(f"Error | Result too large")
        except InvalidNumberError as e:
            print(f"Error | {e} - Item: {e.invalid_num}")
        except OperatorError as e:
            print(f"Error | {e} - operator: {e.op.name}")
        except KeyboardInterrupt:
            print("Stopping the program.")
            return
        except EOFError:
            print(f"Error | End Of File Error")
        except ZeroDivisionError as e:
            print(f"Error | {e}")
        except ValueError as e:
            print(f"Error | {e}")




if __name__ == "__main__":
    main()
