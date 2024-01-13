from SingletonMeta import *
from OpImplementations import *


class OperatorFactory(metaclass=SingletonMeta):

    def __init__(self):
        self.operators = {
            "+": Add,
            "-": BinaricMinus,
            "*": Multiply,
            "/": Divide,
            "^": Power,
            "_": UnaricMinus,
            "%": Modulus,
            "@": Avg,
            "$": Max,
            "&": Min,
            "~": Tilde,
            "!": Factorial,
            "__": SignMinus
        }

    def get_operator(self, operator_symbol):
        op_class = self.operators.get(operator_symbol)
        if not op_class:
            raise ValueError(f"No operator found for symbol: {operator_symbol}")
        return op_class()
