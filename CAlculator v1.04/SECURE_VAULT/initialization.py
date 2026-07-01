
import os
import getpass
from state import shared_state
import pygame
# Import the backend manager we built above
from SECURE_VAULT.VaultManager import backend
from docx import Document

class Initialize:
    def __init__(self):
        pass # We don't auto-run checks here anymore. main.py will trigger them!

    def run_checks(self):
        # --- SCENARIO 1: ENCRYPTING A NEW VAULT ---
        # Inside initialization.py -> run_checks() -> New Vault Scenario

        if not os.path.exists("Crypted_file.aes"):
            print("No vault detected. Let's set one up.")
            while True:
                password = getpass.getpass("Set a password for the vault: ")
                
                if len(password) < 4:
                    print("Password must be at least 4 characters long.")
                    continue
                    
                confirm = getpass.getpass("Confirm password: ")
                
                if password == confirm:
                    # 1. Ask the user for their first piece of data RIGHT HERE!
                    print("\nVault needs initial data to encrypt.")
                    print("Enter \"SAVE\" to save and finish inputting data.")
                    lines = []
                    
                    while True:
                        line = input()
                        
                        if line.lower() == "save":
                            break
                        else:
                            lines.append(line)
                        
                    backend.create_and_encrypt(password, lines)
                    print("Vault created securely!")
                    
                    
                    # 3. Drop them straight into the beautiful menu!
                    shared_state.state = "vault_access" 
                    break
                else:
                    print("Passwords do not match. Try again.")
        # --- SCENARIO 2: DECRYPTING AN EXISTING VAULT ---
        else:
            password_attempt = getpass.getpass("Enter vault password: ")
            if backend.authenticate_and_decrypt(password_attempt):
                # Clean up the temp file immediately for security until they actually need it
                if os.path.exists(backend.temp_file):
                    os.remove(backend.temp_file)
                shared_state.state = "vault_access"
            else:
                print("Incorrect password or corrupt vault.")
                shared_state.state = "first"
             



class music_player:
    def __init__(self):
        self.started = False

    def play_init(self):
        pygame.mixer.init()
        pygame.mixer.music.load(r"C:\Users\LRP\Downloads\where_winds_meets.mp3")
        
    def play_music(self):
        pygame.mixer.music.play(-1)
        self.started = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.started = False

    def resume_music(self):
        pygame.mixer.music.unpause()
        self.started = True

    def pause_music(self):
        pygame.mixer.music.pause()
        self.started = False



initialize_instance = Initialize()

music_player_instance = music_player()
music_player_instance.play_init()  # Initialize the music player on startup
music_player_instance.play_music()  # Start playing music on startup