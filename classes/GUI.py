from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static
from textual.containers import HorizontalGroup, VerticalGroup, Container
from classes.FleetManager import FleetManager
from textual.reactive import reactive
from textual.screen import Screen
import re
# from classes.FleetManager import FleetManager
fleet_manager = FleetManager()
fleet_manager.load_data("component/save/")
ship = None
member = None
class MemberScreen(Screen):
    def compose(self):
        yield Container(
            Static(fleet_manager._current_member._first_name),
            Static(fleet_manager._current_member._last_name),
                
            id = "member"
            
        )
        if type(fleet_manager._current_member).__name__ == "Mentalist":
            yield Static(fleet_manager._current_member._mana)
        elif fleet_manager._current_member._role:
            yield Static(fleet_manager._current_member._role._role)
            yield Static(str(fleet_manager._current_member._exp))
        yield Button(label="Retour", id="retour")
        
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "retour":
            self.app.pop_screen()
        else:
            print("nut")
class Memberui(VerticalGroup):
    def compose(self):
            for j in fleet_manager._current_ship._crew:
                yield Button(label=f"{j._first_name} {j._last_name}", id=j._first_name, classes="buttons")
        
    def on_button_pressed(self, event: Button.Pressed):
        member_name = event.button.id
        print(f"Selected member: {member_name}")
        fleet_manager.get_member(ship=fleet_manager._current_ship, name=member_name)
        # if fleet_manager._current_member:
        print(f"Member found: {fleet_manager._current_member._first_name} {fleet_manager._current_member._last_name}")
        self.app.push_screen(MemberScreen())  # Pass member to MemberScreen
        # else:
        print("Member not found!")
class ShipScreen(Screen):
    def compose(self):
        yield Container(
            Static(fleet_manager._current_ship._name),
            Static(fleet_manager._current_ship._Type),
            Static(fleet_manager._current_ship._state),
            HorizontalGroup(Memberui()),
            id = "ship"
            # *[Button(label=f"{i._first_name} {i._last_name}", id=i._first_name, classes="buttons") for i in fleet_manager._current_ship._crew],
        )
        yield Button(label="Retour", id="retour")
        
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "retour":
            self.app.pop_screen()
        else:
            print("nut")
class Shipui(HorizontalGroup):
    def compose(self):
        for i in fleet_manager.get_current_fleet()._spaceship:
            yield Button(label=i._name, id=str(i._name).replace(" ", "_"), classes="buttonsscreen")
            print(i._name)
        
    def on_button_pressed(self, event: Button.Pressed):
        ship_name = event.button.id.replace("_", " ")
        print(f"Selected ship: {ship_name}")
        fleet_manager.test(ship_name)
        event.button.label = event.button.id.replace("_", " ") 
        fleet_manager.get_ship(True, name=ship_name)
        if fleet_manager._current_ship:
            print(f"Ship found: {fleet_manager._current_ship._name}")
            self.app.push_screen(ShipScreen())  # Pass ship to ShipScreen
        else:
            print("Ship not found!")


        
class FLeetScreen(Screen):
    stat = fleet_manager.get_current_fleet().stat()   
    def compose(self):
        yield Container(
              Static("Statistiques de la flotte :", classes="textstat"),
              Static(f"Nombre de membres : {self.stat[0]}", classes="textstat"),
              Static(f"Nombre d'opérateurs : {self.stat[1]}", classes="textstat"),
              Static(f"Nombre de pilotes : {self.stat[2]}", classes="textstat"),
              Static(f"Nombre de techniciens : {self.stat[3]}", classes="textstat"),
              Static(f"Nombre de mentalistes : {self.stat[4]}", classes="textstat"),
              Static(f"Expérience totale : {self.stat[5]}", classes="textstat"),
              Static(f"Expérience moyenne : {self.stat[6]}", classes="textstat"),
              id="stat",
         ) 
        yield Container(VerticalGroup(Shipui()), id="ship")
        yield Button(label="Retour", id="retour")
   
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "retour":
            self.app.pop_screen()
            
class Fleetui(VerticalGroup, Static):
    keybind = ("f", "change_fleet", "Changer de flotte")
    
    def compose(self):
        self.app.BINDINGS = [("d", "toggle_dark", "activer le mode sombre"),(self.keybind)]
        yield Container(
            Static("Choose the fleet you want to work on :", classes="text"),
            *[Button(label=i._name, id=i._name, classes="buttons") for i in fleet_manager._party],
            id="fleet"
        )
        

    def on_button_pressed(self, event: Button.Pressed):
        
        fleet_manager.change_fleet(event.button.id)
        self.app.sub_title=fleet_manager.get_current_fleet()._name
        self.app.push_screen(FLeetScreen())
        
        
class GUI(App):
    CSS_PATH = "fleetui.tcss"
    BINDINGS = [("d", "toggle_dark", "activer le mode sombre"),]
    title = reactive("Fleet Manager")
    
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield HorizontalGroup(Fleetui())
    
    def on_mount(self):
        self.ship = None
        self.member = None
        self.title = "Fleet Manager"
        self.sub_title = fleet_manager.get_current_fleet()._name
        
    
    
    
    def dark_mode(self):
        self.theme = ("thetual-dark" if self.theme == "thetual-light" else "thetual-light")

if __name__ == "__main__":
    GUI = GUI()
    GUI.run()