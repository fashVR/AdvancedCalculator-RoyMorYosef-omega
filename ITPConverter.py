class ITPConverter:
    def __init__(self):
        self.stack = []
        self.postfix = []
        self.precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3, "%": 4, "@": 5, "$": 5, "&": 5, "~": 6, "!": 6, }

    def isOperator(self, c):
        return c in ['+', '-', '*', '/', '^']

    def precedenceLevel(self, operator):
        return self.precedence.get(operator, 0)

    def convert(self, infix):
        for char in infix:
            if char.isnumeric() or char.isalpha():
                self.postfix.append(char)
            elif char == '(':
                self.stack.append(char)
            elif char == ')':
                while self.stack and self.stack[-1] != '(':
                    self.postfix.gittappend(self.stack.pop())
                self.stack.pop()
            elif self.isOperator(char):
                while self.stack and self.precedenceLevel(self.stack[-1]) >= self.precedenceLevel(char):
                    self.postfix.append(self.stack.pop())
                self.stack.append(char)

        while self.stack:
            self.postfix.append(self.stack.pop())

        return ' '.join(self.postfix)
