from abstract_classes import AbstractPlayer
from inventory import Inventory
from scripts import load_script, discover_scripts
from game_skills import load_skills
import os
import json
from time import sleep

SAVE_DIR = 'save files'

class Player(AbstractPlayer):
    def __init__(self, name, inventory=None, cube_aura=3, cube_keys=0, health=22):
        self.cube = cube_aura
        self.cube_keys = cube_keys
        self.inventory = Inventory(inventory)
        self.name = name
        self.health = health
        self.paused = False
        self.SCRIPT_FILES = discover_scripts()

    @staticmethod
    def print_effect(string):
        for char in string:
            print(char, end="", flush=True)
            sleep(0.01)

    def print_welcome_message(self):
        os.system('clear')
        self.print_effect(f"Hello, {self.name}!\n\n")
        sleep(2)
        self.print_effect("Welcome to Eclipse\n\n")
        sleep(2)
        self.print_effect("Take a deep breath and just follow the River\n\n")
        sleep(2)
        os.system('clear')

    def load_game_script(self, script_key, clear_after=False):
        if script_key not in self.SCRIPT_FILES:
            print(f"Error: Unknown script '{script_key}'")
            return
        for line in load_script(self.SCRIPT_FILES[script_key]):
            self.print_effect(line)
            print()
            # Removed input() for 'press enter to continue'
            if clear_after:
                os.system('clear')

    def load_prologue(self):
        if 'prologue' not in self.SCRIPT_FILES:
            print(f"Error: Unknown script 'prologue'")
            return
        for line in load_script(self.SCRIPT_FILES['prologue']):
            self.print_effect(line)
            print()
            sleep(2)
        print()

    def load_script1(self):
        self.load_game_script('script_1')

    def load_script2(self):
        self.load_game_script('script_2')

    def load_act1_intro(self):
        self.load_game_script('act1_intro')

    def load_script1_1(self):
        self.load_game_script('script_1_1')
    
    def load_script1_2(self):
        self.load_game_script('script1_2')

    def save_game(self):
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
        game_state = {
            'name': self.name,
            'inventory': self.inventory.to_list()
        }
        try:
            with open(os.path.join(SAVE_DIR, 'save_game.json'), 'w') as f:
                json.dump(game_state, f)
            self.print_effect("\nGame saved successfully!\n")
        except Exception as e:
            print(f"Error saving game: {e}")

    def load_saved_game(self):
        try:
            with open(os.path.join(SAVE_DIR, 'save_game.json'), 'r') as f:
                game_state = json.load(f)
                self.name = game_state['name']
                self.inventory.from_list(game_state.get('inventory', []))
            self.print_effect("\nGame loaded successfully!\n")
        except FileNotFoundError:
            self.print_effect("\nNo saved game found.\n")
        except Exception as e:
            print(f"Error loading game: {e}")

    def pause_menu(self):
        self.paused = True
        while self.paused:
            self.print_effect("\n--- PAUSED ---\n")
            self.print_effect("1. Continue\n")
            self.print_effect("2. Save game\n")
            self.print_effect("3. Load game\n")
            self.print_effect("4. View skills\n")
            self.print_effect("5. View inventory\n")
            self.print_effect("6. Quit\n")
            choice = input()
            if choice == '1':
                self.paused = False
                return  # Ensure it exits the pause menu cleanly
            elif choice == '2':
                self.save_game()
            elif choice == '3':
                self.load_saved_game()
            elif choice == '4':
                self.view_skills_file()
            elif choice == '5':
                self.view_inventory()
            elif choice == '6':
                self.print_effect("\nQuitting game. Goodbye!\n")
                exit()
            else:
                self.print_effect("Choose a valid option.\n")

    def view_skills_file(self):
        print("\n--- ACQUIRED SKILLS ---\n")
        try:
            with open('data/acquired_skills.txt', 'r') as f:
                skills = f.read().strip()
                if skills:
                    print(skills)
                else:
                    print("No skills acquired yet.")
        except FileNotFoundError:
            print("No skills acquired yet.")
        input("Press Enter to return to the pause menu...")

    def view_inventory(self):
        print("\n--- INVENTORY ---\n")
        print(self.inventory.list_items())
        input("Press Enter to return...")

    def get_input_with_pause(self, prompt_msg=""):
        while True:
            user_input = input(prompt_msg)
            if user_input.lower() == 'p':
                self.pause_menu()
                continue
            return user_input

    def ask_choice(self):
        while True:
            self.print_effect("\nWhat will you do?\n")
            self.print_effect("1. Spring to your feet and strike.\n")
            self.print_effect("2. Stay still. Pretend to be dead.\n")
            self.print_effect("(Press 'p' to pause)\n")
            try:
                choice = self.get_input_with_pause()
                if choice == '1':
                    self.load_script1()
                    self.cube += 2
                    self.print_effect("You killed Two Orcs! Cube Aura +2 points\n")
                    self.print_effect("Cube Aura can be used to gain new skills.\n")
                    self.print_effect(f"Cube Aura: {self.cube}\n\n")
                    self.print_effect("Do you want to unlock a new skill? (y/n): (Press 'p' to pause)")
                    unlock = self.get_input_with_pause().strip().lower()
                    if unlock == 'y':
                        self.unlock_skill()
                    break
                elif choice == '2':
                    self.load_script2()
                    exit()
                else:
                    self.print_effect("Choose a valid option. Your fate depends on it!\n")
            except Exception:
                self.print_effect("Please enter a valid option!\n")

    def ask_choice2(self):
        while True:
            self.print_effect("1. Follow the mysterious figure and heed the cube.\n")
            self.print_effect("2. Inspect the fallen orcs\n")
            self.print_effect("3. Escape the Battlefield\n")
            self.print_effect("(Press 'p' to pause)\n")
            try:
                choice = self.get_input_with_pause()
                if choice == '1':
                    self.load_script1_1()
                    break
                elif choice == '2':
                    self.print_effect("You find a healing potion among the fallen orcs.\n")
                    self.print_effect("You have gained a Potion of Healing!\n")
                    self.inventory.add_item('Potion of Healing')
                    self.print_effect(f"Your current health: {self.health}\n")
                    self.print_effect("Do you want to consume the healing potion? (y/n): (Press 'p' to pause)")
                    consume = self.get_input_with_pause().strip().lower()
                    if consume == 'y':
                        restored_health = min(100, self.health + 10)
                        self.health = restored_health
                        self.inventory.remove_item('Potion of Healing')
                        self.print_effect(f"You consumed the healing potion. Your health is now: {self.health}\n")
                    else:
                        self.print_effect("The healing potion has been stored in your inventory.\n")
                    # Present next options after inspecting orcs
                    while True:
                        self.print_effect("1. Follow the mysterious figure and heed the cube.\n")
                        self.print_effect("3. Escape the Battlefield\n")
                        self.print_effect("(Press 'p' to pause)\n")
                        next_choice = self.get_input_with_pause()
                        if next_choice == '1':
                            self.load_script1_1()
                            return
                        elif next_choice == '3':
                            self.print_effect("You have chosen to escape the battlefield.\n")
                            self.print_effect("You ran away from the battlefield like a coward.\n")
                            self.print_effect("The cube senses your timidity and bursts into a explosion engulfing you in flames.\n")
                            self.print_effect("What the f did you expect? coward!!\n")
                            self.print_effect("You have lost the game.\n")
                            return
                        else:
                            self.print_effect("Choose a valid option. Your fate depends on it!\n")
                    break
                elif choice == '3':
                    self.print_effect("You have chosen to escape the battlefield.\n")
                    self.print_effect("You ran away from the battlefield like a coward.\n")
                    self.print_effect("The cube senses your timidity and bursts into a explosion engulfing you in flames.\n")
                    self.print_effect("What the f did you expect? coward!!\n")
                    self.print_effect("You have lost the game.\n")
                    break
                else:
                    self.print_effect("Choose a valid option. Your fate depends on it!\n")
            except Exception:
                self.print_effect("Please enter a valid option!\n")

    def ask_choice3(self):
        self.print_effect("1. Let it pass\n")
        self.print_effect("2. Fight the creature (requires Bladebind)\n")
        self.print_effect("3. Stealth blow (requires Veilstep)\n")
        self.print_effect("(Press 'p' to pause)\n")
        try:
            choice = self.get_input_with_pause()
            if choice == '1':
                # Play ACTI/BRANCH_1/choice_2_1.txt
                for line in load_script(self.SCRIPT_FILES['choice_2_1']):
                    self.print_effect(line)
                    print()
            elif choice == '2':
                if self.has_acquired_skill('Bladebind'):
                    self.health = max(0, self.health - 5)  # Lose 5 health
                    self.cube += 2  # Gain 2 Cube Aura
                    self.print_effect("You fought fiercely with the creature, losing 5 health but gaining 2 Cube Aura.\n")
                    self.print_effect(f"Your current health: {self.health}\n")
                    self.print_effect(f"Your current Cube Aura: {self.cube}\n")
                    self.load_game_script('script_1_1')  # Bladebind Acquired
                else:
                    self.print_effect("You don't have the Bladebind skill to fight the creature.\n")
                    self.ask_choice3()
            elif choice == '3':
                if self.has_acquired_skill('Veilstep'):
                    self.cube += 1  # Gain 1 Cube Aura
                    self.print_effect("You used Veilstep to deal a stealth blow, killing the creature instantly.\n")
                    self.print_effect(f"Your current Cube Aura: {self.cube}\n")
                    for line in load_script(self.SCRIPT_FILES['choice_2_3']):
                        self.print_effect(line)
                        print()
                else:
                    self.print_effect("You don't have the Veilstep skill to perform a stealth blow.\n")
                    self.ask_choice3()
            else:
                self.print_effect("Choose a valid option. Your fate depends on it!\n")
                self.ask_choice3()
        except Exception:
            self.print_effect("Please enter a valid option!\n")
            self.ask_choice3()

    def has_acquired_skill(self, skill_name):
        try:
            with open('data/acquired_skills.txt', 'r') as f:
                acquired_skills = [line.strip() for line in f if line.strip()]
            return any(skill_name in skill for skill in acquired_skills)
        except FileNotFoundError:
            return False

    def acquire_skill(self, skill):
        try:
            with open('data/acquired_skills.txt', 'a') as af:
                af.write(skill + '\n')
            print(f"You have acquired: {skill}\n")
        except Exception as e:
            print(f"Error acquiring skill: {e}")

    def unlock_skill(self):
        try:
            with open('data/skills.txt', 'r') as f:
                skills = [line.strip() for line in f if line.strip()]

            # Group skills into titles and descriptions
            grouped_skills = []
            for i in range(0, len(skills), 3):
                title = skills[i]
                description = " ".join(skills[i + 1:i + 3])
                grouped_skills.append((title, description))

            print("\nAvailable Skills:")
            for idx, (title, description) in enumerate(grouped_skills, 1):
                print(f"{idx}. {title}")
                print(f"   {description}\n")

            print("Enter the number of the skill you want to unlock:")
            choice = self.get_input_with_pause().strip()
            if choice.isdigit() and 1 <= int(choice) <= len(grouped_skills):
                selected_skill = grouped_skills[int(choice) - 1][0]
                # Extract cost from skill description
                cost = int(selected_skill.split('(Cost: ')[1].split(' Cube Aura')[0])
                if self.cube >= cost:
                    self.cube -= cost
                    self.acquire_skill(selected_skill)
                    print(f"Skill unlocked! Remaining Cube Aura: {self.cube}\n")

                    # Increase the cost of all skills after the first unlock
                    self.increase_skill_cost()
                else:
                    print("Not enough Cube Aura to unlock this skill.\n")
            else:
                print("Invalid choice. No skill unlocked.\n")
        except Exception as e:
            print(f"Error unlocking skill: {e}")

    def increase_skill_cost(self):
        try:
            with open('data/skills.txt', 'r') as f:
                skills = [line.strip() for line in f if line.strip()]

            updated_skills = []
            for i in range(0, len(skills), 3):
                title = skills[i]
                description = skills[i + 1:i + 3]
                # Increase the cost by 1 Cube Aura
                cost = int(title.split('(Cost: ')[1].split(' Cube Aura')[0]) + 1
                updated_title = f"{title.split(' (Cost: ')[0]} (Cost: {cost} Cube Aura)"
                updated_skills.extend([updated_title] + description + [""])

            with open('data/skills.txt', 'w') as f:
                f.write("\n".join(updated_skills))
        except Exception as e:
            print(f"Error increasing skill costs: {e}")

    def printdetails(self):
        return self.name
