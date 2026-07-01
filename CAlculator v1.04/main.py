
from state import shared_state


import time, random
from GAME.first import step_one
from GAME.calc_operator import operator_input_instance
from GAME.second import second_number_instance
from GAME.result import result_instance
from GAME.choice import choice_instance
from GAME.exit import exit








while True:
    state = shared_state.state
    if state == "first":
        step_one.get_first_number()
    elif state == "operation":
        operator_input_instance.get_operator()
    elif state == "second_number":
        second_number_instance.get_second_number()
    elif state == "calculate":
        result_instance.calculate_result()
    elif state == "choice":
        choice_instance.get_choice()
    elif state == "menu":
        from SECURE_VAULT.check_and_menu import installer
        pyAesCrypt = installer.pyAesCrypt
        print("Checking resources...")
        random_number=random.uniform(0, 2)
        time.sleep(random_number)

        pygame = installer.pygame
        print("Hold on, almost done...")
        random_number=random.uniform(0, 2)
        time.sleep(random_number)

        docx = installer.Document
        print("""if the compiler is not responding, please restart the program.""")
        random_number=random.uniform(0, 2)
        time.sleep(random_number)

        shared_state.state = "initialize"

    elif state == "initialize":
        
        from SECURE_VAULT.initialization import initialize_instance, music_player_instance
        initialize_instance.run_checks()
        if music_player_instance.started:
            music_player_instance.resume_music()
        
        

    elif state == "vault_access":
        from SECURE_VAULT.option import option_instance
        option_instance.menu_new()
    elif state == "write_data":
        from SECURE_VAULT.write_new import write_instance
        write_instance.write_data()
        
    elif state == "read_data":
        from SECURE_VAULT.read_data import read_data_instance
        read_data_instance.read_lines()
    
    elif state == "settings":
        from SECURE_VAULT.settings import settings_instance
        print("Settings menu:")
        print("""
            1. Music
            2. Export vault
            3. Delete vault
            4. Home\n""")
        input_choice = input("Enter your choice: ")
        if input_choice == "1":
            settings_instance.music()
        elif input_choice == "2":
            settings_instance.export()
        elif input_choice == "3":
            settings_instance.delete()
        elif input_choice == "4":
            settings_instance.home()



    elif state == "exit":
        exit()
        music_player_instance.stop_music()
        break

