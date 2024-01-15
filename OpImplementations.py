# OpImplementations.py
from CustomeExceptions import *


class Operator:
    def __init__(self, precedence, associativity, name):
        self.precedence = precedence
        self.associativity = associativity
        self.name = name

    def operate(self, *args):
        raise NotImplementedError("Subclasses must override the operate() method.")


# '+'
class Add(Operator):
    def __init__(self):
        super().__init__(precedence=1, associativity='middle', name="Plus: (+)")

    def operate(self, operand1, operand2):
        return operand1 + operand2


# '-'

class Minus(Operator):
    def __init__(self, precedence, associativity):
        super().__init__(precedence, associativity, name="Minus: (-)")

    def operate(self, *args):
        raise NotImplementedError("Subclasses must override the operate() method.")


class BinaryMinus(Minus):
    def __init__(self):
        super().__init__(precedence=1, associativity='middle')

    def operate(self, operand1, operand2):
        return operand1 - operand2


# '*'
class Multiply(Operator):
    def __init__(self):
        super().__init__(precedence=2, associativity='middle', name="Multiplication: (*)")

    def operate(self, operand1, operand2):
        return operand1 * operand2


# '/'
class Divide(Operator):
    def __init__(self):
        super().__init__(precedence=2, associativity='middle', name="Division: (/)")

    def operate(self, operand1, operand2):
        if operand2 == 0:
            raise ValueError("Cannot divide by zero.")
        return operand1 / operand2


# '^'
class Power(Operator):
    def __init__(self):
        super().__init__(precedence=3, associativity='middle', name="Power: (^)")

    def operate(self, operand1, operand2):
        return operand1 ** operand2


# '_'
class UnaryMinus(Minus):
    def __init__(self):
        super().__init__(precedence=3.5, associativity='left')

    def operate(self, operand):
        return -operand


# '%'
class Modulus(Operator):
    def __init__(self):
        super().__init__(precedence=4, associativity='middle', name="Modulus: (-)")

    def operate(self, operand1, operand2):
        return operand1 % operand2


# '@'
class Avg(Operator):
    def __init__(self):
        super().__init__(precedence=5, associativity='middle', name="Average: (@)")

    def operate(self, operand1, operand2):
        return (operand1 + operand2) / 2


# '$'
class Max(Operator):
    def __init__(self):
        super().__init__(precedence=5, associativity='middle', name="Maximum: ($)")

    def operate(self, operand1, operand2):
        if operand1 > operand2:
            return operand1
        else:
            return operand2


# '&'
class Min(Operator):
    def __init__(self):
        super().__init__(precedence=5, associativity='middle', name="Minimum: (&)")

    def operate(self, operand1, operand2):
        if operand1 > operand2:
            return operand2
        else:
            return operand1


# '~'
class Tilde(Operator):
    def __init__(self):
        super().__init__(precedence=6, associativity='left', name="Tilde: (~)")

    def operate(self, operand):
        return -operand


# '!'
class Factorial(Operator):
    def __init__(self):
        super().__init__(precedence=6, associativity='right', name="Factorial: (!)")

    def operate(self, operand1):
        if operand1 < 0:
            raise OperatorError("Factorial is not defined for negative numbers", self)

        result = 1
        for i in range(1, operand1 + 1):
            result *= i
        return result


# '__'
class SignMinus(Minus):
    def __init__(self):
        super().__init__(precedence=8, associativity='left')

    def operate(self, operand):
        return -operand
