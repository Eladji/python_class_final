import classes.Spaceship as Spaceship

class Fleet():
    def __init__(self, name, spaceship=None):
        self.__name = name
        self.__spaceship = spaceship if spaceship is not None else []

    @property
    def _name(self):
        return self.__name

    @_name.setter
    def _name(self, value):
        self.__name = value

    @property
    def _spaceship(self) :
        return self.__spaceship
    
    def display_spaceship(self):
        print(f"\nLa flotte {self.__name} est composé de :")
        for Spaceship in self.__spaceship:
            print(f" - {Spaceship._name} :  {Spaceship._Type} - {Spaceship._state} - {len(Spaceship._crew)} membres")

    def append_spaceship(self, Spaceship):
        self.__spaceship.append(Spaceship)
        print(f"{Spaceship._name} a rejoint la flotte")

    def remove_spaceship(self, value):
        self.__spaceship.pop(value._name())
        print(f"{value._name} a quitté la flotte")

    def stat(self) -> list:
        # Initialize counters
        total_members = 0
        total_operators = 0
        total_pilots = 0
        total_technicians = 0
        total_mentalists = 0
        total_experience = 0

        # Calculate statistics
        for spaceship in self.__spaceship:
            for member in spaceship._crew:
                match type(member).__name__:
                    case 'Operator':
                        total_experience += member._exp
                        match type(member._role).__name__:
                            case 'Pilote':
                                total_pilots += 1
                            case 'Technicien':
                                total_technicians += 1
                    case 'Mentalist':
                        total_mentalists += 1

        total_operators = total_pilots + total_technicians
        total_members = total_operators + total_mentalists
        average_experience = total_experience / total_members if total_members > 0 else 0
        average_experience=round(average_experience,2)
        stats = [total_members, total_operators, total_pilots, total_technicians, total_mentalists, total_experience, average_experience]
        # Display stats with improved formatting
        print("\n" + "=" * 40)
        print(f"🌌 Statistiques de la Flotte: {self.__name}")
        print("=" * 40)
        print(f"👥 Nombre total de membres: {total_members}")
        print(f"  ├─ {total_operators} Opérateurs")
        print(f"  │   ├─ {total_pilots} Pilotes")
        print(f"  │   └─ {total_technicians} Techniciens")
        print(f"  └─ {total_mentalists} Mentalistes")
        print("\n📊 Expérience:")
        print(f"  ├─ {total_experience} XP total")
        print(f"  └─ {average_experience:.2f} XP moyenne par membre")
        print("=" * 40)
        return stats
