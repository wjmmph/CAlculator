
from state import shared_state

class second_input:
    def __init__(self):
        self.b = None

    def get_second_number(self):
        val = input("Enter second number: ").strip().lower()
        if val == '#':
            shared_state.state = "menu"
            return None
        try:
            self.b = float(val)
            shared_state.state = "calculate"
        except ValueError:
            print("Invalid input. Please enter a valid number or '#' to return to the menu.")
            self.get_second_number()

second_number_instance = second_input()
