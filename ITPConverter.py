from CustomeExceptions import *
from OperatorFactory import *


class ITPConverter:

    def __init__(self):
        self.operator_factory = OperatorFactory()
        self.precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3, "_": 3.5, "%": 4, "@": 5, "$": 5, "&": 5, "~": 6,
                           "!": 6, "__": 7}

    def string_to_list_of_chars(self, input_string):

        def find_next_non_empty(index):
            for i in range(index + 1, len(input_string)):
                if input_string[i] not in [' ', '\t']:
                    return input_string[i]

        char_list = []
        current_number = ''
        operators = self.operator_factory.operators

        index = -1
        while index < len(input_string) - 1:
            index += 1
            char = input_string[index]
            if char in [' ', '\t']:
                if index > 0:
                    if input_string[index - 1] not in self.operator_factory.operators and input_string[
                        index - 1] not in ['\t', ' ']:
                        h = find_next_non_empty(index)
                        if find_next_non_empty(index) not in self.operator_factory.operators:
                            raise ValueError("illegal space between numbers")
                continue
            if char in operators or char in ['(', ')']:
                if current_number:
                    char_list.append(current_number)
                    current_number = ''
                char_list.append(char)
            else:
                current_number += char

        if current_number:
            char_list.append(current_number)

        return char_list

    def check_for_placement_of_sign(self, input_string):

        def check_right_unary(index, op_char):
            for j in range(index - 1, -1, -1):
                if input_string[j] != op_char:
                    if input_string[j][0].isdigit() or input_string[j][0] == ')':
                        return True
                    return False
            return False

        for i, char in enumerate(input_string):
            if char in self.operator_factory.operators:
                if self.operator_factory.get_operator(char).associativity == "right":
                    if not check_right_unary(i, char):
                        raise ValueError(f"Incorrect placement of {char}")

    def unary_operators_exception(self, input_string):

        def check_right_unary(index, op_char):
            for j in range(index - 1, -1, -1):
                if input_string[j] != op_char:
                    if input_string[j][0].isdigit() or input_string[j][0] == ')':
                        return True
                    return False
            return False

        def check_left_unary(index, op_char):
            for j in range(index + 1, len(input_string)):
                if input_string[j] != op_char:
                    if input_string[j][0].isdigit() or input_string[j][0] == '(':
                        return True
                    return False
            return False

        for i, char in enumerate(input_string):
            if char in self.operator_factory.operators:
                if isinstance(self.operator_factory.get_operator(char), Unary):
                    if self.operator_factory.get_operator(char).associativity == "Right":
                        if not check_right_unary(i, char):
                            raise ValueError(f"Incorrect placement of {char}")
                    elif self.operator_factory.get_operator(char).associativity == "Left":
                        if not check_left_unary(i, char):
                            raise ValueError(f"Incorrect placement of {char}")

    def analyze_minuses(self, char_list):

        def is_operator_first(index):
            return char_list[index - 1][0].isdigit() or char_list[index - 1] in [')']

        def last_optr(index):
            for i in range(index - 1, -1, -1):
                if char_list[i] in self.operator_factory.operators:
                    op_class = self.operator_factory.get_operator(char_list[i])
                    return op_class
            return None

        def no_operator_separating(index):
            found = False
            reached = False
            while not found and not reached and index < len(char_list) - 1:
                index += 1
                if char_list[index - 1][0].isdigit():
                    reached = True
                elif char_list[index] in self.operator_factory.operators and not char_list[index] == '-':
                    found = True
            return not found

        def is_unary(index):
            return (index == 0 and no_operator_separating(index)) or char_list[index - 1] == '_' or (
                    char_list[index - 1] == '(' and no_operator_separating(index))

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
                if is_unary(current_index):
                    char_list[current_index] = '_'

                elif not is_operator_first(current_index):
                    last_operator = last_optr(current_index)
                    if isinstance(last_operator, Unary):
                        if last_optr(current_index).associativity != "Right":
                            char_list[current_index] = '__'
                    if isinstance(last_operator, Binary):
                        char_list[current_index] = '__'
            current_index += 1

        # Condense '__'
        char_list = condense_characters('__')
        # Condense '_'
        char_list = condense_characters('_')

        return char_list

    def to_postfix(self, infix_expression):
        op_stack = []
        postfix = []

        for char in infix_expression:
            if char[0].isdigit():
                postfix.append(char)
            elif char in ['(', ')']:
                if char == '(':
                    op_stack.append(char)
                else:
                    while op_stack and op_stack[-1] != '(':
                        postfix.append(op_stack.pop())
                    op_stack.pop()
            else:

                while op_stack and op_stack[-1] != '(' and self.compare_precedence(op_stack[-1], char):
                    postfix.append(op_stack.pop())
                op_stack.append(char)

        while op_stack:
            postfix.append(op_stack.pop())

        return postfix

    def evaluate_postfix(self, postfix_expression):
        operand_stack = []

        for char in postfix_expression:
            if char[0].isdigit():
                operand_stack.append(float(char))
            else:
                operator = self.operator_factory.get_operator(char)

                try:
                    if isinstance(operator, Binary):
                        operand2 = operand_stack.pop()
                        operand1 = operand_stack.pop()
                        result = operator.operate(operand1, operand2)
                    else:
                        operand = operand_stack.pop()
                        result = operator.operate(operand)

                except IndexError:
                    raise OperatorError(f"Incorrect use of operator", operator)
                operand_stack.append(result)

        return operand_stack.pop()

    def compare_precedence(self, op1, op2):
        op1_precedence = self.operator_factory.get_operator(op1).precedence
        op2_precedence = self.operator_factory.get_operator(op2).precedence
        return op1_precedence >= op2_precedence
