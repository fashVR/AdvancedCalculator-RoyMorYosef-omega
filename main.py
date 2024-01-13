from ITPConverter import *


def receive_input():
    expression = input()


def main():
    infix_expression = input("Enter an infix expression: ")
    converter = ITPConverter()
    loc = converter.string_to_list_of_chars(infix_expression)
    new_string = converter.analyze_minuses(loc)
    to_post = converter.to_postfix(new_string)
    solvepost = converter.evaluate_postfix(to_post)
    print(solvepost)


if __name__ == "__main__":
    main()
