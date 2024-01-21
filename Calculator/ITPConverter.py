from OperatorComponents.OperatorFactory import *


class ITPConverter:
    """
    A class for converting infix expressions to postfix expressions and evaluating them.

    This class includes methods for converting a string representation of an arithmetic expression into a list,
    cleaning and validating this list, transforming it into a postfix format, and finally evaluating the postfix expression.
    """

    @staticmethod
    def analyze_minuses(char_list):
        """
        updates the minus signs in an expression list to differentiate between unary, binary and sign minus.

        This method goes through the expression list and decides whether a minus sign should be considered
        as a unary minus, a binary minus, or a sign minus based on the context in which it appears.
        it uses two helper functions: 'is_operator_first' and 'is_unary' to aid in this analysis.

        :param char_list: The list representation of an expression where minus signs are to be analyzed.
        :return: The updated list with the minus signs correctly identified as unary or binary.
        """
        operator_factory = OperatorFactory()

        def is_binary_minus(index):
            """
            determines whether a minus in a certain index is placed as a binary minus
            :param index: the index of the minus we want to analyze.
            :return: True if it is placed as binary, False if not
            """
            if char_list[index - 1][0].isdigit() or char_list[index - 1] in [')']:
                return True
            elif char_list[index - 1] in operator_factory.operators:
                left_op = operator_factory.get_operator(char_list[index - 1])
                if isinstance(left_op, Unary):
                    if left_op.associativity == Unary.RIGHT:
                        return True
            return False

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

    @staticmethod
    def to_postfix(infix_expression):
        """
        this function converts a list representing an expression in infix form to a postfix expression list.
        it uses 2 helper function: compare_precedence and insert_operator to perform this process.
        :param infix_expression:
        :return: a list representing the infix expression in postfix form
        :raises OperatorError: if it discovers an attempt to stack on an operator a non 'stackable_on_others' operator,
        or an attempt to repeat a non 'Repeatable' operator.
        """

        operator_factory = OperatorFactory()

        def compare_precedence(op1, op2):
            """
            compares the precedence of 2 operators.
            :param op1: the first operator
            :param op2: the second operator
            :return: True if the precedence of the first one is bigger or equal
            to the second, False if else.
            """
            op1_precedence = operator_factory.get_operator(op1).precedence
            op2_precedence = operator_factory.get_operator(op2).precedence
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
                if op_stack[i] == '(' or operator_factory.get_operator(
                        op_stack[i]).precedence < operator_factory.get_operator(char).precedence:
                    insert_position = i + 1
                    break

            # Insert the operator at the found position
            op_stack.insert(insert_position, char)

        op_stack = []
        postfix = []
        latest_operator_inserted = ''
        for i, char in enumerate(infix_expression):
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
                    optr = operator_factory.get_operator(char)
                    iterate_as_normal = True
                    check_stackble = True
                    if latest_operator_inserted == char:
                        if isinstance(optr, Unary):
                            if optr.repeatable:
                                iterate_as_normal = False
                                check_stackble = False
                            else:
                                raise OperatorError(f"Error: non repeatable operator at index {i}", optr)
                    if isinstance(optr, Unary) and check_stackble:
                        if isinstance(operator_factory.get_operator(latest_operator_inserted), Unary):
                            if operator_factory.get_operator(latest_operator_inserted).associativity == Unary.LEFT:
                                if optr.associativity == Unary.LEFT:
                                    if operator_factory.get_operator(latest_operator_inserted).stackable_on_others:
                                        iterate_as_normal = False
                                    else:
                                        raise OperatorError(f"Error: can't stack operator at index {i-1} on others",
                                                            operator_factory.get_operator(
                                                                latest_operator_inserted))
                            elif operator_factory.get_operator(
                                    latest_operator_inserted).associativity == Unary.RIGHT:
                                if optr.associativity == Unary.RIGHT:
                                    if not optr.stackable_on_others:
                                        raise OperatorError(f"Error: can't stack operator at index {i} on others",
                                                            optr)

                    if iterate_as_normal:
                        while op_stack and op_stack[-1] != '(' and compare_precedence(op_stack[-1], char):
                            postfix.append(op_stack.pop())
                insert_operator()
                latest_operator_inserted = char
        while op_stack:
            postfix.append(op_stack.pop())

        return postfix

    @staticmethod
    def evaluate_postfix(postfix_expression):
        """
        evaluates a list representing a postfix expression.
        :param postfix_expression: the list representing the postfix expression
        :return: the result of calculation of postfix expression.
        :raises: OperatorError: when it detects an incorrect use of an operator. usually when the stack does not
        contain the operands needed for an operator to operate.

        """

        operator_factory = OperatorFactory()
        operand_stack = []

        for char in postfix_expression:
            if char[0].isdigit():
                operand_stack.append(float(char))
            else:
                operator = operator_factory.get_operator(char)

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
