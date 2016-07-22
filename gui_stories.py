from models import *
import populator
from tabulate import tabulate
from datetime import datetime
import getpass


class FirstStory():

    def __init__(self):
        pass


    def new_applicants(self):
        updateable_applicants = (Applicant.select(
                                    Applicant.first_name,
                                    Applicant.last_name,
                                    Applicant.email,
                                    Applicant.city
                                 )
                                 .where(Applicant.application_code >> None).tuples())
        return updateable_applicants

    def create_id(self):
        updated_applicants = []
        ids = []
        for applicant in Applicant.select():
            ids.append(applicant.application_code)
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
        return updated_applicants




class SecondStory():

    def __init__(self):
        pass

    def new_applicants(self):

        no_interview = Applicant.select().where(Applicant.interview >> None)
        applicants_without_interview = (Applicant.select(
            Applicant.first_name,
            Applicant.last_name,
            Applicant.email,
            Applicant.city
        )
                                        .where(Applicant.interview >> None).tuples())

        return applicants_without_interview

    def add_interview(self):

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
        return updated_applicants



class ThirdStory():

    def __init__(self):
        print("Third Story: ")
        print("Here you can the details of your application.\n")

        ids = []
        for applicant in Applicant.select():
            ids.append(applicant.application_code)
        app_num = input("Please give me your application number: ")
        if app_num in ids:
            Applicant_objekt = Applicant.get(app_num == Applicant.application_code)
            print("\n")
            print('First name: ', Applicant_objekt.first_name)
            print('Last name: ', Applicant_objekt.last_name)
            print('Email: ', Applicant_objekt.email)
            print('City: ', Applicant_objekt.city)
            print('Application code: ', Applicant_objekt.application_code)
            print('School: ', Applicant_objekt.school)
            print('Status: ', Applicant_objekt.status)
            print("\n")
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
        print("Sixth Story: ")
        print("Here you can the list of all applicants.\n")

        menu_points = ["By status", "By time", "By location", "By personal data", " By school", " By mentor name"]
        for point in menu_points:
            print("{0}.: {1}".format(menu_points.index(point) + 1, point))
        print("\nPress 'x' to exit\n")

        user_input = int(getpass.getpass(prompt=""))

        if user_input == 1:
            filter_by = input("Give in the status: ")
            result = (Applicant.select(Applicant.first_name,
                                       Applicant.last_name,
                                       Applicant.email,
                                       Applicant.city)
                      .where(Applicant.status == filter_by).tuples())

        elif user_input == 2:
            date_input = str(input('Give in the date:  '))
            filter_by = datetime.strptime(date_input, '%Y-%m-%d')
            result = []
            for applicant in Applicant.select():
                if filter_by < applicant.interview.start:
                    result.append([applicant.first_name, applicant.last_name, applicant.email, applicant.city])

        elif user_input == 3:
            filter_by = input("Give in the location: ")
            result = Applicant.select(
                Applicant.first_name,
                Applicant.last_name,
                Applicant.email,
                Applicant.city
                ).where(Applicant.city == filter_by).tuples()

        elif user_input == 4:
            filter_by = input("Give in the email address: ")
            result = Applicant.select(
                Applicant.first_name,
                Applicant.last_name,
                Applicant.email,
                Applicant.city
                ).where(Applicant.email == filter_by).tuples()

        elif user_input == 5:
            filter_by = input("Give in the school ")
            result = Applicant.select(
                Applicant.first_name,
                Applicant.last_name,
                Applicant.email,
                Applicant.city
                ).join(City, JOIN.FULL, Applicant.city == City.city.where(City.school_city == filter_by).tuples())

        elif user_input == 6:
            filter_by = input("Give in the mentor: ")
            result = []
            for applicant in Applicant.select():
                if filter_by == applicant.interview.mentor.first_name:
                    result.append([applicant.first_name, applicant.last_name, applicant.email, applicant.city])
        print ("\n")
        print(tabulate(result, headers=["First name", "Last name", "Email", "City"]))
        print("\n\n")
