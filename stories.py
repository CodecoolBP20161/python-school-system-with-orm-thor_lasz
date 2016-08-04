from models import *
from populator import Populator, Email
from tabulate import tabulate
from datetime import datetime
import getpass

# # TODO:
# - interviewslot multiple hozzarendelés bug kijavítása
# - story1-2 bug kijavítása
# - hülyebiztosság kb minden sztorinál


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
            # for applicant in updated_applicants:
            #     Email.send_email("laszthor", "codecool", "laszthor@gmail.com",
            #                      "CodeCool application process", self.create_email_body(applicant))

        print("The following {0} applicants have been assigned an id and a school"
              "in the database.\n".format(len(updated_applicants)))
        print(tabulate(updated_applicants, headers=["First name", "Last name", "Application code", "School", "Email"]))
        print("\n")

    @staticmethod
    def create_email_body(applicant):
        message = "Dear {} {}! \nWe are glad to inform you, that your application to Codecool has been processed. " \
            "Your private application code is {}, with which you will be able to check your application status. " \
            "Your interview will be held at the Codecool school in {}.\n\nThe Codecool team" \
            "".format(applicant[0], applicant[1], applicant[2], applicant[3])
        return message


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
            if updated_applicants is None:
                print("\nPlease assign the applicants to school before assigning them an interview in their school.\n")
            else:
                for applicant in updated_applicants:
                    Email.send_email("laszthor", "codecool", "laszthor@gmail.com",
                                     "CodeCool interview details", self.create_email_body(applicant))

                print("The following {0} applicants have been assigned an interview.\n".format(len(updated_applicants)))
                print(tabulate(updated_applicants, headers=["First name", "Last name", "Unique id",
                                                            "Interview", "Mentor"]))
                print("\n")

    @staticmethod
    def create_email_body(applicant):
        message = "Dear {} {}! \nWe are glad to inform you, that you have been assigned an interview slot at " \
            "Codecool. The date of the interview is {} and it will be held by {}.\n\nThe Codecool team" \
            "".format(applicant[0], applicant[1], applicant[3], applicant[4])
        return message


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


class FifthStory():

    def __init__(self):
        print("Fifth story:")
        print("You asked questions from Codecool. Here you can check whether they are answered. ")

        current_application_code = input("Please give in your application code: ")
        applicants_questions = Question.get_questions_for_applicant(current_application_code)

        print("\nYou have the following questions:\n")
        print(tabulate(applicants_questions, headers=["Question", "Answer", "Mentor", "Status"]))
        print("\n")


class SixthStory():
    def __init__(self):
        print("Sixth Story: ")
        print("Here you can the list of all applicants.\n")

        menu_points = ["By status", "By time", "By location", "By personal data", " By school", " By mentor name"]

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


class EightStory():

    def __init__(self):
        print("Eight Story:")
        print("Here you can handle the questions of the applicants.\n")

        menu_points = ["Assign questions to mentors", "By status", "By time",
                       "By applicant", "By school", "By mentor name"]

        user_input = None
        while user_input != "x":
            print(tabulate(Question.get_questions_for_administrator(), headers=["Id", "Question", "Answer", "Date", "App id", "Mentor", "School"]))
            print("\n")
            for point in menu_points:
                print("{0}.: {1}".format(menu_points.index(point) + 1, point))
            print("\nPress 'x' to exit\n")
            user_input = input("Give in the number of your choice: ")

            if user_input == str(1):
                print("\nTo which question would you like to assign a mentor?")
                selected_question = input("Give in question id: ")
                print("\n")

                questions = Question.get_mentors_for_question(selected_question)
                if questions is not None:
                    print("You can choose from the following mentors: ")
                    print(tabulate(questions, headers=["Id", "Mentor's name"]))
                    print("\n")
                    print("To which mentor would you like to assign the selected question?")
                    selected_mentor = input("Give in mentor id: ")

                    Question.assign_mentor(selected_question, selected_mentor)

            if user_input == str(2):
                print("Filtering by school:")
                filter_by = input("Give in school: ")
                # for tweet in Tweet.select().join(User).where(User.username == 'Charlie'):
                #     print tweet.message
            if user_input == str(3):
                print("Filtering by application code:")
                filter_by = input("Give in application code: ")

            if user_input == str(4):
                print("Filtering by mentor:")
                filter_by = input("Give in mentor name: ")

            if user_input == str(5):
                print("Filtering by date:")
                filter_by = input("Give in date: ")






class NinthStory():

    def __init__(self):
        print("Ninth Story: ")
        print("Here you can check all the interviews scheduled for you.\n")

        mentors_name = input("Give in any part of the mentor's name: ")

        print("\n Showing interviews for {}: ".format(mentors_name))
        interview_data = InterviewSlot.get_interview_dates(mentors_name)
        print("\n")
        print(tabulate(interview_data, headers=["Start", "End", "Applicant's name", "Application code"]))
        print("\n")
