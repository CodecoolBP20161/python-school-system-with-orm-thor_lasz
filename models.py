from peewee import *
import getpass
import random
import string
from tabulate import tabulate

# Configure your database connection here
# database name = should be your username on your laptop
# database user = should be your username on your laptop
db = PostgresqlDatabase(str(getpass.getuser()), user=str(getpass.getuser()))


class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    @classmethod
    def get_model_attributes(cls):
        """ Returns the model's attributes
        :returns: list -- a list of strings of the attributes
        """
        return cls._meta.sorted_field_names

    class Meta:
        database = db


class School(BaseModel):
    city = CharField()


class Mentor(BaseModel):
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    school = ForeignKeyField(School, related_name="mentor", null=True)


class InterviewSlot(BaseModel):
    start = DateTimeField()
    end = DateTimeField()
    reserved = BooleanField(default=False)
    school_id = IntegerField(null=True)
    mentor = ForeignKeyField(Mentor, null=True, related_name="interviewslot_1")
    second_mentor = ForeignKeyField(Mentor, null=True, related_name="interviewslot_2")

    @classmethod
    def get_interview_dates(cls, mentors_name):
        interview_data = []
        name = ""
        app_code = ""
        for interview in cls.select().join(Mentor).where(Mentor.first_name % str("%" + mentors_name + "%")):
            for applicant in interview.applicant:
                name = applicant.first_name + " " + applicant.last_name
                app_code = applicant.application_code
            interview_data.append([interview.start, interview.end, name, app_code])

        return interview_data


class City(BaseModel):
    city = CharField()
    school_city = CharField()


class Applicant(BaseModel):
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    city = CharField()
    application_code = CharField(null=True)
    school = ForeignKeyField(School, related_name='applicant', null=True)
    interview = ForeignKeyField(InterviewSlot, null=True, related_name='applicant')
    status = CharField(default='New applicant')

    @classmethod
    def get_application_codes(cls):
        """ Saves to the class and returns all application codes of the applicants. """
        cls.application_codes = [applicant.application_code for applicant in Applicant.select()]
        return cls.application_codes

    @staticmethod
    def get_applicants_without_code():
        """ Returns those applicants who do not have application codes. """
        return Applicant.select(
                Applicant.first_name,
                Applicant.last_name,
                Applicant.email,
                Applicant.city
        ).where(Applicant.application_code >> None).tuples()

    @staticmethod
    def get_applicants_without_interview():
        """ Returns those applicants who do not have an interview slot reserved. """
        return Applicant.select(
            Applicant.first_name,
            Applicant.last_name,
            Applicant.email,
            Applicant.city
        ).where(Applicant.interview >> None).tuples()

    @classmethod
    def application_code_generator(cls):
        """ Generates a new, random, six-digit application code that is unique to other application codes. """
        application_code = (''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(6)))
        while application_code in cls.application_codes:
            application_code = (''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(6)))
        return application_code

    @classmethod
    def assign_application_code(cls):
        """ Assigns application code to those applicants who do not have one and returns them in a list. """
        applicants = []
        for applicant in Applicant.select().where(Applicant.application_code >> None):
            applicant.application_code = cls.application_code_generator()
            applicant.save()
            applicants.append([
                    applicant.first_name, applicant.last_name,
                    applicant.application_code, applicant.school.city, applicant.email
                ])
        return applicants

    @staticmethod
    def assign_school():
        """ Assigns a school to those applicants who do not have one. """
        for applicant in Applicant.select().where(Applicant.school >> None):
            city = City.get(City.city == applicant.city).school_city
            applicant.school = School.get(School.city == city).id
            applicant.save()

    # def free_interview_slot():
    #     for applicant in Applicant.select().where(Applicant.interview >> None):
    #         for slot in InterviewSlot.select().where(InterviewSlot.reserved >> False).order_by(InterviewSlot.start):
    #             if slot.school_id == applicant.school_id:
    #                 return slot

    @staticmethod
    def assign_interview():
        """ Assigns an interview to those applicants who do not have one and returns them in a list. """
        updated_applicants = []
        interview = None
        for applicant in Applicant.select().where(Applicant.interview >> None):

            number_of_mentors = input("How many mentors needed for the interview? ")
            for slot in InterviewSlot.select().where(InterviewSlot.reserved >> False).order_by(InterviewSlot.start):
                if slot.school_id == applicant.school_id:
                    interview = slot
                    break

            if interview == None:
                print("There is no matching applicant, please check applicants school!")
                break
            else:
                interview.reserved = True
                interview.save()
                applicant.interview = interview
                applicant.save()
                updated_applicants.append(
                    [applicant.first_name, applicant.last_name, applicant.application_code,
                     applicant.interview.start, applicant.interview.mentor.first_name,
                     applicant.interview.mentor.last_name]
                )

                if number_of_mentors == '2':
                    print ("i'm in")
                    for mentor_b in Mentor.select():
                        if mentor_b.school_id == interview.school_id and  mentor_b != interview.mentor:
                            print (mentor_b.id)
                            interview.second_mentor = mentor_b
                            interview.save()
                            break
                else:
                    continue

        return updated_applicants


class Question(BaseModel):
    content = CharField()
    answer = CharField(null=True)
    applicant = ForeignKeyField(Applicant, related_name="applicant_question", null=True)
    mentor = ForeignKeyField(Mentor, related_name="mentor_question", null=True)
    status = CharField(default="New")
    time = DateTimeField()

    @staticmethod
    def print_result(result):
        if result == []:
            print("\nNo macthing question\n")
        else:
            print(tabulate(result, headers=["Content", "Answer", "Applicant", "Mentor", "Status"]))
        go_on = input("\nPress any key to continue\n")

    @classmethod
    def get_questions_for_applicant(cls, applicant_id):
        applicants_questions = []
        for question in cls.select().join(Applicant).where(Applicant.application_code == applicant_id):
            applicants_questions.append([question.content, question.answer, question.mentor, question.status])

        return applicants_questions

    @classmethod
    def get_questions_for_administrator(cls):
        question_data = []

        for question in cls.select():
            question_data.append([
                question.id, question.content, question.status, question.time, question.applicant.application_code
                ])
            if question.mentor is not None:
                question_data[-1].append(str(question.mentor.first_name + " " + question.mentor.last_name))
            else:
                question_data[-1].append("")
            if question.applicant.school is not None:
                question_data[-1].append(question.applicant.school.city)
            else:
                question_data[-1].append("")
        return question_data

    @classmethod
    def get_mentors_for_question(cls, selected_question):
        mentors = []

        try:
            school_id = cls.get(cls.id == selected_question).applicant.school.id
        except AttributeError:
            print("You cannot assign a mentor to a question, if the applicant is not assigned to a school!\n")
            return
        except Question.DoesNotExist:
            print("Please choose a valid question id!\n")
            return

        for mentor in Mentor.select().join(School).where(School.id == school_id):
            mentors.append([mentor.id, mentor.first_name + " " + mentor.last_name])

        return mentors

    @classmethod
    def assign_mentor(cls, question_id, mentor_id):
        question = cls.get(cls.id == question_id)
        question.mentor = mentor_id
        question.status = "Waiting for answer"
        question.save()
