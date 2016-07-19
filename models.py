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
    school_city = CharField

class School(BaseModel):
    city = CharField()

class Applicant(BaseModel):
    """Model representation of a Codecool class."""
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    city = CharField
    application_code = CharField
    school = ForeignKeyField(School, related_name='applicant', default=None)

    # def mentors(self):
    #     return self.mentor

db.connect()
db.create_tables([School, Applicant, City], safe=True)
bp1 = School.create(city = "Budapest", year=2016)
