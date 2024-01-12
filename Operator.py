class Operator:
    def __init__(self, precedence, associativity):
        if type(self) is Operator:
            raise NotImplementedError("Operator is an abstract class")
        self.precedence = precedence
        self.associativity = associativity

    def operate(self, operand1, operand2):
        raise NotImplementedError("Subclasses must override this method")
