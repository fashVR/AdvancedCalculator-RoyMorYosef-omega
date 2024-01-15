class ParenthesesMismatchError(ValueError):
    def __init__(self, message, index):
        super().__init__(message)
        self.index = index


class InvalidNumberError(ValueError):
    def __init__(self, message, invalid_num):
        super().__init__(message)
        self.invalid_num = invalid_num


class OperatorError(ValueError):
    def __init__(self, message, op):
        super().__init__(message)
        self.op = op
