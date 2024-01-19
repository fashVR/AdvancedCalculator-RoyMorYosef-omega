# OpImplementations.py
from CustomeExceptions import *


class Operator:
    def __init__(self, precedence, name):
        self.precedence = precedence
        self.name = name

    def operate(self, *args):
        raise NotImplementedError("Subclasses must override the operate() method.")


class Unary(Operator):
    LEFT = 'Left'
    RIGHT = 'Right'
    VALID_ASSOCIATIVITIES = (LEFT, RIGHT)

    def __init__(self, precedence, associativity, repeatable, stackable_on_others, name):
        super().__init__(precedence, name)
        self.stackable_on_others = stackable_on_others
        if associativity not in self.VALID_ASSOCIATIVITIES:
            raise ValueError(f"Associativity must be one of {self.VALID_ASSOCIATIVITIES}")
        self.associativity = associativity
        self.repeatable = repeatable

    def operate(self, operand):
        raise NotImplementedError("Subclasses must override the operate() method.")


class Binary(Operator):
    def __init__(self, precedence, name):
        super().__init__(precedence, name)

    def operate(self, operand1, operand2):
        raise NotImplementedError("Subclasses must override the operate() method.")


# '+'
class Add(Binary):
    def __init__(self):
        super().__init__(precedence=1, name="Plus: (+)")

    def operate(self, operand1, operand2):
        return operand1 + operand2


# '-'


class BinaryMinus(Binary):
    def __init__(self):
        super().__init__(precedence=1, name='Minus: (-)')

    def operate(self, operand1, operand2):
        return operand1 - operand2


# '*'
class Multiply(Binary):
    def __init__(self):
        super().__init__(precedence=2, name="Multiplication: (*)")

    def operate(self, operand1, operand2):
        return operand1 * operand2


# '/'
class Divide(Binary):
    def __init__(self):
        super().__init__(precedence=2, name="Division: (/)")

    def operate(self, operand1, operand2):
        if operand2 == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return operand1 / operand2


# '^'
class Power(Binary):
    def __init__(self):
        super().__init__(precedence=3, name="Power: (^)")

    def operate(self, operand1, operand2):
        if operand1 == 0 and operand2 < 0:
            raise ZeroDivisionError(f"0 cant be raised ny a negative number: ({operand2})")
        return operand1 ** operand2


# '_'
class UnaryMinus(Unary):
    def __init__(self):
        super().__init__(precedence=3.5, associativity='Left', repeatable=True, stackable_on_others=False,
                         name='Minus: (-)')

    def operate(self, operand):
        return -operand


# '%'
class Modulus(Binary):
    def __init__(self):
        super().__init__(precedence=4, name="Modulus: (-)")

    def operate(self, operand1, operand2):
        return operand1 % operand2


# '@'
class Avg(Operator):
    def __init__(self):
        super().__init__(precedence=5, name="Average: (@)")

    def operate(self, operand1, operand2):
        return (operand1 + operand2) / 2


# '$'
class Max(Operator):
    def __init__(self):
        super().__init__(precedence=5, name="Maximum: ($)")

    def operate(self, operand1, operand2):
        if operand1 > operand2:
            return operand1
        else:
            return operand2


# '&'
class Min(Operator):
    def __init__(self):
        super().__init__(precedence=5, name="Minimum: (&)")

    def operate(self, operand1, operand2):
        if operand1 > operand2:
            return operand2
        else:
            return operand1


# '~'
class Tilde(Unary):
    def __init__(self):
        super().__init__(precedence=6, associativity='Left', repeatable=False, stackable_on_others=True,
                         name="Tilde: (~)")

    def operate(self, operand):
        return -operand


# '!'
class Factorial(Unary):
    def __init__(self):
        super().__init__(precedence=6, associativity='Right', repeatable=True, stackable_on_others=True,
                         name="Factorial: (!)")

    def operate(self, operand1):
        if operand1 < 0:
            raise OperatorError("Factorial is not defined for negative numbers", self)

        if operand1 != int(operand1):
            raise OperatorError("Factorial is not defined for non-integer numbers", self)

        result = 1
        for i in range(1, int(operand1) + 1):
            result *= i
        return result


# '__'
class SignMinus(Unary):
    def __init__(self):
        super().__init__(precedence=8, associativity='Left', repeatable=True, stackable_on_others=False,
                         name='Minus: (-)')

    def operate(self, operand):
        return -operand
