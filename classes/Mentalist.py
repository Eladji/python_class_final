from classes.Member import Member

class Mentalist(Member):

    def __init__(self,first_name, last_name, gender, age, mana= 100, max_mana= 100):
        super().__init__(first_name, last_name, gender, age)
        self.__mana = mana
        self.__max_mana = max_mana


    @property
    def _mana(self):
        return self.__mana

    @_mana.setter
    def _mana(self, value):
        self.__mana = value

    @property
    def _max_mana(self):
        return self.__max_mana

    @_max_mana.setter
    def _max_mana(self, value):
        self.__max_mana = value

    def act(self, Operator):
        if self.__mana <= 0:
            print("ce mentaliste n'a plus de mana")
            return 
        self._mana((self._mana - 20))
        Operator.act()
        print(f"{Operator._first_name()} {Operator._last_name()} a était envoyer au travail")
    
    def load_mana(self):
        mana_gain = self._max_mana() / 2
        self._mana(mana_gain)
        print(f"{self._first_name()} {self._last_name()} a regagner {mana_gain}\n")


