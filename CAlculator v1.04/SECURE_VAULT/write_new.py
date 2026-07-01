
import os

from state import shared_state
from SECURE_VAULT.VaultManager import backend

import getpass
from docx import Document

class WriteMoreData:
    def __init__(self):
        pass


    def write_data(self):
        print("\nEnter \"SAVE\" to save and finish inputting data.")
        lines = []
        while True:
            line = input()
            if line.lower() == "save":
                break
            else:
                lines.append(line)

        # 1. Decrypt existing vault to temp
        backend.decrypt_existing()
        
        # 2. Append data
        doc = Document(backend.temp_file)
        for line in lines:
            doc.add_paragraph(line)
        doc.save(backend.temp_file)
        
        # 3. Re-encrypt back to vault and clean up
        import pyAesCrypt
        pyAesCrypt.encryptFile(backend.temp_file, backend.vault_file, backend.active_password, backend.buffer)
        os.remove(backend.temp_file)
        
        print("\nData securely saved!\n")
        shared_state.state = "vault_access"



    def password_input(self):
        while True:
                password_input = getpass.getpass("Enter the vault password: ")
                
                # Pass the key to the back-room manager to test it
                is_valid = backend.authenticate_and_decrypt(password_input)
                
                if is_valid:
                    print("Access Granted.")
                    self.write_data()
                    if os.path.exists(backend.temp_file): 
                        os.remove(backend.temp_file)
                    shared_state.state = "vault_access"

                    
                    break
                else:
                    print("Incorrect password.")
                    
                    # Kick them back to the calculator and escape the loop!
                    shared_state.state = "first"
                    break
                
write_instance = WriteMoreData()
        
