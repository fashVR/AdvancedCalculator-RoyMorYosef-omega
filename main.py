def main():
    infix_expression = input("Enter an infix expression: ")
    converter = InfixToPostfix()
    postfix_expression = converter.convert(infix_expression)
    print("Postfix Expression:", postfix_expression)


if __name__ == "__main__":
    main()