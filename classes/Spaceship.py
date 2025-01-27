from classes.Pilote import Pilote
from classes.Technicien import Technicien
class Spaceship:
    def __init__(self, name, Type, crew = [], state = "Opérationnel"):
        self.__name = name
        self.__Type = Type
        self.__crew = crew
        self.__state = state

    @property
    def _name(self):
        return self.__name

    @_name.setter
    def _name(self, value):
        self.__name = value

    @property
    def _Type(self):
        return self.__Type

    @_Type.setter
    def _Type(self, value):
        self.__Type = value

    @property
    def _crew(self) -> list:
        return self.__crew

    @property
    def _state(self):
        return self.__state

    @_state.setter
    def _state(self, value):
        self.__state = value

    def append_member(self, Member):
        if len(self.__crew) <= 10:
            self.__crew.append(Member)
            print(f"{Member._first_name} {Member._last_name} a rejoint l'équipage")
        else:
            print("impossible d'ajouter de nouveau membre a l'équipage")

    def remove_member(self, Member):
        if Member:
            self.__crew.remove(Member)
        else:
            print("le membre que vous essayer d'enlever est invalide")
        print(f"{Member._first_name} {Member._last_name} a quitté l'équipage")
    def check_preparation(self):
        check = [False, False]
        for i in self.__crew:
            if type(i).__name__ == "Operator":
                if i._role == Pilote:
                    check[0] = True
                if i._role == Technicien:
                    check[1] = True
        return check[0] and check[1] == True
    def display_crew(self):
        for i in self.__crew:
            print(f"{i._first_name} {i._last_name} { type(i._role).__name__ if  type(i).__name__ == "Operator" else "Mentaliste"}\n")