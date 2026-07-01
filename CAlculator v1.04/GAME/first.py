
from state import shared_state

class first_number:
    def __init__(self):
        self.a = None

    def get_first_number(self):
        val = input("Enter first number: ").strip().lower()
        if val == '#':
            shared_state.state = "menu"
            return None
        
        
        try:
            self.a = float(val)
            shared_state.state = "operation"
        except ValueError:
            print("Invalid input. Please enter a valid number or '#' to return to the menu.")
            self.get_first_number()
        
#MOST IMPORTANT: The shared_state object is used to manage the state of the calculator application. It allows different parts of the program to communicate and change the state as needed. In this case, when the user inputs '#', the state is changed to "menu", which can be used by other parts of the program to determine what action to take next.
step_one = first_number()
