from player import Player

def instanciate():
    try:
        name = input("Enter your name: ")
    except Exception as e:
        print(e)
    return name

def start_menu():
    import shutil
    columns = shutil.get_terminal_size((80, 20)).columns
    title = "--- ECLIPSE ---"
    options = ["1. Start Game", "2. Load Game", "3. Quit"]
    while True:
        print("\n" + title.center(columns))
        for opt in options:
            print(opt.center(columns))
        choice = input("Select an option: ").strip()
        if choice == '1':
            return 'start'
        elif choice == '2':
            return 'load'
        elif choice == '3':
            print("Goodbye!".center(columns))
            exit()
        else:
            print("Invalid option. Please try again.".center(columns))

def reduce_skill_costs(filepath='data/skills.txt'):
    try:
        with open(filepath, 'r') as f:
            lines = [line.rstrip() for line in f]
        for i in range(0, len(lines), 4):
            if i < len(lines):
                title = lines[i]
                if '(Cost: ' in title:
                    cost = int(title.split('(Cost: ')[1].split(' Cube Aura')[0])
                    new_cost = max(1, cost - 1)
                    lines[i] = f"{title.split(' (Cost: ')[0]} (Cost: {new_cost} Cube Aura)"
        with open(filepath, 'w') as f:
            f.write('\n'.join(lines))
    except Exception as e:
        print(f"Error reducing skill costs: {e}")

reduce_skill_costs()

def clear_acquired_skills(filepath='data/acquired_skills.txt'):
    try:
        with open(filepath, 'w') as f:
            f.write('')
    except Exception as e:
        print(f"Error clearing acquired skills: {e}")

def main():
    action = start_menu()
    if action == 'start':
        clear_acquired_skills()
    player1 = Player(instanciate())
    if action == 'load':
        player1.load_saved_game()
    player1.print_welcome_message()
    player1.load_prologue()
    player1.load_act1_intro()
    player1.ask_choice()
    player1.ask_choice2()
    player1.ask_choice3()

if __name__ == "__main__":
    main()
