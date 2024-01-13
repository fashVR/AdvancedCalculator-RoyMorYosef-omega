class ITPConverter:

    def __init__(self):
        self.stack = []
        self.postfix = []
        self.precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3, "_": 3.5, "%": 4, "@": 5, "$": 5, "&": 5, "~": 6, "!": 6, "__": 7}

    def string_to_list_of_chars(self, input_string):
        char_list = []
        current_number = ''

        for char in input_string:
            if char.isdigit():
                current_number += char
            else:
                if current_number:
                    char_list.append(current_number)
                    current_number = ''

                char_list.append(char)

        if current_number:
            char_list.append(current_number)

        return char_list

    def analyze_minuses(self, char_list):

        def is_operator_first(index):
            return char_list[index - 1].isdigit()

        # Checks for unaric minuses and replaces them for '_'
        current_index = 1
        if char_list[0] == '-':
            char_list[0] = '_'
            while char_list[current_index] == '-':
                char_list[current_index] = '_'
                current_index += 1

        while current_index < len(char_list):
            if char_list[current_index] == '-':
                if not is_operator_first(current_index):
                    char_list[current_index] = '__'
            current_index += 1

        return char_list

    def postfix_evaluate(expression):
        stack = []

        for token in expression.split():
            if token.isdigit():  # Assuming the operands are integers
                stack.append(int(token))
            elif token in ['+', '-', '*', '/']:  # Binary operators
                operand2 = stack.pop(-1)
                operand1 = stack.pop(-1)
                if token == '+':
                    stack.append(operand1 + operand2)
                elif token == '-':
                    stack.append(operand1 - operand2)
                elif token == '*':
                    stack.append(operand1 * operand2)
                elif token == '/':
                    stack.append(operand1 / operand2)
            elif token in ['~', '!']:  # Example unary operators
                operand = stack.pop(-1)
                if token == '~':  # Assuming ~ is a unary negation
                    stack.append(-operand)
                elif token == '!':  # Factorial as an example unary operation
                    stack.append(math.factorial(operand))

        return stack.pop()

    # Example Usage
    expression = "5 1 2 + 4 * + 3 -"
    print(postfix_evaluate(expression))  # Example with binary operators


    def isOperator(self, c):
        return c in self.precedence

    def precedence_level(self, operator):
        return self.precedence.get(operator, 0)
