import random
import string
from models import *


def id_generator(ids):
    # THIS NEEDS TO BE REPLACED!!!!!
    id = (''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(6)))
    while id in ids:
        id = (''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(6)))
    return id


def establish_connection():
    """ Connects to the database and creates the necessary tables. """
    db.connect()
    db.drop_tables([School, Applicant, City, Mentor], safe=True)
    db.create_tables([School, Applicant, City, Mentor], safe=True)


def populate_tables():
    """ Populates the tables with the example data. """
    cities, applicants, mentors = example_data()

    with db.atomic():
        City.insert_many(cities).execute()
        Applicant.insert_many(applicants).execute()
        Mentor.insert_many(mentors).execute()


def example_data():
    """ Contains the example data for populating the tables in the database. """

    cities = [
        {"city": "Érd", "school_city": "Budapest"},
        {"city": "Kiskunbüdösbütykös", "school_city": "Miskolc"},
        {"city": "Mars", "school_city": "Miskolc"},
        {"city": "Tijuana", "school_city": "Budapest"},
        {"city": "Decapod 10", "school_city": "Miskolc"},
        {"city": "Nimbus", "school_city": "Budapest"},
        {"city": "New New York", "school_city": "Budapest"}
    ]

    applicants = [
        {"first_name": "Jack", "last_name": "Johnson", "email": "jackjohnson@gmail.com", "city": "Érd"},
        {"first_name": "John", "last_name": "Jackson", "email": "johnjackson@gmail.com", "city": "Kiskunbüdösbütykös"},
        {"first_name": "Amy", "last_name": "Wong", "email": "awong79@marslink.web", "city": "Mars"},
        {"first_name": "Bender", "last_name": "Rodriguez", "email": "bender@ilovebender.com", "city": "Tijuana"},
        {"first_name": "John", "last_name": "Zoidberg", "email": "zoidberg@decapodians.deca", "city": "Decapod 10"},
        {"first_name": "Kif", "last_name": "Kroker", "email": "iamgreen@military.earth", "city": "Nimbus"},
        {"first_name": "Zapp", "last_name": "Brannigan", "email": "lovethezapper@military.earth", "city": "Nimbus"},
        {"first_name": "Hermes", "last_name": "Conrad", "email": "bureaucrat_conrad@gmail.com", "city": "New New York"},
        {"first_name": "Antonio", "last_name": "Calculon", "email": "allmycircuits@gmail.com", "city": "New New York"},
        {"first_name": "Philip", "last_name": "Fry", "email": "iloveleela@gmail.com", "city": "New New York"}
    ]

    bp = School.create(city="Budapest")
    miskolc = School.create(city="Miskolc")
    krakow = School.create(city="Krakow")

    mentors = [
        {"first_name": "Hubert", "last_name": "Farnsworth", "email": "", "school": bp},
        {"first_name": "Lord", "last_name": "Nibbler", "email": "iamcute@nibblonians.niblo", "school": miskolc}
    ]

    return cities, applicants, mentors
