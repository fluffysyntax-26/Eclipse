def load_skills(filepath='data/skills.txt'):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading skills file: {e}"
