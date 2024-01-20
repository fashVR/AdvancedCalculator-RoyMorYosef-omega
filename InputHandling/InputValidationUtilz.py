from OperatorComponents.OperatorFactory import *


class InputValidationUtilz:
    """
    A utility class containing functions for the validation of the expression list before calculating it.
    """

    @staticmethod
    def check_parentheses(input_list: list):
        """
        Checks for mismatched or empty parentheses in an expression list.

        This function iterates through each character in the expression list to ensure that all parentheses are
        correctly matched and none are empty. It raises an error if it finds mismatched or empty parentheses.

        :param input_list: A list of strings representing mathematical expression elements.
        :raises ParenthesesMismatchError: If mismatched parentheses are found, specifying the type of mismatch.
        """

        open_parentheses_count = 0

        index = 0
        dist = 0
        for char in input_list:
            if char == '(':
                dist = 0
                open_parentheses_count += 1
            elif char == ')':
                if dist == 1:
                    raise ParenthesesMismatchError("Mismatched parentheses: Empty Parenthesis", index)

                if open_parentheses_count == 0:
                    raise ParenthesesMismatchError("Mismatched parentheses: Extra closing parenthesis detected", index)
                open_parentheses_count -= 1
            index += 1
            dist += 1
        if open_parentheses_count != 0:
            raise ParenthesesMismatchError("Mismatched parentheses: missing closing parenthesis", len(input_list))

    @staticmethod
    def validate_unary_operators(input_string):
        """
        Validates the correct placement of unary operators in an expression list.

        Ensures that unary operators are correctly placed in the expression, raising an error if they are not.
        This method internally uses two helper functions: is_left_unary and is_right_unary.

        :param operator_factory:  pre-initialized OperatorFactory instance
        :param input_string: The string representing the expression to be validated.
        :raises OperatorError: If a unary operator is incorrectly placed in the expression.
        """
        operator_factory = OperatorFactory()
        operators = operator_factory.operators

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
            op = operator_factory.get_operator(op_char)
            if index < len(input_string) - 1:
                right_char = input_string[index + 1]
                if not right_char[0].isdigit():
                    if right_char in operators:
                        right_op = operator_factory.get_operator(right_char)
                        if isinstance(right_op, Binary):
                            raise OperatorError(f"Invalid placement of right unary operator at index {index}"
                                                , op)
                        elif isinstance(right_op, Unary):
                            if right_op.associativity == Unary.RIGHT:
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
                        if left_char in operators:
                            left_op = operator_factory.get_operator(left_char)
                            if isinstance(left_op, Binary):
                                return True
                            elif isinstance(left_op, Unary):
                                if left_op.associativity == Unary.LEFT:
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
            op = operator_factory.get_operator(op_char)
            # Check left of right unary
            if not checked_left:
                if index != 0:
                    left_char = input_string[index - 1]
                    if not left_char[0].isdigit():
                        if left_char in operators:
                            left_op = operator_factory.get_operator(left_char)
                            if isinstance(left_op, Binary):
                                raise OperatorError(f"Invalid placement of right unary operator at index {index}"
                                                    , op)
                            elif isinstance(left_op, Unary):
                                if left_op.associativity == Unary.LEFT:
                                    raise OperatorError(f"Invalid placement of right unary operator at index {index}"
                                                        , op)
                        elif left_char == '(':
                            raise OperatorError(f"Invalid placement of right unary operator at index {index}"
                                                , op)

            # Check right of right unary
            if index < len(input_string) - 1:
                right_char = input_string[index + 1]
                if not right_char[0].isdigit():
                    if right_char in operators:
                        right_op = operator_factory.get_operator(right_char)
                        if isinstance(right_op, Binary):
                            return True
                        elif isinstance(right_op, Unary):
                            if right_op.associativity == Unary.RIGHT:
                                return True
                    elif right_char == ')':
                        return True
                raise OperatorError(f"Invalid placement of right unary operator at index {index}"
                                    , op)
            else:
                return True

        checked_left = False
        for i, char in enumerate(input_string):
            if char in operators:
                optr = operator_factory.get_operator(char)
                if isinstance(optr, Unary):
                    if optr.associativity == Unary.LEFT:
                        is_left_unary(i, char)
                    elif optr.associativity == Unary.RIGHT:
                        is_right_unary(i, char)
                    checked_left = True
                else:
                    checked_left = False
