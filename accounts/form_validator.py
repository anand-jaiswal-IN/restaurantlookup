import re

def is_valid_username(username):
    regex = r'^[a-zA-Z0-9_-]{3,150}$'
    return re.match(regex, username) is not None

def is_valid_password(password):
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$'
    '''
    at least one lowercase
    at least one uppercase
    at least one digit
    at least one special characters
    minimum length is 8
    '''
    return re.match(regex, password) is not None

def is_valid_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None