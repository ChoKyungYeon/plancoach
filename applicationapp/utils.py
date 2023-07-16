

def teacher_application_classification(teacher):
    application_queryset = teacher.application_teacher.all()

    temp_application_dict = {'applied': [], 'matching': [], 'waiting': []}

    for application in application_queryset:
        if application.state == 'applied':
            state_key = 'applied'
        elif application.state == 'waiting':
            state_key = 'waiting'
        elif application.state == 'matching':
            state_key = 'matching'
        else:
            continue
        temp_application_dict[state_key].append(application)
    return temp_application_dict['applied'], temp_application_dict['matching'], temp_application_dict['waiting']

