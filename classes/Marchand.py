# FILE: classes/Marchand.py
from classes.Role import Role

class Marchand(Role):
    def __init__(self):
        super().__init__(rep_ship=False, drive_ship=False)
        self._role = "Marchand"
    
    def act(self):
        print("Gère les marchandises du vaisseau\n")
