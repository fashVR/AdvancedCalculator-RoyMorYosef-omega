from ITPConverter import ITPConverter


def receive_input():
    expression = input()


def main():
    infix_expression = input("Enter an infix expression: ")
    converter = ITPConverter()
    loc = converter.string_to_list_of_chars(infix_expression)
    new_string = converter.analyze_minuses(loc)
    print(new_string)


if __name__ == "__main__":
    main()
