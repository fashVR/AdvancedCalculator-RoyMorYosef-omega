import SingletonMeta


class OperatorFactory(metaclass=SingletonMeta):

    def __init__(self):
        self.operators = {
            "+": Add,
            "-": Subtract,
            "*": Multiply,
            "/": Divide
        }

    def get_operator(self, operator_symbol):
        op_class = self.operators.get(operator_symbol)
        if not op_class:
            raise ValueError(f"No operator found for symbol: {operator_symbol}")
        return op_class()
