from OperatorFactory import *


class ITPConverter:

    def __init__(self):
        self.operator_factory = OperatorFactory()
        self.precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3, "_": 3.5, "%": 4, "@": 5, "$": 5, "&": 5, "~": 6,
                           "!": 6, "__": 7}

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
            return char_list[index - 1].isdigit() or char_list[index - 1] in [')', '(']

        def last_optr(index):
            for i in range(index - 1, -1, -1):
                if char_list[i] in self.operator_factory.operators:
                    op_class = self.operator_factory.get_operator(char_list[i])
                    return op_class
            return None

        def is_unaric(index):
            return index == 0 or char_list[index - 1] == '_' or char_list[index - 1] == '('

        def condense_characters(char_to_condense):
            i = 0
            while i < len(char_list):
                if char_list[i] == char_to_condense:
                    start = i
                    while i < len(char_list) and char_list[i] == char_to_condense:
                        i += 1
                    end = i
                    count = end - start
                    if count % 2 == 0:  # Even count - remove all
                        del char_list[start:end]
                        i = start
                    else:  # Odd count - keep one
                        char_list[start:end] = [char_to_condense]
                        i = start + 1
                else:
                    i += 1
            return char_list

        current_index = 0

        while current_index < len(char_list):
            if char_list[current_index] == '-':
                if not is_operator_first(current_index):
                    if last_optr(current_index).associativity != "right":
                        char_list[current_index] = '__'

                if is_unaric(current_index):
                    char_list[current_index] = '_'
            current_index += 1

        # Condense '__'
        char_list = condense_characters('__')
        # Condense '_'
        char_list = condense_characters('_')

        return char_list

    def to_postfix(self, infix_expression):
        op_stack = []
        postfix = []

        for token in infix_expression:
            if token.isdigit():
                postfix.append(token)
            elif token in ['(', ')']:
                if token == '(':
                    op_stack.append(token)
                else:
                    while op_stack and op_stack[-1] != '(':
                        postfix.append(op_stack.pop())
                    op_stack.pop()
            else:

                while op_stack and op_stack[-1] != '(' and self.compare_precedence(op_stack[-1], token):
                    postfix.append(op_stack.pop())
                op_stack.append(token)

        while op_stack:
            postfix.append(op_stack.pop())

        return postfix

    def evaluate_postfix(self, postfix_expression):
        operand_stack = []

        for token in postfix_expression:
            if token.isdigit():
                operand_stack.append(int(token))
            else:
                operator = self.operator_factory.get_operator(token)

                if operator.associativity == 'middle':
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()
                    result = operator.operate(operand1, operand2)
                else:
                    operand = operand_stack.pop()
                    result = operator.operate(operand)

                operand_stack.append(result)

        return operand_stack.pop()

    def compare_precedence(self, op1, op2):
        op1_precedence = self.operator_factory.get_operator(op1).precedence
        op2_precedence = self.operator_factory.get_operator(op2).precedence
        return op1_precedence >= op2_precedence
