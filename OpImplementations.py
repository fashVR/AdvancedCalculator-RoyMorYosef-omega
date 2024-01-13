# OpImplementations.py

class Operator:
    def __init__(self, precedence, op_num):
        self.precedence = precedence
        self.op_num = op_num

    def operate(self, *args):
        raise NotImplementedError("Subclasses must override the operate() method.")


# '+'
class Add(Operator):
    def __init__(self):
        super().__init__(precedence=1, op_num=2)

    def operate(self, operand1, operand2):
        return operand1 + operand2


# '-'
class BinaricMinus(Operator):
    def __init__(self):
        super().__init__(precedence=1, op_num=2)

    def operate(self, operand1, operand2):
        return operand1 - operand2


# '*'
class Multiply(Operator):
    def __init__(self):
        super().__init__(precedence=2, op_num=2)

    def operate(self, operand1, operand2):
        return operand1 * operand2


# '/'
class Divide(Operator):
    def __init__(self):
        super().__init__(precedence=2, op_num=2)

    def operate(self, operand1, operand2):
        if operand2 == 0:
            raise ValueError("Cannot divide by zero.")
        return operand1 / operand2


# '^'
class Power(Operator):
    def __init__(self):
        super().__init__(precedence=3, op_num=2)

    def operate(self, operand1, operand2):
        return operand1 ** operand2


# '_'
class UnaricMinus(Operator):
    def __init__(self):
        super().__init__(precedence=3.5, op_num=1)

    def operate(self, operand):
        return -operand


# '%'
class Modulus(Operator):
    def __init__(self):
        super().__init__(precedence=4, op_num=2)

    def operate(self, operand1, operand2):
        return operand1 % operand2


# '@'
class Avg(Operator):
    def __init__(self):
        super().__init__(precedence=5, op_num=2)

    def operate(self, operand1, operand2):
        return (operand1 + operand2) / 2


# '$'
class Max(Operator):
    def __init__(self):
        super().__init__(precedence=5, op_num=2)

    def operate(self, operand1, operand2):
        if operand1 > operand2:
            return operand1
        else:
            return operand2


# '&'
class Min(Operator):
    def __init__(self):
        super().__init__(precedence=5, op_num=2)

    def operate(self, operand1, operand2):
        if operand1 > operand2:
            return operand2
        else:
            return operand1


# '~'
class Tilde(Operator):
    def __init__(self):
        super().__init__(precedence=6, op_num=1)

    def operate(self, operand):
        return -operand


# '!'
class Factorial(Operator):
    def __init__(self):
        super().__init__(precedence=6, op_num=1)

    def operate(self, operand1):
        if operand1 < 0:
            raise ValueError("Factorial is not defined for negative numbers")

        result = 1
        for i in range(1, operand1 + 1):
            result *= i
        return result


# '__'
class SignMinus(Operator):
    def __init__(self):
        super().__init__(precedence=8, op_num=1)

    def operate(self, operand):
        return -operand
