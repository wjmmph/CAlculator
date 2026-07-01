import os
import pyAesCrypt
from docx import Document

class VaultManager:
    def __init__(self):
        self.vault_file = "Crypted_file.aes"
        self.temp_file = "temp.docx"
        self.buffer = 64 * 1024
        
        # Memorizes the password once successfully verified so you don't have to ask again!
        self.active_password = None 

    # --- DECRYPT (Login) ---
    def authenticate_and_decrypt(self, password_attempt):
        try:
            pyAesCrypt.decryptFile(self.vault_file, self.temp_file, password_attempt, self.buffer)
            
            # Success! Memorize it and clean up the temp file
            self.active_password = password_attempt
            
                
            return True
        

        except ValueError:
            return False
        except Exception as e:
            return False

    # --- ENCRYPT (Create New) ---
    def create_and_encrypt(self, new_password, lines):
        self.active_password = new_password
        
        # Build a fresh docx document
        doc = Document()
        for line in lines:
            doc.add_paragraph(line)
        doc.save(self.temp_file)
        
        # Encrypt it and delete the evidence
        pyAesCrypt.encryptFile(self.temp_file, self.vault_file, self.active_password, self.buffer)
        os.remove(self.temp_file)


    def decrypt_existing(self):
        pyAesCrypt.decryptFile(self.vault_file, self.temp_file, self.active_password, self.buffer)
        dest = self.temp_file
        return dest
        
# Build a single instance of the manager that other files can import
backend = VaultManager()

