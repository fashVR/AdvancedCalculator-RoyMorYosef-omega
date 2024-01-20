from OperatorComponents.OperatorFactory import *


class InputProcessingUtilz:
    """
    A utility class containing functions for the validation of the expression list before calculating it.
    """

    @staticmethod
    def string_to_list(input_string: str, operator_factory: OperatorFactory):
        """
        a function which converts a string representing an expression to a list of strings. it puts operators and
        brackets as separate items and places everything in between as numbers.
        :param operator_factory: the operator factory being used.
        :param input_string: the string being converted.
        :return: returns the list of strings representing the input string.
        """
        char_list = []
        current_number = ''

        num_counter = 0
        index = -1
        while index < len(input_string) - 1:
            index += 1
            char = input_string[index]
            if char in operator_factory.operators or char in ['(', ')']:
                if current_number:
                    if num_counter > 0:
                        char_list.append(current_number)
                    current_number = ''
                    num_counter = 0
                char_list.append(char)
            else:
                current_number += char
                if char not in [' ', '\t']:
                    num_counter += 1

        if current_number.strip():
            char_list.append(current_number)

        return char_list

    @staticmethod
    def clean_list(input_list: list):
        """
        a function which iterates over the list and removes spaces which are correctly placed and raises exception for
        incorrectly placed spaces and invalid characters
        :param operator_factory:
        :param input_list: the list it iterates over
        :raises: InvalidNumberError if the list contains an invalid character or an illegal space between numbers.
        """
        operator_factory = OperatorFactory()

        if not input_list:
            raise ValueError("The input list is empty.")

        for i, item in enumerate(input_list):
            if item not in operator_factory.operators and item not in ('(', ')'):
                try:
                    input_list[i] = str(float(item))
                except ValueError:
                    raise InvalidNumberError(f"Invalid number:", item)
