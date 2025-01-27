# FILE: classes/Entretien.py
from classes.Role import Role

class Entretien(Role):
    def __init__(self):
        super().__init__(rep_ship=True, drive_ship=False)
    
    def act(self):
        print("Entretien le vaisseau\n")
