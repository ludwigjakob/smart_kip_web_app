def load_mode():
    try:
        with open('mode.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return 'auto'  # Standardmodus

def save_mode(mode):
    with open('mode.txt', 'w') as f:
        f.write(mode)