from models import *
from populator import Populator
from tabulate import tabulate
from datetime import datetime
import getpass


class StoryHandler():
    pass


class FirstStory():

    def __init__(self):
        print("First story: ")
        print("Here you can automate the process of incoming applications.\n")

        app_codes = Applicant.get_application_codes()
        no_app_code = app_codes.count(None)
        print("There are {0} applicants without an assigned id or school in the database.\n".format(no_app_code))
        print("The list of these applicants: \n")

        updateable_applicants = Applicant.get_applicants_without_code()
        print(tabulate(updateable_applicants, headers=["First name", "Last name", "Email", "City"]))

        print("\nPress x to quit, press any other key to assign a school and a unique id to these applicants.\n")
        user_input = getpass.getpass(prompt="")

        if user_input == "x":
            return
        else:
            Applicant.assign_school()
            updated_applicants = Applicant.assign_application_code()

        print("The following {0} applicants have been assigned an id and a school"
              "in the database.\n".format(len(updated_applicants)))
        print(tabulate(updated_applicants, headers=["First name", "Last name", "Application code", "School"]))
        print("\n")


class SecondStory():

    def __init__(self):
        print("Second Story: ")
        print("Here you can assign interview slots to applicants.\n")

        no_interview = Applicant.get_applicants_without_interview()
        print("There are {0} applicants without interview in the database.\n".format(len(no_interview)))
        print("The list of these applicants: \n")
        print(tabulate(no_interview, headers=["First name", "Last name", "Email", "City"]))

        print("\nPress x to quit, press any other key to assign an interview slot to these applicants.\n")
        user_input = getpass.getpass(prompt="")

        if user_input == "x":
            return
        else:
            updated_applicants = Applicant.assign_interview()
            print("The following {0} applicants have been assigned an interview.\n".format(len(updated_applicants)))
            print(tabulate(updated_applicants, headers=["First name", "Last name", "Application code",
                                                        "Interview starts at"]))
            print("\n")


class ThirdStory():

    def __init__(self):
        print("Third Story: ")
        print("Here you can the details of your application.\n")
        ids = []
        for applicant in Applicant.select():
            ids.append(applicant.application_code)
        app_num = input("Please give me your application number: ")
        if app_num in ids:
            result = Applicant.select(
                Applicant.first_name,
                Applicant.last_name,
                Applicant.email,
                Applicant.city,
                Applicant.application_code,
                Applicant.school,
                Applicant.status
                ).where(Applicant.application_code == app_num).tuples()
            print("\n")
            print(tabulate(result, headers=[
                    "First name", "Last name", "Email", "City",
                    "Application code", "School", "Status"
                ]))
            print("\n")
        else:
            print('Not a valid application code!')
            print("\n")


class FourthStory():

    def __init__(self):
        print("Fourth Story: ")
        print("Here you can check the details of you interview.\n")

        application_codes = []
        for applicant in Applicant.select():
            application_codes.append(applicant.application_code)

        current_application_code = input("Please give in your application code: ")
        if current_application_code in application_codes:
            your_interview = Applicant.get(current_application_code == Applicant.application_code).interview

            print("\nYour interview starts at {0}".format(your_interview.start))
            print("\nYour interview ends at {0}".format(your_interview.end))
            print("\nYour interview will be conducted by {0} {1} at {2}\n".format(
                your_interview.mentor.first_name,
                your_interview.mentor.last_name,
                your_interview.mentor.school.city
            ))


class SixthStory():
    def __init__(self):
        print("Sixth Story: ")
        print("Here you can the list of all applicants.\n")

        menu_points = ["By status", "By time", "By location", "By personal data", " By school", " By mentor name"]
        # for point in menu_points:
        #     print("{0}.: {1}".format(menu_points.index(point) + 1, point))

        user_input = ""
        while user_input != "x":
            for point in menu_points:
                print("{0}.: {1}".format(menu_points.index(point) + 1, point))
            print("\nPress 'x' to exit\n")

            user_input = int(getpass.getpass(prompt=""))

            if user_input == 1:
                filter_by = input("Give in the status: ")
                result = (Applicant.select(Applicant.first_name,
                                           Applicant.last_name,
                                           Applicant.email,
                                           Applicant.city,
                                           Applicant.status)
                          .where(Applicant.status == filter_by).tuples())
                print ("\n")
                print(tabulate(result, headers=["First name", "Last name", "Email", "City"]))
                print("\n\n")

            elif user_input == 2:
                date_input = str(input('Give in the date:  '))
                filter_by = datetime.strptime(date_input, '%Y-%m-%d')
                result = []
                for applicant in Applicant.select():
                    if filter_by < applicant.interview.start:
                        result.append(
                            [applicant.first_name, applicant.last_name, applicant.email,
                                applicant.city, applicant.interview.start]
                        )
                print ("\n")
                print(tabulate(result, headers=["First name", "Last name", "Email", "City", "Interview starts at"]))
                print("\n\n")

            elif user_input == 3:
                filter_by = input("Give in the location: ")
                result = Applicant.select(
                    Applicant.first_name,
                    Applicant.last_name,
                    Applicant.email,
                    Applicant.city
                    ).where(Applicant.city == filter_by).tuples()

                print ("\n")
                print(tabulate(result, headers=["First name", "Last name", "Email", "City"]))
                print("\n\n")

            elif user_input == 4:
                filter_by = input("Give in the email address: ")
                result = Applicant.select(
                    Applicant.first_name,
                    Applicant.last_name,
                    Applicant.email,
                    Applicant.city
                    ).where(Applicant.email % str("%"+filter_by+"%")).tuples()
                print ("\n")
                print(tabulate(result, headers=["First name", "Last name", "Email", "City"]))
                print("\n\n")

            elif user_input == 5:
                filter_by = input("Give in the school ")
                result = Applicant.select(
                    Applicant.first_name,
                    Applicant.last_name,
                    Applicant.email,
                    Applicant.city
                    ).join(City, JOIN.FULL, Applicant.city == City.city.where(City.school_city == filter_by).tuples())

                print ("\n")
                print(tabulate(result, headers=["First name", "Last name", "Email", "City"]))
                print("\n\n")

            elif user_input == 6:
                filter_by = input("Give in the mentor: ")
                result = []
                for applicant in Applicant.select():
                    if filter_by == applicant.interview.mentor.first_name:
                        result.append([applicant.first_name, applicant.last_name, applicant.email, applicant.city])
                print ("\n")
                print(tabulate(result, headers=["First name", "Last name", "Email", "City"]))
                print("\n\n")
