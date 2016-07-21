from models import *
import populator
from tabulate import tabulate
import getpass


class FirstStory():

    def __init__(self):
        print("First story: ")
        print("Here you can automate the process of incoming applications.\n")
        ids = []
        for applicant in Applicant.select():
            ids.append(applicant.application_code)
        print("There are {0} applicants without an assigned id or school in the database.\n".format(len(ids)))
        print("The list of these applicants: \n")

        updateable_applicants = (Applicant.select(
                                    Applicant.first_name,
                                    Applicant.last_name,
                                    Applicant.email,
                                    Applicant.city
                                 )
                                 .where(Applicant.application_code >> None).tuples())

        print(tabulate(updateable_applicants, headers=["First name", "Last name", "Email", "City"]))
        print("\nPress x to quit, press any other key to assign a school and a unique id to these applicants.\n")
        user_input = getpass.getpass(prompt="")
        if user_input == "x":
            return
        else:
            updated_applicants = []
            for applicant in Applicant.select().where(Applicant.application_code >> None):
                applicant.application_code = populator.id_generator(ids)
                applicant.save()

            for applicant in Applicant.select().where(Applicant.school >> None):
                varos = City.get(City.city == applicant.city).school_city
                applicant.school = School.get(School.city == varos).id
                applicant.save()
                updated_applicants.append(
                    [applicant.first_name, applicant.last_name, applicant.application_code, applicant.school.city]
                )
        print("The following {0} applicants have been assigned an id and a school in the database.\n".format(len(ids)))
        print(tabulate(updated_applicants, headers=["First name", "Last name", "Application code", "School"]))
        print("\n")


class SecondStory():

    def __init__(self):
        print("Second Story: ")
        print("Here you can assign interview slots to applicants.\n")

        no_interview = Applicant.select().where(Applicant.interview >> None)

        applicants_without_interview = (Applicant.select(
                                            Applicant.first_name,
                                            Applicant.last_name,
                                            Applicant.email,
                                            Applicant.city
                                        )
                                        .where(Applicant.interview >> None).tuples())
        print("There are {0} applicants without interview in the database.\n".format(len(no_interview)))
        print("The list of these applicants: \n")
        print(tabulate(applicants_without_interview, headers=["First name", "Last name", "Email", "City"]))
        print("\nPress x to quit, press any other key to assign an interview slot to these applicants.\n")
        user_input = getpass.getpass(prompt="")
        if user_input == "x":
            return
        else:
            updated_applicants = []
            for applicant in Applicant.select().where(Applicant.interview >> None):
                interview = InterviewSlot.select().where(
                    InterviewSlot.reserved >> False,
                    InterviewSlot.mentor_id == applicant.school_id
                ).order_by(fn.Random()).limit(1)[0]
                interview.reserved = True
                interview.save()
                applicant.interview = interview
                applicant.save()
                updated_applicants.append(
                    [applicant.first_name, applicant.last_name, applicant.application_code, applicant.interview.start]
                )
            print("The following {0} applicants have been assigned an interview.\n".format(len(updated_applicants)))
            print(tabulate(updated_applicants, headers=["First name", "Last name", "Application code", "Interview starts at"]))
            print("\n")


class ThirdStory():

    def __init__(self):

        ids = []
        for applicant in Applicant.select():
            ids.append(applicant.application_code)
        app_num = input("Please give me your application number: ")
        if app_num in ids:

            Applicant_objekt = Applicant.get(app_num == Applicant.application_code)
            print('First name: ', Applicant_objekt.first_name)
            print('Last name: ', Applicant_objekt.last_name)
            print('Email: ', Applicant_objekt.email)
            print('City: ', Applicant_objekt.city)
            print('Application code: ', Applicant_objekt.application_code)
            print('School: ', Applicant_objekt.school)

        else:
            print('Not a valid application code!')


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
        menu_points = ["by status", "by time", "by location", "by personal data", " by school", " by mentor name"]
        for point in menu_points:
            print("{0}.: {1}".format(menu_points.index(point) + 1, point))
        print("\nPress 'x' to exit\n")
        # for applicant in Applicant.select():
        #    print(applicant.interview.mentor)
        user_input = int(getpass.getpass(prompt=""))
        if user_input == 1: #status
            filter_by = "status"
        elif user_input == 2: #time
            filter_by = input ("day? yr-mth-day")
            result = Applicant.select(Applicant.first_name,
                                            Applicant.last_name,
                                            Applicant.email,
                                            Applicant.city) \
                .join(InterviewSlot, JOIN.FULL, Applicant.interview.start == InterviewSlot.start).where(InterviewSlot.start.year == filter_by)
        elif user_input == 3: #location
            filter_by = input ("location? ")
            result = (Applicant.select(Applicant.first_name,
                                            Applicant.last_name,
                                            Applicant.email,
                                            Applicant.city)\
                                        .where(Applicant.city == filter_by).tuples())
        elif user_input == 4: #personal data
            filter_by = input("email adress? ")
            result = Applicant.select(Applicant.first_name,
                                            Applicant.last_name,
                                            Applicant.email,
                                            Applicant.city)\
                                        .where(Applicant.email == filter_by)
        elif user_input == 5: #school
            filter_by = input("School? ")
            result = (Applicant.select(Applicant.first_name,
                                            Applicant.last_name,
                                            Applicant.email,
                                            Applicant.city)\
                    .join(City, JOIN.FULL, Applicant.city == City.city).where(City.school_city == filter_by).tuples())  #.join(City, Applicant.city == City.city)
        elif user_input == 6: #mentor
            filter_by = input("mentor? ")
            result = Applicant.select(Applicant.first_name,
                                            Applicant.last_name,
                                            Applicant.email,
                                            Applicant.city)\
                                        .where(Applicant.interview.mentor.first_name == filter_by)
        print ("\n")
        print(tabulate(result, headers=["First name", "Last name", "Email", "City"]))
        print("\n\n")


class SeventhStory():

    def __init__(self):
        print("Seventh Story: ")
        print("Here you can check the list of all scheduled interviews.\n")
