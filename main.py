"""SRPN calculator"""
# This is your SRPN file. Make your changes here.

# Imports
# Regex library is used for removing, replacing text
import re
import shunting as shunt


class SrpnStack:
    """Class behaves as stack for SRPN, supports functions for pushing, popping,
       and performing maths"""

    def __init__(self):
        self.stack_contents = []
        # Stack counter keeps track of the number of operands in stack
        # Prevents using an operator with only one operand.
        self.stack_counter = 0
        self.randoms_pushed = 0

    def output_result(self):
        """Output first element of stack"""
        return self.stack_contents[-1]

    def push_stack(self, push_value: int):
        """Pushes to SRPN stack"""
        if self.stack_counter > 22:
            print("Stack overflow.")
            return

        self.stack_counter += 1
        self.stack_contents.append(push_value)

    def operator_push_stack(self, operator_command: str):
        """Perform a maths operator on the stack"""

        if self.stack_counter < 2:
            print("Stack underflow.")
            return

        if not validate_operator(self.stack_contents, operator_command):
            return
        operand_stack = [self.pop_stack(1), self.pop_stack()]
        # Pop last two elements off stack and place into temporary stack
        # Do maths and push result
        self.push_stack(self.execute_maths(operand_stack, operator_command))

    def pop_stack(self, index=0):
        """Remove and then return the stacks first value. If given index,
        removes and returns that index."""

        self.stack_counter -= 1
        if index == 0:
            return self.stack_contents.pop(-1)
        return self.stack_contents.pop(- index - 1)

    def execute_maths(self, stack, input_operator):
        """Maps maths to inline functions, ensures input is between min, max
           limits"""
        operator_function_dispatch = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y,
            "%": lambda x, y: x % y,
            "^": lambda x, y: x ** y,
        }
        result = operator_function_dispatch[input_operator](stack[-2],
                                                            stack[-1])
        if result < 0:
            result = max(result, -2147483648)
        else:
            result = min(result, 2147483647)
        # Each operator is mapped to an inline function
        return int(result)

    def push_random(self):
        """Pushes number to stack"""

        num_list = [1804289383, 846930886, 1681692777, 1714636915, 1957747793,
                    424238335, 719885386, 1649760492, 596516649, 1189641421,
                    1025202362, 1350490027, 783368690, 1102520059, 2044897763,
                    1967513926, 1365180540, 1540383426, 304089172, 1303455736,
                    35005211, 521595368]
        self.push_stack(num_list[self.randoms_pushed])
        self.randoms_pushed += 1


def validate_operator(stack, operator):
    """Ensures that an unsupported operator is not executed"""

    if stack[-1] == 0 and operator == "/":
        print("Divide by 0.")
        return False
    if stack[-1] == -1 and operator == "^":
        print("Negative power.")
        return False
    return True


def regex_list(input):
    srpn_command = re.findall(r"-?\d+|\S", input)
    return srpn_command


def handle_srpn_command(srpn_command, srpn_stack, needs_regex=True):
    """Takes the command and executes the relevant SRPN class function"""

    if needs_regex is True:
        srpn_command = regex_list(srpn_command)

    # Regex used as it allows for inputs on both single and multiline inputs
    # Regex explanation:
    # -? - matches "-" zero or more times, matching both negative and positive
    # numbers
    # \d - finds digits
    # + - finds more than one digit character in number
    # | - is an or statement
    # \S - finds non-words whitespace characters, such as r and
    # Combination of this with findall splits the string into a list of srpn
    # operators

    for element in srpn_command:
        try:
            # Check if input is integer
            element = int(element)
            if element < 0:
                element = max(element, -2147483648)
            element = min(element, 2147483647)
            srpn_stack.push_stack(element)
        except ValueError:
            if element == "=":
                print(srpn_stack.output_result())
            elif element == "d":
                for i in srpn_stack.stack_contents:
                    print(str(i))
            elif element == "r":
                srpn_stack.push_random()
            elif element in "+*-/^%":
                srpn_stack.operator_push_stack(element)
            else:  # Catches anything that passed through validation
                print(f"Unrecognised operator or operand \"{element}\".")


def validate_input(usr_input: str) -> str:
    """Sanitises, removes comments, unnecessary characters inputs"""

    usr_input = re.sub(r"#(.*?)#|#", "", usr_input)
    # Regex command does the following:
    # '#' - finds a hashtag
    # () - groups the characters inside it
    # .* - selects all text between the hashtags
    # ? - prevents regex from selecting text between two comments
    # | - or operator
    # # - removes single hashtags

    usr_input = re.sub(r"(?!r|d)[a-z]|\s(?!\d)", "", usr_input)
    # Regex explanation:
    # (?!) - do not match characters with r or d
    # [a-z] - try to match characters
    # | - or command
    # \s removes whitespace
    return usr_input


# This is the entry point for the program.
# It is suggested that you do not edit the below,
# to ensure your code runs with the marking script
if __name__ == "__main__":
    srpn = SrpnStack()
    while True:
        try:
            input_string = input()
            is_infix = re.match(r"\d+(\+|%|\/|\*|\^|-|--)*\d+", input_string)
            if is_infix:
                infix_command = re.findall(r"\d+|\S", input_string)
                infix_command = shunt.shunting_algorithm(infix_command)
                handle_srpn_command(infix_command, srpn, False)

            else:
                validated_string = validate_input(input_string)
                handle_srpn_command(validated_string, srpn)
        except EOFError:
            exit()
