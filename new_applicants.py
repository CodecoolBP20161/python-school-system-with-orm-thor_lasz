# New applicants arrive into your project database by this script.
# You can run it anytime to generate new data!

from models import *

db.connect()
db.create_tables([School, Applicant, City, Mentor], safe=True)

bp = School.create(city="Budapest")
miskolc = School.create(city="Miskolc")

applicant1 = Applicant.create(
    first_name="Jack",
    last_name="Johnson",
    email="jackjohnson@gmail.com",
    city="Érd",
    application_code=None,
    school=None
)

applicant2 = Applicant.create(
    first_name="John",
    last_name="Jackson",
    email="johnjackson@gmail.com",
    city="Kiskunbüdösbütykös",
    application_code=None,
    school=None
)

applicant3 = Applicant.create(
    first_name="Amy",
    last_name="Wong",
    email="awong79@marslink.web",
    city="Mars",
    application_code=None,
    school=None
)

applicant4 = Applicant.create(
    first_name="Bender",
    last_name="Bending Rodriguez",
    email="bender@ilovebender.com",
    city="Tijuana",
    application_code=None,
    school=None
)

applicant5 = Applicant.create(
    first_name="John",
    last_name="Zoidberg",
    email="zoidberg@decapodians.deca",
    city="Decapod 10",
    application_code=None,
    school=None
)

applicant6 = Applicant.create(
    first_name="Kif",
    last_name="Kroker",
    email="iamgreen@military.earth",
    city="Nimbus",
    application_code=None,
    school=None
)

applicant7 = Applicant.create(
    first_name="Zapp",
    last_name="Brannigan",
    email="lovethezapper@military.earth",
    city="Nimbus",
    application_code=None,
    school=None
)

applicant8 = Applicant.create(
    first_name="John",
    last_name="Zoidberg",
    email="zoidberg@decapodians.deca",
    city="Decapod 10",
    application_code=None,
    school=None
)

applicant9 = Applicant.create(
    first_name="Antonio",
    last_name="Calculon",
    email="allmycircuits@gmail.com",
    city="New New York",
    application_code=None,
    school=None
)

applicant10 = Applicant.create(
    first_name="Philip",
    last_name="Fry",
    email="iloveleela@gmail.com",
    city="New New York",
    application_code=None,
    school=None
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

# print(bp1.applicants()[1].first_name)
