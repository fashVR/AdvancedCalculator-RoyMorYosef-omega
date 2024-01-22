import pytest
from Calculator import main
from Calculator.CustomeExceptions import *


@pytest.mark.parametrize("expression, expected_result", [
    # invalid expressions
    ("4^*4", "Caught"),
    ("afe#cw1", "Caught"),
    ("     ", "Caught"),
    (" \n\r\f", "Caught"),
    ("4\n\r\f4 - 4", "Caught"),

    # simple expressions
    ("3+4", 7),
    ("2-3", -1),
    ("--2!", 2),
    ("2---2!", 0),
    ("4*5", 20),
    ("4/8", 0.5),
    ("4^2", 16),
    ("4 % 2", 0),
    ("10 @ 5", 7.5),
    ("10 $ 5", 10),
    ("10 & 5", 5),
    ("~-1", 1),
    ("5!", 120),
    ("1.23#", 6),

    # complex expressions
    (" 4 + 5*(2-8)^2 -- 6 % 4 ^ 2 ", 180),
    ("-1- 2-3*(16# & 8 $ 7.5) -- 2 + 9", -14.5),
    ("(1-2) + ~(2-6*9) - 6 --- 3!", 39),
    ("(90 + -89) * (2)*2*(3) - ~ - 9", 3),
    ("-4^2 +3! - ~2& 6 / 2", -9),
    ("~-2!+(4)!# / 3 - 9.2 % 9", 3.8),
    ("2--3*2^3! # + 6.9*23", 352.7),
    ("89 * 2---6#-(--4^3)#!", -3628628),
    ("4^2^2---6!  + (1 + --1 -1 +1)", -462),
    ("9.99^ 2 + 4-12.5# / 3 - 6", 95.1334333333),
    ("19/ 2 - (44 ---3^2 /7) + 16", -17.2142857143),
    ("4@3#! -5&7$6 - (30 % 4) ", -3),
    ("(90099# - 982#)# / 7 + --2! ", 3.1428571429),
    ("(4##)#!# + 5!# - ~ - 7", 2),
    ("((23- 7) - (1)!*(2*(3)!!#)#)", 7),
    ("(~---3! & (8/ 1.4))  @ 9", 7.3571428572),
    ("--7 - 9 + ~ 2 - 6 / 3 + ~- 4", -2),
    ("(2-(-2-(2-2)))! / 7.235 + 98", 101.3172080166)

])
def test_valid_expressions(expression, expected_result):
    try:

        processed_expression, res = main.calculate(expression)
        assert res == expected_result


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
