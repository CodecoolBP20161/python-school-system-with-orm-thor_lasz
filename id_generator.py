import random
import string


def id_generator():
    id = (''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(6)))
    applicants = Applicant.objects
    ids = []
    for applicant in applicants:
        ids.append(applicant.id)
    if id in ids:
        id = (''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(6)))
    return id

print(id_generator())
