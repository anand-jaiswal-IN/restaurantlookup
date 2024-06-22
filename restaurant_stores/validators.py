import re
from django.core.exceptions import ValidationError

def validate_phone(value):
    phone_regex = re.compile(r'^\+?1?\d{9,15}$') 

    if not phone_regex.match(value):
        raise ValidationError("Invalid phone number. It must be entered in the format: '+99xxxxxx'. Up to 15 digits allowed.")