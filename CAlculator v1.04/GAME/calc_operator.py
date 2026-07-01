
from state import shared_state

class operator_input:
    def __init__(self):
        self.operator = None

    def get_operator(self):
        val = input("Enter operator (+, -, *, /): ").strip().lower()
        if val in ('+', '-', '*', '/'):
            self.operator = val
            shared_state.state = "second_number"
            return self.operator
        else:
            print("Invalid operator. Please enter a valid operator (+, -, *, /)")
            return self.get_operator()

operator_input_instance = operator_input()

