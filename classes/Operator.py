from classes.Member import Member
from classes.Role import Role
class Operator(Member):
    def __init__(self, first_name, last_name, gender, age ,Role:Role, exp = 0):
        super().__init__(first_name, last_name, gender, age)
        self.__role = Role
        self.__exp = exp

    @property
    def _role(self)->Role:
        return self.__role

    @_role.setter
    def _role(self, value):
        self.__role = value

    @property
    def _exp(self):
        return self.__exp

    @_exp.setter
    def _exp(self, value):
        self.__exp = value


    def act(self):
        self.__role.act()
        
    def gain_xp(self):
        self.__exp += 1
