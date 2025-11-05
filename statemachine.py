# statemachine.py
from mode_database import save_mode_to_db, load_latest_mode

def save_mode(mode):
    save_mode_to_db(mode)

def load_mode():
    return load_latest_mode()
