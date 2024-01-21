from OperatorComponents.OperatorFactory import *


class InputProcessingUtilz:
    """
    A utility class containing functions to initialize a list that represents a string containing a mathematical
    expression.
    """

    @staticmethod
    def string_to_list(input_string: str):
        """
        converts a string (representing a mathematical expression) to a list, in which operators and parenthesis are
        stored as single items and the characters in between are grouped (as a number). makes ure not to insert empty
        items into the list.

        :param input_string: the string being converted.
        :return: returns the list of strings representing the input string.
        """

        operator_factory = OperatorFactory()
        operators = operator_factory.operators
        char_list = []
        current_number = ''

        a_number_is_in_cur_number = False
        index = 0
        while index < len(input_string):
            char = input_string[index]
            if char in operators or char in ['(', ')']:
                if a_number_is_in_cur_number:
                    char_list.append(current_number)
                    current_number = ''
                    a_number_is_in_cur_number = False
                char_list.append(char)
            else:
                current_number += char
                if char not in [' ', '\t', '\r', '\f']:
                    a_number_is_in_cur_number = True
            index += 1

        if current_number.strip():
            char_list.append(current_number)

        return char_list

    @staticmethod
    def clean_list(input_list: list):
        """
        a function which iterates over the list and removes correctly placed white spaces
        :param input_list: the list it iterates over
        :raises InvalidNumberError:  if the list contains an invalid character or an illegally placed white space
        :raises ValueError:  if the list is empty
        """
        operator_factory = OperatorFactory()
        operators = operator_factory.operators

        if not input_list:
            raise ValueError("The input list is empty.")

        for i, item in enumerate(input_list):
            if item not in operators and item not in ('(', ')'):
                try:
                    input_list[i] = str(float(item))
                except ValueError:
                    raise InvalidNumberError(f"Invalid number:", item)
