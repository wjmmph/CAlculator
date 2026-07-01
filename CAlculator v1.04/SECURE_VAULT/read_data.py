

from state import shared_state
from SECURE_VAULT.VaultManager import backend
from docx import Document
import os


class read_data:
    def __init__(self):
        pass

    def read_lines(self):
        backend.decrypt_existing()
        doc = Document(backend.temp_file)
        print("\n Stored vault data:\n")
        for para in doc.paragraphs:
            print(para.text)
        print("\nEnd of vault data.")

        os.remove(backend.temp_file)
        shared_state.state = "vault_access"
    
read_data_instance = read_data()
