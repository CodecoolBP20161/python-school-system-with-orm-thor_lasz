from peewee import *

# Configure your database connection here
# database name = should be your username on your laptop
# database user = should be your username on your laptop
db = PostgresqlDatabase('handris', user='handris')


class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = db


class City(BaseModel):
    city = CharField()
    school_city = CharField()


class School(BaseModel):
    city = CharField()


class Applicant(BaseModel):
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    city = CharField()
    application_code = CharField(null=True)
    school = ForeignKeyField(School, related_name='applicant', null=True)
    interview = DateField(null=True)


class Mentor(BaseModel):
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    school = ForeignKeyField(School, related_name="mentor", null=True)


class InterviewSlot(BaseModel):
    slot = DateField()
    mentor = ForeignKeyField(Mentor, related_name="interview", null=True)
    applicant = ForeignKeyField(Applicant, related_name="interview", null=True)
