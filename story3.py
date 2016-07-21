def __init__(self):

    ids = []
    for applicant in Applicant.select():
        ids.append(applicant.application_code)
    app_num = input("Please give me your application number: ")
    if app_num in ids:

        print('First name: ', Applicant.get(app_num == Applicant.application_code).first_name)
        print('Last name: ', Applicant.get(app_num == Applicant.application_code).last_name)
        print('Email: ', Applicant.get(app_num == Applicant.application_code).email)
        print('City: ', Applicant.get(app_num == Applicant.application_code).city)
        print('Application code: ', Applicant.get(app_num == Applicant.application_code).application_code)
        print('School: ', Applicant.get(app_num == Applicant.application_code).school)


    else:
        print('Not a valid application code!')
