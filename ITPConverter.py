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
        """
        checks for correct placement of right and left unary operators.
        :param input_string: the string representing the expression
        :return: True if all unary operators are placed correctly, False if not.
        """
        cur_index = 0

        def check_right_unary(index, op_char):
            """
            Checks if a right unary operator is correctly placed in an expression.

            Parameters:
            :param: index (int): The index of the right unary operator in the expression.
            :param: op_char (str): The character representing the right unary operator.

            :returns:
                    True if the unary operator has a correctly placed corresponding operand (the operand
                    is immediately to the left of the operator, possibly separated by repeated instances of the
                    same operator) and there is no number after him. False if there is another different operator
                    separating the unary operator from its operand, or if there is no operand for the unary operator.
            """
            if index < len(input_string) - 1:
                if input_string[index + 1][0].isdigit():
                    return False
            for j in range(index - 1, -1, -1):
                if input_string[j] != op_char:
                    if input_string[j][0].isdigit() or input_string[j][0] == ')':
                        return True
                    return False
            return False

        def check_left_unary(index, op_char):
            """
            Checks if a left unary operator is correctly placed in an expression.

            Parameters:
            :param: index (int): The index of the left unary operator in the expression.
            :param: op_char (str): The character representing the left unary operator.

            :returns:
                    True if the unary operator has a correctly placed corresponding operand (the operand
                    is immediately to the right of the operator, possibly separated by repeated instances of the
                    same operator) and there is no number before him. False if there is another different operator
                    separating the unary operator from its operand, or if there is no operand for the unary operator.
            """
            if index > 0:
                if input_string[index - 1][0].isdigit():
                    return False
            for j in range(index + 1, len(input_string)):
                if input_string[j] != op_char:
                    if input_string[j][0].isdigit() or input_string[j][0] == '(':
                        return True
                    return False
            return False

        while cur_index < len(input_string):
            char = input_string[cur_index]
            if char in self.operator_factory.operators:
                optr = self.operator_factory.get_operator(char)
                if isinstance(optr, Unary):
                    if optr.associativity == "Right":
                        if not check_right_unary(cur_index, char):
                            raise ValueError(f"Incorrect placement of {char}")
                    elif optr.associativity == "Left":
                        if not check_left_unary(cur_index, char):
                            raise ValueError(f"Incorrect placement of {char}")
            cur_index += 1

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
            # return (index == 0 and no_operator_separating(index)) or char_list[index - 1] == '_' or (
            # char_list[index - 1] == '(' and no_operator_separating(index))
            return index == 0 or char_list[index - 1] == '_' or char_list[index - 1] == '('

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

        return char_list

    def to_postfix(self, infix_expression):
        def compare_precedence(op1, op2):
            op1_precedence = self.operator_factory.get_operator(op1).precedence
            op2_precedence = self.operator_factory.get_operator(op2).precedence
            return op1_precedence >= op2_precedence

        def insert_operator():
            # Find the position in the stack where the operator should be inserted
            insert_position = 0
            for i in range(len(op_stack) - 1, -1, -1):
                if op_stack[i] == '(' or self.operator_factory.get_operator(op_stack[i]).precedence < self.operator_factory.get_operator(char).precedence:
                    insert_position = i + 1
                    break

            # Insert the operator at the found position
            op_stack.insert(insert_position, char)

        op_stack = []
        postfix = []
        latest_operator_inserted = ''
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
                if op_stack:
                    optr = self.operator_factory.get_operator(char)
                    iterate_as_normal = True

                    if latest_operator_inserted == char:
                        if isinstance(optr, Unary) and optr.repeatable:
                            iterate_as_normal = False
                        else:
                            raise OperatorError("Error: non repeatable operator", optr)
                    elif isinstance(optr, Unary):
                        if isinstance(self.operator_factory.get_operator(latest_operator_inserted), Unary):
                            if self.operator_factory.get_operator(latest_operator_inserted).associativity == "Left":
                                if optr.associativity == "Left":
                                    if self.operator_factory.get_operator(latest_operator_inserted).stackable_on_others:
                                        iterate_as_normal = False
                                    else:
                                        raise OperatorError("Error: can't stack this operator on others",
                                                            self.operator_factory.get_operator(
                                                                latest_operator_inserted))
                            if self.operator_factory.get_operator(latest_operator_inserted).associativity == "Right":
                                if optr.associativity == "Right":
                                    if not optr.stackable_on_others:
                                        raise OperatorError("Error: can't stack this operator on others", optr)

                    # pushes to the postfix expression all the operators in the op_stack that their precedence is bigger
                    # than the new operator
                    if iterate_as_normal:
                        while op_stack and op_stack[-1] != '(' and compare_precedence(op_stack[-1], char):
                            postfix.append(op_stack.pop())
                insert_operator()
                latest_operator_inserted = char
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
        print(operand_stack)
        return operand_stack.pop()
