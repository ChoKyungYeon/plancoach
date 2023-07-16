def is_consult_ongoing(consult):
    if consult.state == 'new':
        return False
    else:
        return True



