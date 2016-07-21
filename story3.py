def __init__(self):

    ids = []
    for applicant in Applicant.select():
        ids.append(applicant.application_code)
    app_num = input("Please give me your application number: ")
    if app_num in ids:

        Applicant_objekt = Applicant.get(app_num == Applicant.application_code)
        print('First name: ', Applicant_objekt.first_name)
        print('Last name: ', Applicant_objekt.last_name)
        print('Email: ', Applicant_objekt.email)
        print('City: ', Applicant_objekt.city)
        print('Application code: ', Applicant_objekt.application_code)
        print('School: ', Applicant_objekt.school)


    else:
        print('Not a valid application code!')
