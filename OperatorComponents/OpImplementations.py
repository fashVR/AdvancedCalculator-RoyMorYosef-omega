# OpImplementations.py
import math

from Calculator.CustomeExceptions import *
from OperatorComponents.SingletonMeta import *


class Operator:
    """
    Base class for defining mathematical operators.

    :param precedence: The precedence level of the operator.
    :param name: The display name of the operator.
    """

    def __init__(self, precedence, name):
        self.precedence = precedence
        self.name = name

    def operate(self, *args: float):
        """
        Abstract method to be implemented by subclasses for performing the operation.

        :param args: The operands for the operation.
        :raises NotImplementedError: If the method is not overridden in a subclass.
        """
        raise NotImplementedError("Subclasses must override the operate() method.")


class Unary(Operator):
    """
    Base class for unary operators.

    :param precedence: The precedence level of the operator.
    :param associativity: The associativity property of the operator ('LEFT' or 'RIGHT').
    :param repeatable: Indicates if the operator is repeatable. meaning it can be used consecutively (for example: --1).
    :param stackable_on_others: Indicates if the operator can be stacked on other operators
    (for example: ~-1 | '~' is stacked on '-')
    :param name: The display name of the operator.
    :raises ValueError: If the provided associativity is not valid.
    """
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

    def operate(self, operand: float):
        """
        Method to perform the unary operation.

        :param operand: The operand for the unary operation.
        :raises NotImplementedError: If not implemented in a subclass.
        """
        raise NotImplementedError("Subclasses must override the operate() method.")


class Binary(Operator):
    """
    Base class for binary operators.

    :param precedence: The precedence level of the operator.
    :param name: The display name of the operator.
    """

    def __init__(self, precedence, name):
        super().__init__(precedence, name)

    def operate(self, operand1: float, operand2: float):
        """
        Method to perform the binary operation.

        :param operand1: The first operand for the operation.
        :param operand2: The second operand for the operation.
        :raises NotImplementedError: If not implemented in a subclass.
        """
        raise NotImplementedError("Subclasses must override the operate() method.")


# '+'
class Add(Binary, metaclass=SingletonMeta):
    """
    Class representing the addition operator.

    :param precedence: The precedence level of the operator, set to 1.
    :param name: The display name of the operator, set to "Plus: (+)".
    """

    def __init__(self):
        super().__init__(precedence=1, name="Plus: (+)")

    def operate(self, operand1: float, operand2: float):
        """
        Performs addition operation on two operands.

        :param operand1: The first operand.
        :param operand2: The second operand.
        :return: The sum of the two operands.
        """
        return operand1 + operand2


# '-'


class BinaryMinus(Binary, metaclass=SingletonMeta):
    """
    Class representing the binary minus operator.

    :param precedence: The precedence level of the operator, set to 1.
    :param name: The display name of the operator, set to "Minus: (-)".
    """

    def __init__(self):
        super().__init__(precedence=1, name='Minus: (-)')

    def operate(self, operand1: float, operand2: float):
        """
        Performs subtraction operation on two operands.

        :param operand1: The first operand.
        :param operand2: The second operand.
        :return: The result of subtracting operand2 from operand1.
        """
        return operand1 - operand2


# '*'
class Multiply(Binary, metaclass=SingletonMeta):
    """
    Class representing the multiplication operator.

    :param precedence: The precedence level of the operator, set to 2.
    :param name: The display name of the operator, set to "Multiplication: (*)".
    """

    def __init__(self):
        super().__init__(precedence=2, name="Multiplication: (*)")

    def operate(self, operand1: float, operand2: float):
        """
        Performs multiplication operation on two operands.

        :param operand1: The first operand.
        :param operand2: The second operand.
        :return: The product of the two operands.
        """
        return operand1 * operand2


# '/'
class Divide(Binary, metaclass=SingletonMeta):
    """
    Class representing the division operator.

    :param precedence: The precedence level of the operator, set to 2.
    :param name: The display name of the operator, set to "Division: (/)".
    """

    def __init__(self):
        super().__init__(precedence=2, name="Division: (/)")

    def operate(self, operand1: float, operand2: float):
        """
        Performs division operation on two operands.

        :param operand1: The numerator.
        :param operand2: The denominator.
        :return: The result of dividing operand1 by operand2.
        :raises ZeroDivisionError: If the second operand (divisor) is zero.

        """
        if operand2 == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return operand1 / operand2


# '^'
class Power(Binary, metaclass=SingletonMeta):
    """
    Class representing the exponentiation operator.

    :param precedence: The precedence level of the operator, set to 3.
    :param name: The display name of the operator, set to "Power: (^)".
    """

    def __init__(self):
        super().__init__(precedence=3, name="Power: (^)")

    def operate(self, operand1: float, operand2: float):
        """
        Performs exponentiation operation on two operands.

        :param operand1: The base.
        :param operand2: The exponent.
        :return: The result of raising operand1 to the power of operand2.
        :raises ZeroDivisionError: If operand1 is 0 and operand2 is negative.
        """
        if operand1 < 0 and 1 > operand2 > -1:
            raise OperatorError(f"cannot handle imaginary numbers", self)

        if operand1 == 0 and operand2 < 0:
            raise ZeroDivisionError(f"0 cant be raised ny a negative number: ({operand2})")
        return math.pow(operand1,operand2)


# 'UNARY_MINUS'
class UnaryMinus(Unary, metaclass=SingletonMeta):
    """
        Class representing the unary minus operator.

        :param precedence: The precedence level of the operator, set to 3.5.
        :param associativity: The associativity property of the operator, set to 'Left'.
        :param repeatable: Indicates if the operator is repeatable, set to True.
        :param stackable_on_others: Indicates if the operator can be stacked on other operators, set to False.
        :param name: The display name of the operator, set to "Minus: (-)".
        """

    def __init__(self):
        super().__init__(precedence=2.5, associativity='Left', repeatable=True, stackable_on_others=False,
                         name='Minus: (-)')

    def operate(self, operand: float):
        """
        Negates the given operand.

        :param operand: The operand to make negative.
        :return: The negative value of the operand.
        """
        return -operand


# '%'
class Modulus(Binary, metaclass=SingletonMeta):
    """
    Class representing the modulus operator.

    :param precedence: The precedence level of the operator, set to 4.
    :param name: The display name of the operator, set to "Modulus: (%)".
    """

    def __init__(self):
        super().__init__(precedence=4, name="Modulus: (-)")

    def operate(self, operand1: float, operand2: float):
        """
        Performs modulus operation on two operands.

        :param operand1: The first operand.
        :param operand2: The second operand.
        :return: The modulus of operand1 by operand2.
        """
        if operand2 == 0:
            raise OperatorError(f"modulus by zero is not allowed", self)
        result = operand1 % operand2
        return result


# '@'
class Avg(Binary, metaclass=SingletonMeta):
    """
    Class representing the average operator.

    :param precedence: The precedence level of the operator, set to 5.
    :param name: The display name of the operator, set to "Average: (@)".
    """

    def __init__(self):
        super().__init__(precedence=5, name="Average: (@)")

    def operate(self, operand1: float, operand2: float):
        """
        Calculates the average of two operands.

        :param operand1: The first operand.
        :param operand2: The second operand.
        :return: The average of the two operands.
        """
        return (operand1 + operand2) / 2


# '$'
class Max(Binary, metaclass=SingletonMeta):
    """
    Class representing the maximum operator.

    :param precedence: The precedence level of the operator, set to 5.
    :param name: The display name of the operator, set to "Maximum: ($)".
    """

    def __init__(self):
        super().__init__(precedence=5, name="Maximum: ($)")

    def operate(self, operand1: float, operand2: float):
        """
        Determines the maximum of two operands.

        :param operand1: The first operand.
        :param operand2: The second operand.
        :return: The greater of the two operands.
        """
        if operand1 > operand2:
            return operand1
        else:
            return operand2


# '&'
class Min(Binary, metaclass=SingletonMeta):
    """
    Class representing the minimum operator.

    :param precedence: The precedence level of the operator, set to 5.
    :param name: The display name of the operator, set to "Minimum: (&)".
    """

    def __init__(self):
        super().__init__(precedence=5, name="Minimum: (&)")

    def operate(self, operand1: float, operand2: float):
        """
        Determines the minimum of two operands.

        :param operand1: The first operand.
        :param operand2: The second operand.
        :return: The lesser of the two operands.
        """
        if operand1 > operand2:
            return operand2
        else:
            return operand1


# '~'
class Tilde(Unary, metaclass=SingletonMeta):
    """
    Class representing the tilde operator.

    :param precedence: The precedence level of the operator, set to 6.
    :param associativity: The associativity property of the operator, set to 'Left'.
    :param repeatable: Indicates if the operator is repeatable, set to False.
    :param stackable_on_others: Indicates if the operator can be stacked on other operators, set to True.
    :param name: The display name of the operator, set to "Tilde: (~)".
    """

    def __init__(self):
        super().__init__(precedence=6, associativity='Left', repeatable=False, stackable_on_others=True,
                         name="Tilde: (~)")

    def operate(self, operand: float):
        """
        Negates the given operand.

        :param operand: The operand to negate.
        :return: The negated value of the operand.
        """
        return -operand


# '!'
class Factorial(Unary, metaclass=SingletonMeta):
    """
    Class representing the factorial operator.

    :param precedence: The precedence level of the operator, set to 6.
    :param associativity: The associativity property of the operator, set to 'Right'.
    :param repeatable: Indicates if the operator is repeatable, set to True.
    :param stackable_on_others: Indicates if the operator can be stacked on other operators, set to True.
    :param name: The display name of the operator, set to "Factorial: (!)".

    """

    def __init__(self):
        super().__init__(precedence=6, associativity='Right', repeatable=True, stackable_on_others=True,
                         name="Factorial: (!)")

    def operate(self, operand: float):
        """
        Calculates the factorial of the given operand.

        :param operand: The operand for which to calculate the factorial.
        :return: The factorial of the operand.
        :raises OperatorError: If the operand is negative or not an integer.

        """
        if operand < 0:
            raise OperatorError("Unary operator cant perform operation on negative numbers", self)

        if operand != int(operand):
            raise OperatorError("Unary operator cant perform operation on decimal numbers", self)

        result = 1
        for i in range(1, int(operand) + 1):
            result *= i
        return result


# '#'
class DigitSum(Unary, metaclass=SingletonMeta):
    """
    Class representing the digit sum operator.

    :param precedence: The precedence level of the operator, set to 6.
    :param associativity: The associativity property of the operator, set to 'Right'.
    :param repeatable: Indicates if the operator is repeatable, set to True.
    :param stackable_on_others: Indicates if the operator can be stacked on other operators, set to True.
    :param name: The display name of the operator, set to "Digits Sum: (#)".
    """

    def __init__(self):
        super().__init__(precedence=6, associativity='Right', repeatable=True, stackable_on_others=True,
                         name='Digits Sum: (#)')

    def operate(self, operand: float):
        """
        Calculates the sum of the digits of the given operand.

        :param operand: The operand whose digits are to be summed.
        :return: The sum of the digits of the operand.
        """
        try:
            if operand < 0:
                raise OperatorError("Unary operator cant perform operation on negative numbers", self)
            if 'e' in str(operand):
                raise Warning("number is represented with a scientific notation, result may not be accurate")
        except Warning as e:
            print(e)
        str_op = str(operand)
        str_op = str_op[0:str_op.index('e')]
        digits = [int(char) for char in str_op if char.isdigit()]
        return sum(digits)


# 'SIGN_MINUS'
class SignMinus(Unary, metaclass=SingletonMeta):
    """
    Class representing the sign minus operator.

    :param precedence: The precedence level of the operator, set to 8.
    :param associativity: The associativity property of the operator, set to 'Left'.
    :param repeatable: Indicates if the operator is repeatable, set to True.
    :param stackable_on_others: Indicates if the operator can be stacked on other operators, set to False.
    :param name: The display name of the operator, set to "Minus: (-)".
    """

    def __init__(self):
        super().__init__(precedence=8, associativity='Left', repeatable=True, stackable_on_others=False,
                         name='Minus: (-)')

    def operate(self, operand: float):
        """
        Negates the given operand.

        :param operand: The operand to make negative.
        :return: The negative value of the operand.
        """
        return -operand
