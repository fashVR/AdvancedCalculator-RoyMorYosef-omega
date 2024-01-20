class ParenthesesMismatchError(ValueError):
    """
    Raised when there is a mismatch in parentheses in an expression.

    :param message: Explanation of the error.
    :param index: Index in the expression list where the mismatched parenthesis is detected.
    """
    def __init__(self, message, index):
        super().__init__(message)
        self.index = index


class InvalidNumberError(ValueError):
    """
    Raised for errors in numeric values within an expression.

    :param message: Explanation of the error.
    :param invalid_num: The invalid numeric string that caused the error.
    """
    def __init__(self, message, invalid_num):
        super().__init__(message)
        self.invalid_num = invalid_num


class OperatorError(ValueError):
    """
    Raised for errors related to the usage of operators in an expression.

    :param message: Explanation of the error.
    :param op: The operator object that caused the error.
    """
    def __init__(self, message, op):
        super().__init__(message)
        self.op = op
