from datetime import date
from django.utils import timezone
import re
import phonenumbers

def validate_password(password):
    refined_password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,}'
    status = re.findall(refined_password_pattern,password)
    if status:
        return True
    return False

def validate_phone_number(number):
    
    try:

        parsed_number = phonenumbers.parse(number,region=None)
        is_validate_number = phonenumbers.is_valid_number(parsed_number)
        return is_validate_number
    
    except:
        return False

def validate_birth_date(birth_date):

    if not isinstance(birth_date, date):
        return False 

    current_date = timezone.now().date()
    if birth_date > current_date:
        return False
    
    age = current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))
    
    min_age = 18
    if age < min_age:
        return False
        
    return True
