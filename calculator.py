import string
from collections import deque


def calculate(expression):  # evaluates and calculates an expression
    postfix_ex = convert_infix_post(expression)
    operand_stack = deque()
    for term in postfix_ex:
        if str(term) in operators:
            ope2 = operand_stack.pop()
            ope1 = operand_stack.pop()
            operand_stack.append(operation(ope1, ope2, term))
        else:
            operand_stack.append(term)
    return operand_stack.pop()


def convert_infix_post(expression):  # converts a mathematical expression written in infix order to postfix order
    priority_dict = {"(": 0, "+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
    result_queue = deque()
    operators_stack = deque()
    i = 0
    while True:
        operand = ""
        # get the operand
        while i < len(expression) and expression[i] not in operators:
            operand += expression[i]
            i += 1
        if i < len(expression):
            # append operand to the resulting queue
            if operand == "" and expression[i] == "-":  # this help us to deal with unary "-"
                result_queue.append(0)
            elif operand and all([char in numbers for char in operand]):
                result_queue.append(int(operand))
            elif operand:
                result_queue.append(read_var(operand))
            # get the operator
            operator = expression[i]
            i += 1
            if operator == ")":
                while operators_stack[len(operators_stack) - 1] != "(":
                    result_queue.append(operators_stack.pop())
                operators_stack.pop()  # get rid of the "("
            elif operator == "(" or len(operators_stack) == 0 or priority_dict[operators_stack[len(operators_stack) - 1]] < priority_dict[operator]:
                operators_stack.append(operator)
            else:
                while len(operators_stack) != 0 and priority_dict[operators_stack[len(operators_stack) - 1]] >= priority_dict[operator]:
                    result_queue.append(operators_stack.pop())
                operators_stack.append(operator)
        else:
            break
    if operand != "":  # last operand
        if all([char in numbers for char in operand]):
            result_queue.append(int(operand))
        else:
            result_queue.append(read_var(operand))
    while len(operators_stack) != 0:  # last operators
        result_queue.append(operators_stack.pop())
    return result_queue


def operation(op1, op2, operator):  # preforms the operation "operator" between op1 and op2 and returns the result
    if operator == "+":
        return int(op1 + op2)
    elif operator == "-":
        return int(op1 - op2)
    elif operator == "*":
        return int(op1 * op2)
    elif operator == "/":
        return int(op1 / op2)
    elif operator == "^":
        return int(op1 ** op2)


def create_var(expression):  # user want to create a new variable and assign a value to it
    if expression.count("=") != 1 or expression.endswith("="):  # multiple "=" or no right side of assignment
        print("Invalid assignment")
    else:
        expression = expression.split("=")
        if all([char in alphabet for char in expression[0]]):  # it's a valid identifier ( var = express )
            try:
                variable_dict[expression[0]] = calculate(expression[1])
            except (ModuleNotFoundError, FileNotFoundError):  # error in right side of "="
                print("Invalid assignment")
        else:  # invalid variable name (error in left side of "=")
            raise ModuleNotFoundError


def read_var(expression):  # read a variable's content
    if expression in variable_dict.keys():  # it's an existing variable
        return variable_dict[expression]
    elif all([char in alphabet for char in expression]):  # it's a valid variable name but it doesn't exist
        raise FileNotFoundError
    else:  # wrong variable name
        raise ModuleNotFoundError


# write your code here: main
variable_dict = {}
alphabet = string.ascii_letters
numbers = "0123456789"
operators = "()+-*/^"
while True:  # main loop
    in_put = input().strip()
    if in_put == "/exit":  # user wanna end program
        print("Bye!")
        break
    elif in_put == "/help":  # user wanna see help
        print("The program is a smart calculator.")
    elif in_put and in_put[0] == "/":  # wrong command
        print("Unknown command")
    elif in_put:  # it's not an empty line
        in_put = "".join(in_put.split())  # remove spaces from the expression
        try:
            if "=" in in_put:  # it's a var assignment
                create_var(in_put)
            elif not any([char in operators for char in in_put]):  # reading a variable from the dict
                print(read_var(in_put))
            else:  # it's an expression
                print(calculate(in_put))
        except (ValueError, IndexError):  # in case of invalid input
            print("Invalid expression")
        except FileNotFoundError:  # variable doesn't exist
            print("Unknown variable")
        except ModuleNotFoundError:  # wrong variable name
            print("Invalid identifier")
        except ZeroDivisionError:
            print("A division on zero occurred")
