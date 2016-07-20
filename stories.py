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
                interview = InterviewSlot.select().where(InterviewSlot.reserved >> False).order_by(fn.Random()).limit(1)[0]
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


# from peewee import *
# from models import *
#
# db.connect()
#
#
# def get_app_info():
#     ids = []
#     for applicant in Applicant.select():
#         ids.append(Applicant.application_code)
#     app_num = input("Pls give me your app num: ")
#     if app_num in ids:
#         print(Applicant.get(app_num == Applicant.application_code)) #need to return all arguments
#
#     else:
#         print('Not a valid application code!')
#
# get_app_info()
