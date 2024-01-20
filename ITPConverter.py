from CustomeExceptions import *
from OperatorFactory import *


class ITPConverter:
    """
    A class for converting infix expressions to postfix expressions and evaluating them.

    This class includes methods for converting a string representation of an arithmetic expression into a list,
    cleaning and validating this list, transforming it into a postfix format, and finally evaluating the postfix expression.

    :param operator_factory: An instance of OperatorFactory used for getting operator objects.
    :param precedence: A dictionary mapping operator symbols to their precedence levels.
    """

    def __init__(self):
        """
        Initializes the ITPConverter instance with an OperatorFactory and a predefined precedence dictionary.
        """
        self.operator_factory = OperatorFactory()

    def string_to_list(self, input_string):
        """
        a function which converts a string representing an expression to a list of strings. it puts operators and
        brackets as separate items and places everything in between as numbers.
        :param input_string: the string being converted
        :return: returns the list of strings representing the input string.
        """
        char_list = []
        current_number = ''
        operators = self.operator_factory.operators

        index = -1
        while index < len(input_string) - 1:
            index += 1
            char = input_string[index]
            if char in operators or char in ['(', ')']:
                if current_number:
                    char_list.append(current_number)
                    current_number = ''
                char_list.append(char)
            else:
                current_number += char

        if current_number.strip():
            char_list.append(current_number)

        return char_list

    def clean_list(self, input_list):
        """
        a function which iterates over the list and removes spaces which are correctly placed and raises exception for
        incorrectly placed spaces and invalid characters
        :param input_list: the list it iterates over
        :raises: InvalidNumberError if the list contains an invalid character or an illegal space between numbers.
        """
        if not input_list:
            raise ValueError("The input list is empty.")

        for i, item in enumerate(input_list):
            if item not in self.operator_factory.operators and item not in ('(', ')'):
                try:
                    input_list[i] = str(float(item))
                except ValueError:
                    raise InvalidNumberError(f"Invalid number:", item)

    def validate_unary_operators(self, input_string):
        """
        Validates the correct placement of unary operators in an expression list.

        Ensures that unary operators are correctly placed in the expression, raising an error if they are not.
        This method internally uses two helper functions: is_left_unary and is_right_unary.

        :param input_string: The string representing the expression to be validated.
        :raises OperatorError: If a unary operator is incorrectly placed in the expression.
        """

        def is_left_unary(index, op_char):
            """
            Determines if the placement of a left unary operator in an expression list is valid.
            It examines the characters immediately to the left and right of the given index to ensure the operator
            is correctly positioned. The function raises an exception if the operator's placement violates standard
            mathematical or programming syntax rules.


            :param index: index of the char we want to check
            :param op_char: the char representing the operator.
            :return: True if placement is valid, raises exception if not.
            :raises: OperatorError: If the character to the right of the index is ')', a right unary operator, or a binary operator. If the character to the left of the index is a numeric value,')', or a right unary operator.
            """
            # Check right of left unary
            op = self.operator_factory.get_operator(op_char)
            if index < len(input_string) - 1:
                right_char = input_string[index + 1]
                if not right_char[0].isdigit():
                    if right_char in self.operator_factory.operators:
                        right_op = self.operator_factory.get_operator(right_char)
                        if isinstance(right_op, Binary):
                            raise OperatorError(f"Invalid placement of right unary operator at index {index}"
                                                , op)
                        elif isinstance(right_op, Unary):
                            if right_op.associativity == "Right":
                                raise OperatorError(f"Invalid placement of right unary operator at index {index}"
                                                    , op)
                    elif right_char == ')':
                        raise OperatorError(f"Invalid placement of right unary operator at index {index}"
                                            , op)

            # Check left of left unary
            if not checked_left:
                if index != 0:
                    left_char = input_string[index - 1]
                    if not left_char[0].isdigit():
                        if left_char in self.operator_factory.operators:
                            left_op = self.operator_factory.get_operator(left_char)
                            if isinstance(left_op, Binary):
                                return True
                            elif isinstance(left_op, Unary):
                                if left_op.associativity == "Left":
                                    return True
                        elif left_char == '(':
                            return True
                    raise OperatorError(f"Invalid placement of right unary operator at index {index}"
                                        , op)
                else:
                    return True
            else:
                return True

        def is_right_unary(index, op_char):
            """
            Determines if the placement of a right unary operator in an expression list is valid.
            It examines the characters immediately to the left and right of the given index to ensure the operator
            is correctly positioned. The function raises an exception if the operator's placement violates standard
            mathematical or programming syntax rules.


            :param index: index of the char we want to check
            :param op_char: the char representing the operator.
            :return: True if placement is valid, raises exception if not.
            :raises: OperatorError: If the character to the right of the index is '(', a left unary operator, or a numeric value. If the character to the left of the index is a binary operator,'(', or a left unary operator.
            """
            op = self.operator_factory.get_operator(op_char)

            # Check left of right unary
            if not checked_left:
                if index != 0:
                    left_char = input_string[index - 1]
                    if not left_char[0].isdigit():
                        if left_char in self.operator_factory.operators:
                            left_op = self.operator_factory.get_operator(left_char)
                            if isinstance(left_op, Binary):
                                raise OperatorError(f"Invalid placement of right unary operator at index {index}"
                                                    , op)
                            elif isinstance(left_op, Unary):
                                if left_op.associativity == "Left":
                                    raise OperatorError(f"Invalid placement of right unary operator at index {index}"
                                                        , op)
                        elif left_char == '(':
                            raise OperatorError(f"Invalid placement of right unary operator at index {index}"
                                                , op)

            # Check right of right unary
            if index < len(input_string) - 1:
                right_char = input_string[index + 1]
                if not right_char[0].isdigit():
                    if right_char in self.operator_factory.operators:
                        right_op = self.operator_factory.get_operator(right_char)
                        if isinstance(right_op, Binary):
                            return True
                        elif isinstance(right_op, Unary):
                            if right_op.associativity == "Right":
                                return True
                    elif right_char == ')':
                        return True
                raise OperatorError(f"Invalid placement of right unary operator at index {index}"
                                    , op)
            else:
                return True

        checked_left = False
        for i, char in enumerate(input_string):
            if char in self.operator_factory.operators:
                optr = self.operator_factory.get_operator(char)
                if isinstance(optr, Unary):
                    if optr.associativity == "Left":
                        is_left_unary(i, char)
                    elif optr.associativity == "Right":
                        is_right_unary(i, char)
                    checked_left = True
                else:
                    checked_left = False

    def analyze_minuses(self, char_list):
        """
        updates the minus signs in an expression list to differentiate between unary, binary and sign minus.

        This method goes through the expression list and decides whether a minus sign should be considered
        as a unary minus, a binary minus, or a sign minus based on the context in which it appears.
        it uses two helper functions: 'is_operator_first' and 'is_unary' to aid in this analysis.

        :param char_list: The list representation of an expression where minus signs are to be analyzed.
        :return: The updated list with the minus signs correctly identified as unary or binary.
        """

        def is_binary_minus(index):
            """
            determines whether a minus in a certain index is placed as a binary minus
            :param index: the index of the minus we want to analyze.
            :return: True if it is placed as binary, False if not
            """
            return char_list[index - 1][0].isdigit() or char_list[index - 1] in [')']

        def is_unary(index):
            """
            checks if minus operator as a certain index should be unary.
            :param index: the index of the minus being checked
            :return: returns true if it's the first character of the expression,if the character to its left is a unary minus ot if its the first character in the brackets it's in.
            """
            return index == 0 or char_list[index - 1] == 'UNARY_MINUS' or char_list[index - 1] == '('

        current_index = 0

        while current_index < len(char_list):
            if char_list[current_index] == '-':
                if is_unary(current_index):
                    char_list[current_index] = 'UNARY_MINUS'

                elif not is_binary_minus(current_index):
                    char_list[current_index] = 'SIGN_MINUS'
            current_index += 1

        return char_list

    def to_postfix(self, infix_expression):
        """
        this function converts a list representing an expression in infix form to a postfix expression list.
        it uses 2 helper function: compare_precedence and insert_operator to perform this process.
        :param infix_expression:
        :return: a list representing the infix expression in postfix form
        :raises OperatorError: if it discovers an attempt to stack on an operator a non 'stackable_on_others' operator,
        or an attempt to repeat a non 'Repeatable' operator.
        """

        def compare_precedence(op1, op2):
            """
            compares the precedence of 2 operators.
            :param op1: the first operator
            :param op2: the second operator
            :return: True if the precedence of the first one is bigger or equal
            to the second, False if else.
            """
            op1_precedence = self.operator_factory.get_operator(op1).precedence
            op2_precedence = self.operator_factory.get_operator(op2).precedence
            return op1_precedence >= op2_precedence

        def insert_operator():
            """
            inserts char from the outer scope (the compare_precedence function's for loop) to the op_stack from outer
            scope (compare_precedence's operator stack) at the correct place without removing any of the operators from
            the stack. needed when its required to stack 'repeatable' or 'stackable_on_others' unary operators without
            ruining the order of precedence and postfix validity.

            """
            insert_position = 0
            for i in range(len(op_stack) - 1, -1, -1):
                if op_stack[i] == '(' or self.operator_factory.get_operator(
                        op_stack[i]).precedence < self.operator_factory.get_operator(char).precedence:
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
                            elif self.operator_factory.get_operator(latest_operator_inserted).associativity == "Right":
                                if optr.associativity == "Right":
                                    if not optr.stackable_on_others:
                                        raise OperatorError("Error: can't stack this operator on others", optr)

                    if iterate_as_normal:
                        while op_stack and op_stack[-1] != '(' and compare_precedence(op_stack[-1], char):
                            postfix.append(op_stack.pop())
                insert_operator()
                latest_operator_inserted = char
        while op_stack:
            postfix.append(op_stack.pop())

        return postfix

    def evaluate_postfix(self, postfix_expression):
        """
        evaluates a list representing a postfix expression.
        :param postfix_expression: the list representing the postfix expression
        :return: the result of calculation of postfix expression.
        :raises: OperatorError: when it detects an incorrect use of an operator. usually when the stack does not
        contain the operands needed for an operator to operate.

        """
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
