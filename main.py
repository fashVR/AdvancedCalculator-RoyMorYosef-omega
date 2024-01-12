def main():
    # Your main program logic here
    infix_expression = input("Enter an infix expression: ")
    converter = InfixToPostfix()
    postfix_expression = converter.convert(infix_expression)
    # You can also add evaluation logic here
    print("Postfix Expression:", postfix_expression)

# Other functions if necessary

if __name__ == "__main__":
    main()