# FILE: classes/Armurier.py
from classes.Role import Role

class Armurier(Role):
    def __init__(self):
        super().__init__(rep_ship=False, drive_ship=False)
    
    def act(self):
        print("Gère les armes du vaisseau\n")
