
from state import shared_state

class choice:
    def __init__(self):
        self.choice = None

    def get_choice(self):
        val= input("Continue [Y/n]? ").strip().lower()
        if val == 'y':
            shared_state.state = "first"
        elif val == 'n':
            shared_state.state = "exit"
        else:
            print("Invalid input. Please enter 'Y' to continue or 'N' to exit.")
            self.get_choice()
    
choice_instance = choice()
