# OpImplementations.py

class Operator:
    def __init__(self, precedence, associativity):
        self.precedence = precedence
        self.associativity = associativity

    def operate(self, operand1, operand2):
        raise NotImplementedError("Subclasses must override the operate() method.")


# '+'
class Add(Operator):
    def __init__(self):
        super().__init__(precedence=1, associativity='left')

    def operate(self, operand1, operand2):
        return operand1 + operand2

# '-'
class Subtract(Operator):
    def __init__(self):
        super().__init__(precedence=1, associativity='left')

    def operate(self, operand1, operand2):
        return operand1 - operand2

# '+'
class Multiply(Operator):
    def __init__(self):
        super().__init__(precedence=2, associativity='left')

    def operate(self, operand1, operand2):
        return operand1 * operand2

# '+'
class Divide(Operator):
    def __init__(self):
        super().__init__(precedence=2, associativity='left')

    def operate(self, operand1, operand2):
        if operand2 == 0:
            raise ValueError("Cannot divide by zero.")
        return operand1 / operand2

# '+'
class Power(Operator):
    def __init__(self):
        super().__init__(precedence=3, associativity='right')

    def operate(self, operand1, operand2):
        return operand1 ** operand2

# '+'
class Modulus(Operator):
    def __init__(self):
        super().__init__(precedence=4, associativity='left')

    def operate(self, operand1, operand2):
        return operand1 % operand2

# '+'
class CustomOpAt(Operator):
    def __init__(self):
        super().__init__(precedence=5, associativity='left')

    def operate(self, operand1, operand2):
        pass

# '+'
class CustomOpDollar(Operator):
    def __init__(self):
        super().__init__(precedence=5, associativity='left')

    def operate(self, operand1, operand2):
        pass

