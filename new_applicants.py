# New applicants arrive into your project database by this script.
# You can run it anytime to generate new data!

from models import *

db.connect()
db.create_tables([School, Applicant, City], safe=True)

bp1 = School.create(city="Budapest")

applicant1 = Applicant.create(
    first_name="Jack",
    last_name="Johnson",
    email="jackjohnson@gmail.com",
    city="Érd",
    application_code="",
    school=bp1
)

applicant2 = Applicant.create(
    first_name="John",
    last_name="Jackson",
    email="johnjackson@gmail.com",
    city="Kiskunbüdösbütykös",
    application_code="",
    school=bp1
)

applicant3 = Applicant.create(
    first_name="Amy",
    last_name="Wong",
    email="awong79@marslink.web",
    city="Mars",
    application_code="",
    school=bp1
)

applicant4 = Applicant.create(
    first_name="Bender",
    last_name="Bending Rodriguez",
    email="bender@ilovebender.com",
    city="Tijuana",
    application_code="",
    school=bp1
)

applicant5 = Applicant.create(
    first_name="John",
    last_name="Zoidberg",
    email="zoidberg@decapodians.deca",
    city="Decapod 10",
    application_code="",
    school=bp1
)

# print(bp1.applicants()[1].first_name)
