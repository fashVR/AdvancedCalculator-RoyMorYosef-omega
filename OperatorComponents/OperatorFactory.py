from OperatorComponents.OpImplementations import *
from OperatorComponents.SingletonMeta import *


class OperatorFactory(metaclass= SingletonMeta):
    """
    A factory class for creating instances of operator classes. This class follows the Singleton design pattern
    to ensure only one instance exists throughout the program. It holds a mapping of operator symbols
    to their corresponding operator classes and provides a method to instantiate these classes.
    """
    def __init__(self):
        """
        Initializes the OperatorFactory with a predefined set of operator mappings.
        The mappings include symbols for various operators such as addition, subtraction, multiplication,
        division, power...
        """
        self.operators = {
            "+": Add,
            "-": BinaryMinus,
            "*": Multiply,
            "/": Divide,
            "^": Power,
            "UNARY_MINUS": UnaryMinus,
            "%": Modulus,
            "@": Avg,
            "$": Max,
            "&": Min,
            "~": Tilde,
            "!": Factorial,
            "#": DigitSum,
            "SIGN_MINUS": SignMinus
        }

    def get_operator(self, operator_symbol: str):
        """
        Retrieves and instantiates the operator class associated with the given symbol.

        :param operator_symbol: A string representing the operator symbol.
        :returns: An instance of the operator class corresponding to the given symbol.
        :raises ValueError: If no operator class is found for the provided symbol.
        """
        op_class = self.operators.get(operator_symbol)
        if not op_class:
            raise ValueError(f"No operator found for symbol: {operator_symbol}")
        return op_class()
