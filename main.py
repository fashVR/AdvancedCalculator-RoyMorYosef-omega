
def calc(expression):
    postfixed = postfix(expression)
    calced = calculate(postfixed)
    return calced


def receive_input():
    while True:
        expression = input()
        try:
            result = calc(expression)
            print(result)
        except ValueError as e:
            print(e)
