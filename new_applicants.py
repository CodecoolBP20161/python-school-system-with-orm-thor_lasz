# New applicants arrive into your project database by this script.
# You can run it anytime to generate new data!
import random
import string
from models import *

def id_generator(ids):

    id = (''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(6)))
    while id in ids:
        id = (''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(6)))
    return id

db.connect()
db.drop_tables([School, Applicant, City, Mentor], safe=True)
db.create_tables([School, Applicant, City, Mentor], safe=True)

bp = School.create(city="Budapest")
miskolc = School.create(city="Miskolc")
krakow = School.create(city="Krakow")

cities = {
    "Érd": "Budapest",
    "Kiskunbüdösbütykös": "Miskolc",
    "Mars": "Miskolc",
    "Tijuana": "Budapest",
    "Decapod 10": "Miskolc",
    "Nimbus": "Budapest",
    "New New York": "Budapest"
}

applicants = [
    {"first_name": "Jack", "last_name": "Johnson", "email": "jackjohnson@gmail.com", "city": "Érd"},
    {"first_name": "John", "last_name": "Jackson", "email": "johnjackson@gmail.com", "city": "Kiskunbüdösbütykös"},
    {"first_name": "Amy", "last_name": "Wong", "email": "awong79@marslink.web", "city": "Mars"},
    {"first_name": "Bender", "last_name": "Bending Rodriguez", "email": "bender@ilovebender.com", "city": "Tijuana"},
    {"first_name": "John", "last_name": "Zoidberg", "email": "zoidberg@decapodians.deca", "city": "Decapod 10"},
    {"first_name": "Kif", "last_name": "Kroker", "email": "iamgreen@military.earth", "city": "Nimbus"},
    {"first_name": "Zapp", "last_name": "Brannigan", "email": "lovethezapper@military.earth", "city": "Nimbus"},
    {"first_name": "Hermes", "last_name": "Conrad", "email": "bureaucrat_conrad@gmail.com", "city": "New New York"},
    {"first_name": "Antonio", "last_name": "Calculon", "email": "allmycircuits@gmail.com", "city": "New New York"},
    {"first_name": "Philip", "last_name": "Fry", "email": "iloveleela@gmail.com", "city": "New New York"}
]

for key, value in cities.items():
    City.create(
        city=key,
        school_city=value
    )
for applicant in applicants:
    Applicant.create(
        first_name=applicant.get("first_name"),
        last_name=applicant.get("last_name"),
        email=applicant.get("email"),
        city=applicant.get("city"),
    )

mentor1 = Mentor.create(
    first_name="Lord",
    last_name="Nibbler",
    email="iamcute@nibblonians.niblo",
    school=bp
)

mentor2 = Mentor.create(
    first_name="Hubert",
    last_name="Farnsworth",
    email="",
    school=miskolc
)

ids = []
for applicant in Applicant.select():
    ids.append(applicant.application_code)

for applicant in Applicant.select().where(Applicant.application_code >> None):
    varos = City.select().where(City.city == applicant.city)
    print(varos.school_city)
    applicant.application_code = id_generator(ids)
    applicant.save()

for applicant in Applicant.select().where(Applicant.school >> None):
    applicant.school = 1
    applicant.save()
