
from state import shared_state
from .first import step_one
from .calc_operator import operator_input_instance
from .second import second_number_instance

class result:
    def __init__(self):
        self.result = None

    def calculate_result(self):
        if shared_state.state == "calculate":
            a = step_one.a
            b = second_number_instance.b
            operator = operator_input_instance.operator

            if operator == '+':
                self.result = a + b
            elif operator == '-':
                self.result = a - b
            elif operator == '*':
                self.result = a * b
            elif operator == '/':
                if b != 0:
                    self.result = a / b
                else:
                    print("Error: Division by zero.")
                    shared_state.state = "menu"
                    return #
            print(f"Result: {self.result}")
            shared_state.state = "choice"
        
        
result_instance = result()

