# Import necessary libraries and modules
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static
from textual.containers import HorizontalGroup, VerticalGroup, Container
from classes.FleetManager import FleetManager
from textual.reactive import reactive
from textual.screen import Screen
import re

# Initialize the fleet manager and load saved data
fleet_manager = FleetManager()
fleet_manager.load_data("component/save/")
ship = None
member = None

# Screen to display member details
class MemberScreen(Screen):
    def compose(self):
        # Display the member's first name, last name, and other relevant details
        yield Container(
            Static(fleet_manager._current_member._first_name),
            Static(fleet_manager._current_member._last_name),
            id="member"
        )
        # If the member is a Mentalist, display mana details
        if type(fleet_manager._current_member).__name__ == "Operator":
            yield Static(fleet_manager._current_member._role._role)
            yield Static(str(fleet_manager._current_member._exp))
        else :
            yield Static(str(fleet_manager._current_member._mana), classes="menta")
            yield Static(str("is a mentalist"), classes="menta")
        # Otherwise, display role and experience
        # Button to go back to previous screen
        yield Button(label="Retour", id="retour")
        
    # Button press handler to go back to the previous screen
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "retour":
            self.app.pop_screen()
        else:
            print("nut")

# Screen to display crew member selection and operations
class Memberui(VerticalGroup):
    def compose(self):
        # Create buttons for each crew member in the current ship
        for j in fleet_manager._current_ship._crew:
            yield Button(label=f"{j._first_name} {j._last_name}", id=j._first_name, classes="buttons")
        
    # Handle button press to view details of a selected crew member
    def on_button_pressed(self, event: Button.Pressed):
        member_name = event.button.id
        print(f"Selected member: {member_name}")
        # Get the selected member from the current ship
        fleet_manager.get_member(ship=fleet_manager._current_ship, name=member_name)
        print(f"Member found: {fleet_manager._current_member._first_name} {fleet_manager._current_member._last_name}")
        # Push member details screen
        self.app.push_screen(MemberScreen())
        print("Member not found!")

# Screen to display ship details and operations
class ShipScreen(Screen):
    def compose(self):
        # Display the current ship's name, type, state, and crew member management
        yield Container(
            Static(fleet_manager._current_ship._name),
            Static(fleet_manager._current_ship._Type),
            Static(fleet_manager._current_ship._state),
            HorizontalGroup(Memberui()),
            id="ship"
        )
        # Button to go back to the previous screen
        yield Button(label="Retour", id="retour")
        
    # Handle button press to go back to the previous screen
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "retour":
            self.app.pop_screen()
        else:
            print("nut")

# Screen to display fleet details and ship management
class Shipui(HorizontalGroup):
    def compose(self):
        # Create a button for each ship in the current fleet
        for i in fleet_manager.get_current_fleet()._spaceship:
            yield Button(label=i._name, id=str(i._name).replace(" ", "_"), classes="buttonsscreen")
            print(i._name)
        
    # Handle button press to view details of a selected ship
    def on_button_pressed(self, event: Button.Pressed):
        ship_name = event.button.id.replace("_", " ")
        print(f"Selected ship: {ship_name}")
        # Select the ship and show its details
        fleet_manager.test(ship_name)
        event.button.label = event.button.id.replace("_", " ") 
        fleet_manager.get_ship(True, name=ship_name)
        if fleet_manager._current_ship:
            print(f"Ship found: {fleet_manager._current_ship._name}")
            self.app.push_screen(ShipScreen())  # Show ShipScreen with the current ship's details
        else:
            print("Ship not found!")

# Screen to display fleet statistics and ship list
class FLeetScreen(Screen):
    # Get fleet statistics for display
    stat = fleet_manager.get_current_fleet().stat()   
    def compose(self):
        # Display the statistics of the current fleet
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
        # Display the list of ships in the current fleet
        yield Container(VerticalGroup(Shipui()), id="ship")
        # Button to go back to the previous screen
        yield Button(label="Retour", id="retour")
   
    # Handle button press to go back to the previous screen
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "retour":
            self.app.pop_screen()

# UI to display the current fleet and allow switching fleets
class Fleetui(VerticalGroup, Static):
    keybind = ("f", "change_fleet", "Changer de flotte")
    
    def compose(self):
        # Bind key 'd' to toggle dark mode and the keybind for changing fleet
        self.app.BINDINGS = [("d", "toggle_dark", "activer le mode sombre"), (self.keybind)]
        # Display buttons for each fleet
        yield Container(
            Static("Choose the fleet you want to work on :", classes="text"),
            *[Button(label=i._name, id=i._name, classes="buttons") for i in fleet_manager._party],
            id="fleet"
        )
        
    # Handle button press to change fleet
    def on_button_pressed(self, event: Button.Pressed):
        fleet_manager.change_fleet(event.button.id)
        self.app.sub_title = fleet_manager.get_current_fleet()._name
        self.app.push_screen(FLeetScreen())  # Show FleetScreen with selected fleet's details

# Main application class
class GUI(App):
    CSS_PATH = "fleetui.tcss"
    BINDINGS = [("d", "toggle_dark", "activer le mode sombre"),]
    title = reactive("Fleet Manager")
    
    def compose(self) -> ComposeResult:
        # Compose the app layout with Header, Footer, and Fleetui for fleet selection
        yield Header()
        yield Footer()
        yield HorizontalGroup(Fleetui())
    
    def on_mount(self):
        # Initialize variables and set the initial title
        self.ship = None
        self.member = None
        self.title = "Fleet Manager"
        self.sub_title = fleet_manager.get_current_fleet()._name

    # Dark mode toggle method
    def dark_mode(self):
        self.theme = ("thetual-dark" if self.theme == "thetual-light" else "thetual-light")

# Run the application
if __name__ == "__main__":
    GUI = GUI()
    GUI.run()
