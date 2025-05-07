import os
from game_skills import load_skills

def discover_scripts(base_path='ACTI'):
    script_files = {}
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith('.txt'):
                relative_path = os.path.relpath(os.path.join(root, file), base_path)
                script_key = os.path.splitext(file)[0]
                script_files[script_key] = os.path.join(base_path, relative_path)
    return script_files

def load_script(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.readlines()
    except Exception as e:
        print(f"Error reading script file: {e}")
        return []
