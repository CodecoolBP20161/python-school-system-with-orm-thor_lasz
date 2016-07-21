from models import *
import populator
from stories import *
import getpass
from collections import OrderedDict


class MainMenu():
    """ Initiates the main menu in the terminal. """
    state = "main"

    def __init__(self):
        populator.establish_connection()
        populator.populate_tables()
        self.main_menu = ["Applicant's menu", "Administrator's menu", "Mentor's menu"]
        self.administrator_menu = [
            "Story 1: Handle new applications",
            "Story 2: Assign interview slot to applicants",
            "Story 6: Application detail",
            ]
        self.applicant_menu = ["Story 3: Application details", "Story 4: Interview details"]

        print (" --- WELCOME TO CODECOOL APPLICATION SYSTEM ---")
        print("\nPlease choose from the following options:\n")

        while True:
            if self.state == "main":
                self.call_main_menu()
            elif self.state == "applicant":
                self.applicant()
            elif self.state == "administrator":
                self.administrator()
            elif self.state == "mentor":
                self.mentor()

    def call_main_menu(self):
        """ The main menu, where one can choose from applicant, administrator and mentor submenus. """
        while True:
            for point in self.main_menu:
                print("{0}.: {1}".format(self.main_menu.index(point)+1, point))
            print("\nPress 'x' to exit\n")
            user_input = getpass.getpass(prompt="")

            if user_input == "x":
                exit()
            elif user_input == "1":
                self.state = "applicant"
                return
            elif user_input == "2":
                self.state = "administrator"
                return
            elif user_input == "3":
                return
                self.state = "mentor"

    def applicant(self):
        """ The applicant view submenu. """
        for point in self.applicant_menu:
            print("{0}.: {1}".format(self.applicant_menu.index(point)+1, point))
        print("\nPress 'x' to exit\n")
        user_input = getpass.getpass(prompt="")

        if user_input == "x":
            self.state = "main"
            return

        elif user_input == "1":
            ThirdStory()

        elif user_input == "2":
            FourthStory()

    def administrator(self):
        """ The administrator view submenu. """
        for point in self.administrator_menu:
            print("{0}.: {1}".format(self.administrator_menu.index(point)+1, point))
        print("\nPress 'x' to exit\n")
        user_input = getpass.getpass(prompt="")

        if user_input == "x":
            self.state = "main"
            return
        elif user_input == "1":
            FirstStory()
        elif user_input == "2":
            SecondStory()
        elif user_input == "3":
            SixthStory()

    def mentor(self):
        """ The mento view submenu. """
        print("Sorry buddy, nothing to do here. Press any key to return to the main menu.")
        user_input = getpass.getpass(prompt="")


def main():
    MainMenu()

if __name__ == "__main__":
    main()
