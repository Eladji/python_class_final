from classes.Role import Role
class Technicien(Role):
    def __init__(self, rep_ship= True, drive_ship = False):
        super().__init__(rep_ship, drive_ship)
        self._role = "Technicien"
    def act(self):
        print("Répare le vaisseau\n")