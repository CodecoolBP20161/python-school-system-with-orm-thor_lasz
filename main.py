from models import *
import populator
from stories import *
import getpass
from collections import OrderedDict


class MainMenu():
    state = "main"

    def __init__(self):
        populator.establish_connection()
        populator.populate_tables()
        self.main_menu = ["Applicant's menu", "Administrator's menu", "Mentor's menu"]
        self.administrator_menu = [
            "Story 1: Handle new applications",
            "Story 2: Assign interview slot to applicants",
            "Story 6: Application detail",
            "Story 7: See the list of all scheduled interviews"
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
        elif user_input == "4":
            SeventhStory()

    def mentor(self):
        print("mentor menu")
        user_input = getpass.getpass(prompt="")


def main():
    MainMenu()

if __name__ == "__main__":
    main()

# class Menu():
#
#     @staticmethod
#     def menu_loop():
#         '''Displays menu.'''
#         menu = OrderedDict([
#             ('1', Applicant.show_closest_school)
#             ('2', Applicant.display_student_status)
#         ])
#         choice = None
#         while choice != 'q':
#             print("Press 'q' to exit menu")
#             for key, value in menu.items():
#                 print("{}) {}".format(key, value.__doc__))
#             choice = input("Choice: ").lower().strip()
#
#             if choice in menu:
#                 menu[choice]()
