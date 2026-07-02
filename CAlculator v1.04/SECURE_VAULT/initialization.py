
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
             



import os
import urllib.request
import pygame

class music_player:
    def __init__(self):
        self.started = False
        
        # 1. Set up an OS-independent relative path
        self.asset_dir = "ASSETS"
        # os.path.join ensures it uses the right slashes (\ for Windows, / for Mac/Linux)
        self.music_file = os.path.join(self.asset_dir, "Where_Winds_Meets.mp3") 
        
        # 2. The direct download link to your audio file
        self.music_url = "https://raw.githubusercontent.com/wjmmph/CAlculator/main/ASSETS/Where_Winds_Meets.mp3" 

    def play_init(self):
        # 3. Create the ASSETS folder if it doesn't exist
        if not os.path.exists(self.asset_dir):
            os.makedirs(self.asset_dir)

        # 4. Check if the file is already there; if not, download it!
        if not os.path.exists(self.music_file):
            print("Downloading background music. This only happens once...")
            try:
                urllib.request.urlretrieve(self.music_url, self.music_file)
                print("Download complete!")
            except Exception as e:
                print(f"Could not download music (check internet connection): {e}")
                return # Skip playing music if the download fails

        # 5. Initialize pygame and load the local file
        pygame.mixer.init()
        pygame.mixer.music.load(self.music_file)

    def play_music(self):
        # We need a quick check to ensure the file loaded properly before playing
        if os.path.exists(self.music_file):
            pygame.mixer.music.play(-1)
            self.started = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.started = False

    def pause_music(self):
        pygame.mixer.music.pause()
        self.started = False

    def resume_music(self):
        if self.started: # Only unpause if it was already playing
            pygame.mixer.music.unpause()



initialize_instance = Initialize()

music_player_instance = music_player()
music_player_instance.play_init()  # Initialize the music player on startup
music_player_instance.play_music()  # Start playing music on startup