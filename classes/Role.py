class Role():
    
    def __init__(self, rep_ship, drive_ship):
        self.__rep_ship = rep_ship
        self.__drive_ship = drive_ship
        self.__role:str = None

    @property
    def _role(self)->str:
        return self.__role

    @_role.setter
    def _role(self, value):
        self.__role = value


    @property
    def _rep_ship(self):
        return self.__rep_ship

    @_rep_ship.setter
    def _rep_ship(self, value):
        self.__rep_ship = value

    @property
    def _drive_ship(self):
        return self.__drive_ship

    @_drive_ship.setter
    def _drive_ship(self, value):
        self.__drive_ship = value

    
    def can_rep_ship(self):
        return self.__rep_ship
    
    def can_drive_ship(self):
        return self.__drive_ship