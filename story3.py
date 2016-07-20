from peewee import *
from models import *

db.connect()


def get_app_info():
    ids = []
    for applicant in Applicant.select():
        ids.append(Applicant.application_code)
    app_num = input("Pls give me your app num: ")
    if app_num in ids:
        print(Applicant.get(app_num == Applicant.application_code)) #need to return all arguments

    else:
        print('Not a valid application code!')

get_app_info()
