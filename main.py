from models import *
from menu_system import menu


main_menu = ("Application's menu", "Administrator's menu")

print (" --- WELCOME TO CODECOOL APPLICATION SYSTEM ---")

while True:
    user_input = menu(main_menu)


    if user_input == 1:

        print ("app menu")

    if user_input == 2:

        print ("adm menu")

    print (menu(main_menu))