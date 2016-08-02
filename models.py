from peewee import *
import getpass
import random
import string

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
    mentor = ForeignKeyField(Mentor, null=True)


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
    interview = ForeignKeyField(InterviewSlot, null=True)
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
                    applicant.application_code, applicant.school.city
                ])
        return applicants

    @staticmethod
    def assign_school():
        """ Assigns a school to those applicants who do not have one. """
        for applicant in Applicant.select().where(Applicant.school >> None):
            city = City.get(City.city == applicant.city).school_city
            applicant.school = School.get(School.city == city).id
            applicant.save()

    @staticmethod
    def assign_interview():
        """ Assigns an interview to those applicants who do not have one and returns them in a list. """
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

    @classmethod
    def get_applicant_data(cls, ids, app_num):
        if app_num in ids:
            Applicant_objekt = Applicant.get(app_num == Applicant.application_code)
            result = [["Name: ", Applicant_objekt.first_name + " " + Applicant_objekt.last_name],
                      ["Email adress:", Applicant_objekt.email],
                      ["City: ", Applicant_objekt.city], ["Application code: ", Applicant_objekt.application_code],
                      ["School:", Applicant_objekt.school], ["Status:", Applicant_objekt.status]]
            return result
        else:
            return ["Invalid application code"]



