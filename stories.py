from models import *
import populator
from tabulate import tabulate


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
                                    Applicant.city,
                                 )
                                 .where(Applicant.application_code >> None).tuples())
        print(tabulate(updateable_applicants, headers=["First name", "Last name", "Email", "City"]))

        print("\nPress x to quit, press any other key to assign a school and a unique id to these applicants.\n")
        user_input = input()
        if user_input == "x":
            return
        else:
            for applicant in Applicant.select().where(Applicant.application_code >> None):
                applicant.application_code = populator.id_generator(ids)
                applicant.save()

            for applicant in Applicant.select().where(Applicant.school >> None):
                varos = City.get(City.city == applicant.city).school_city
                applicant.school = School.get(School.city == varos).id
                applicant.save()
        print("{0} applicants has been assigned an assigned id and school in the database.\n".format(len(ids)))


class SecondStory():

    def __init__(self):
        pass
