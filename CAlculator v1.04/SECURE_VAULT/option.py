
from state import shared_state




class settings:
    def __init__(self):
        self.vault_file = "Crypted_file.aes"
        self.temp_file = "temp.docx"
        self.buffer = 64 * 1024

    def menu_new(self):
        print("Choose an option:")
        print("""
              1. Write more data
              2. Read data
              3. Settings\n""")
        ch=input("Enter your choice: ")
        if ch=='1':
            shared_state.state = "write_data"
        elif ch=='2':
            shared_state.state = "read_data"
        elif ch=='3':
            shared_state.state = "settings"
        
option_instance = settings()
