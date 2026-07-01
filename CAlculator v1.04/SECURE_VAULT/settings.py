

import pyAesCrypt

from state import shared_state
from SECURE_VAULT.initialization import music_player_instance
from SECURE_VAULT.VaultManager import backend
import getpass, os
from SECURE_VAULT.write_new import write_instance

from docx import Document

class settings:
    def __init__(self):
        pass

    def music(self):
        action= input("""
1. Play music
2. Pause music\n            
Enter your choice: """)
        if action == "1":
            music_player_instance.resume_music()
        elif action == "2":
            music_player_instance.pause_music()
        shared_state.state = "vault_access"
    
    def export(self):
        password_input = getpass.getpass("Re-enter password: ")
        authentication=backend.authenticate_and_decrypt(password_input)

        if authentication:
            backend.decrypt_existing()
            print("DELETE FILE AFTER EXPORTING")
            pyAesCrypt.encryptFile(backend.temp_file, backend.vault_file, backend.active_password, backend.buffer)
            shared_state.state = "first"
        else:
            print("Incorrect password.")
            shared_state.state = "first"
        
    def delete(self):
        password_input = getpass.getpass("Re-enter password: ")
        authentication=backend.authenticate_and_decrypt(password_input)

        if authentication:
            os.remove(backend.vault_file)
            print("Vault deleted.")
            shared_state.state = "first"
        else:
            print("Incorrect password.")
            shared_state.state = "first"

    def home(self):
        shared_state.state = "first"
        
    
settings_instance = settings()

        

