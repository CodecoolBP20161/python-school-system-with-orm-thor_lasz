from models import *


class MainMenu():
    state = "main"

    def __init__(self):
        self.main_menu = ["Applicant's menu", "Administrator's menu", "Mentor's menu"]

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
            user_input = input()

            if user_input == "x":
                return
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
        print("applicant menu")
        user_input = input()

    def administrator(self):
        print("administrator menu")
        user_input = input()

    def mentor(self):
        print("mentor menu")
        user_input = input()


def main():
    MainMenu()

if __name__ == "__main__":
    main()
