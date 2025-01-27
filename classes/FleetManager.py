import json
from classes.Fleet import Fleet
from classes.Marchand import Marchand
from classes.Mentalist import Mentalist
from classes.Operator import Operator
from classes.Pilote import Pilote
from classes.Armurier import Armurier
from classes.Spaceship import Spaceship
from classes.Technicien import Technicien
from classes.Entretien import Entretien

import os
class FleetManager:
    def __init__(self, json_path='component/save/'):
        self.__current_fleet_index = 0
        self.__metier_map = {
            "Pilote": Pilote,
            "Technicien": Technicien,
            "Armurier": Armurier,
            "Marchand": Marchand,
            "Entretien": Entretien
        }
        self.__party = []
        self.__current_ship = None
        self.__current_member = None

    @property
    def _current_ship(self):
        return self.__current_ship

    @_current_ship.setter
    def _current_ship(self, value):
        self.__current_ship = value

    @property
    def _current_member(self):
        return self.__current_member

    @_current_member.setter
    def _current_member(self, value):
        self.__current_member = value


    @property
    def _party(self):
        return self.__party

    @_party.setter
    def _party(self, value):
        self.__party = value
    

        
        
    # @property
    # def _metier_map(self):
    #     return self.__metier_map

    # @_metier_map.setter
    # def _metier_map(self, value):
    #     self.__metier_map = value

    
    def load_data(self, json_path) -> list:
        if os.path.isdir(json_path) == False:
            os.mkdir(json_path)
        dir_list = os.listdir(json_path)
        input_Choice = input("Do you want to load a save file ? (yes or no): ")
        if input_Choice == "no":
            if self.__party == []:
                print("fresh start")
                self.add_fleet()
                self.add_ship_to_fleet()
                for i in range(4):
                    self.add_member_to_ship()
        else:            
            for i in dir_list:
                print(i)
            input_load = input("name of the file you want to load: ")+".json"
            if input_load not in dir_list:
                print("File not found")
                return self.load_data(json_path)
            
            with open(json_path+input_load, 'r') as file:
                datas = json.load(file)
            party = []
            for flotte_data in datas:
                fleet = Fleet(flotte_data["_Fleet__name"])
                for vaisseau_data in flotte_data["_Fleet__spaceship"]:
                    ship = Spaceship(vaisseau_data["_Spaceship__name"], vaisseau_data["_Spaceship__Type"], [], vaisseau_data["_Spaceship__state"])
                    for member in vaisseau_data["_Spaceship__crew"]:
                        member_to_add = None                    
                        is_operator = False
                        for key in member:
                            if key == "_Operator__role":
                                is_operator = True
                                break
                        if is_operator:
                            member_to_add = Operator(member["_Member__first_name"], member["_Member__last_name"], member["_Member__gender"], member["_Member__age"], self.__metier_map.get(member["_Operator__role"]["_Role__role"])() if member["_Operator__role"] is not None else None)
                        else: 
                            member_to_add = Mentalist(member["_Member__first_name"], member["_Member__last_name"], member["_Member__gender"], member["_Member__age"], member["_Mentalist__mana"])
                        ship.append_member(member_to_add)
                    fleet.append_spaceship(ship)
                party.append(fleet)
            self._party = party
            return 
    
    def save_data(self, path = "component/save"):
        dir_list = os.listdir(path)
        input_save = input("name your save file: ")
        for i in dir_list:
            if input_save == os.path.splitext(i)[0]+'':
                print(f"are you sure you want to overwrite this file ? {os.path.splitext(i)[0]+''}")
                input_check = input("yes or no: ")
                if input_check == "no":
                    self.save_data()
                elif input_check == "yes":
                    with open(f"{path}/{input_save}.json", 'w') as file:
                        json.dump(self.__party, file, default=lambda o: o.__dict__, indent=4)
                else:
                    print("invalid input")
                    self.save_data()
            else:
                f = open(f"{path}/{input_save}.json", 'w') 
                json.dump(self.__party, f, default=lambda o: o.__dict__, indent=4)
    
    def display_fleet_names(self):
        for fleet in self.__party:
            print(fleet._name)  
    
    def change_fleet(self, fleet_name):
        for index, fleet in enumerate(self.__party):
            if fleet._name == fleet_name:
                self.__current_fleet_index = index
                return True
        return False
    
    """
    without those function you need to repeat the same code in each function to find what you need in the party so yes but no
    """
    def get_current_fleet(self)-> Fleet:
        return self.__party[self.__current_fleet_index]
    
    def get_fleet_by_name(self, retries = 3)-> Fleet:
        if retries <= 0:
            print("Maximum retry limit reached. Exiting.")
            return None
        self.display_fleet_names()
        fleet_name = input("Nom de la flotte: \n")
        for fleet in self.__party:
            if fleet._name == fleet_name:
                return fleet
        # If no fleet is found, print the message and return the current fleet
    def stat_party(self):
        self.get_current_fleet().stat()
    
    def test(self, value):
        print(value)
    
    def get_ship(self, current_fleet=None, retries=3, name =None) -> Spaceship:
    # Limit the recursion depth to avoid infinite loops
        print(name)
        if retries <= 0:
            print("Maximum retry limit reached. Exiting.")
            return None  # Return None or handle error
        
        if current_fleet is None:
            
            fleet = self.get_fleet_by_name()
            fleet.display_spaceship()
            input_ship = input("Nom du vaisseau: \n")
            for ship in fleet._spaceship:
                if ship._name == input_ship:
                    return ship
                
            print("couldn't find the wanted Spaceship")
            return self.get_ship(current_fleet=fleet, retries=retries-1)  # Retry with decremented counter
        else:
            if name:
                for i in self.get_current_fleet()._spaceship:
                    print(i._name)
                for ship in self.get_current_fleet()._spaceship:
                    if ship._name == name:
                        self.__current_ship = ship
                        return 
            self.get_current_fleet().display_spaceship()
            input_ship = input("Nom du vaisseau: \n")
            for ship in self.get_current_fleet()._spaceship:
                if ship._name == input_ship:
                    return ship
            print("couldn't find the wanted Spaceship")
            return self.get_ship(current_fleet=current_fleet, retries=retries-1)  # Retry with decremented counter

                
    def get_member(self, ship:Spaceship, retries=3, name=None):
        if retries <= 0:
            print("Maximum retry limit reached. Exiting.")
            return None
        if name:
                for i in ship._crew:
                    if i._first_name == name:
                        self.__current_member = i
                        return 
        ship.display_crew()
        input_member = input("Nom du membre: \n")
        for member in ship._crew:
            if member._first_name == input_member or member._last_name == input_member:
                return member
        print("couldn't find the wanted member")
        return self.get_member(ship, retries=retries-1)
    
    
    def show_menu(self):
        print("\n" + "=" * 40)
        print("\t\t🚀 Menu Principal 🚀")
        print("=" * 40)
        print(f"\n🌌 Flotte actuelle: {self.get_current_fleet()._name}\n")
        print("Options:")
        print("  [0]  📊 Afficher les stats de vos flottes")
        print("  [1]  ➕ Ajouter une flotte")
        print("  [2]  ❌ Supprimer une flotte")
        print("  [3]  ✏️  Renommer une flotte")
        print("  [4]  🧹 Supprimer un membre de l'équipage")
        print("  [5]  🔄 Changer de flotte")
        print("  [6]  👥 Ajouter un membre à l'équipage")
        print("  [7]  ✅ Vérifier la préparation d'un vaisseau")
        print("  [8]  👀 Afficher l'équipage d'un vaisseau")
        print("  [9]  🛠️ Ajouter un vaisseau")
        print(" [10]  🚀 Afficher les vaisseaux de la flotte")
        print(" [11]  🗑️ Supprimer un vaisseau")
        print(" [12]  ❌ Quitter")
        print(" [13]  💾 Sauvegarder")
        print(" [14]  📂 Charger une sauvegarde")
        print("=" * 40)
        return input("🔹 Faites votre choix: ")


    def input_handler(self):
        choice = self.show_menu()
        match choice:
            case "0":
                self.stat_party()
            case "1":
                self.add_fleet()
            case "2":
                fleet_name = input("Nom de la flotte: ")
                for fleet in self.__party:
                    if fleet._name == fleet_name:
                        self.__party.remove(fleet)
            case "3":
                self.rename_fleet()
            case "4":
                self.remove_member_from_ship()
            case "5":
                self.change_fleet_by_name()
            case "6":
                self.add_member_to_ship()
            case "7":
                self.check_preparation()
            case "8":
                self.get_ship(True).display_crew()
            case "9":
                self.add_ship_to_fleet()
            case "10":
                self.get_current_fleet().display_spaceship()
            case "11":
                self.remove_spaceship()
            case "12":
                input_quit = input("Voulez-vous sauvegarder avant de quitter ? (Oui, Non): ")
                if input_quit == "Oui" or input_quit == "oui" or input_quit == "O" or input_quit == "o":
                    self.save_data()
                exit(0)
            case "13":
                self.save_data()
            case "14":
                self.load_data()
            case _:
                print("Choix invalide")
    
    def remove_spaceship(self):
        ship = self.get_ship(True)
        self.get_current_fleet().remove_spaceship(ship)
    def check_preparation(self):
        ship = self.get_ship(True)
        check = ship.check_preparation()
        if check:
            print("Le vaisseau est prêt")
        else:
            print("Le vaisseau n'est pas prêt")
    
    def rename_fleet(self):
        fleet = self.get_current_fleet()
        new_name = input("Nouveau nom: ")
        if new_name == "" or len(new_name) <= 0 or len(new_name) > 20 or new_name in [fleet._name for fleet in self.__party]:
            print("Nom invalide")
            return
        fleet._name = new_name
                
    def add_fleet(self):
        fleet_name = input("Nom de la flotte: ")
        self.__party.append(Fleet(fleet_name))
        
    def add_ship_to_fleet(self):
        add_ship = input("Voulez-vous ajouter un vaisseau à une flotte existante ? (Oui, Non): ")
        if add_ship == "Non" or add_ship == "non" or add_ship == "N" or add_ship == "n":
            self.add_fleet()
            self.add_ship_to_fleet()
            self.change_fleet(self.__party[-1]._name)
        fleet = self.get_current_fleet()
        ship_name = input("Nom du vaisseau: ")
        if ship_name == "" or len(ship_name) <= 0 or len(ship_name) > 20 or ship_name in [ship._name for ship in fleet._spaceship]:
            print("Nom invalide")
            return
        ship_type = input("Type de vaisseau (Transport ou Guerre): ")
        if ship_type != "Transport" and ship_type != "Guerre":
            print("Type de vaisseau invalide")
            return
        fleet.append_spaceship(Spaceship(ship_name, ship_type))
        print(f"Vaisseau ajouté avec succès à la flotte {fleet._name}")
        
    def add_member_to_ship(self):
        ship = self.get_ship(True)
        if ship is None:
            print("Vaisseau invalide")
            return
        input_last_name = input("Nom du membre: ")
        if input_last_name == "" or len(input_last_name) <= 0 or len(input_last_name) > 20 or input_last_name in [member._last_name for member in ship._crew]:
            print("Nom invalide")
            return
        input_first_name = input("Prénom du membre: ")
        if input_first_name == "" or len(input_first_name) <= 0 or len(input_first_name) > 20 or input_first_name in [member._first_name for member in ship._crew]:
            print("Prénom invalide")
            return
        input_age = int(input("Age du membre: "))
        if input_age <= 0 or input_age > 100:
            print("Age invalide")
            return
        input_gender = input("Sexe du membre (Homme, Femme): ")
        if input_gender != "Homme" and input_gender != "Femme" and input_gender != "H" and input_gender != "F":
            print("Sexe invalide")
            return
        if input_gender == "Homme" or input_gender == "H" or input_gender == "h":
            input_gender = "Homme"
        if input_gender == "Femme " or input_gender == "F" or input_gender == "f":
            input_gender = "Femme"
        input_Type = input("Type de membre (Operator, Mentalist): ")
        if input_Type == "Operator":
            input_role = input("Role du membre (Pilote, Technicien, Armurier, Marchand, Entretien): ")
            if input_role != "Pilote" and input_role != "Technicien" and input_role != "Armurier" and input_role != "Marchand" and input_role and "Entretien":
                print("Role invalide")
                return
            else:
                role_class = self.__metier_map.get(input_role)
                
                if role_class:
                    role_instance = role_class()
            new_member = Operator(input_first_name, input_last_name, input_gender, input_age, role_instance)
        if input_Type == "Mentalist":
            new_member = Mentalist(input_first_name, input_last_name, input_gender, input_age)
        if input_Type != "Mentalist" and input_Type != "Operator":
            print("Type de membre invalide")
            return
        ship.append_member(new_member)
                        
    def remove_member_from_ship(self):
        ship = self.get_ship(True)
        ship.display_crew()
        member = self.get_member(ship)
        if member:
            ship.remove_member(member)
        else:
            print("Membre invalide")

    def change_fleet_by_name(self):
        fleet = self.get_fleet_by_name()
        if not self.change_fleet(fleet._name):
            print("Flotte inexistante")

    

    def run(self):
        self.load_data("component/save/")
        while True:
            self.input_handler()



# Instantiate FleetManager and run
if __name__ == "__main__":
    fleet_manager = FleetManager()
    fleet_manager.run()
