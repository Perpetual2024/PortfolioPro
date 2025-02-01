import re
from models import get_user_by_email

def validate_email_format(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

def validate_unique_email(email):
    user = get_user_by_email(email)
    return user is None

def validate_user_data(request_data):
    if 'email' not in request_data or not validate_email_format(request_data['email']):
        return False, "Invalid or missing email format"
    
    if not validate_unique_email(request_data['email']):
        return False, "Email already in use"
    
    return True, None

def validate_project_data(request_data):
    if 'title' not in request_data or 'description' not in request_data or 'image' not in request_data or 'user_id' not in request_data:
        return False, "Project must have a title and description"
    
    if len(request_data['title']) < 5:
        return False, "Project title must be at least 5 characters long"
    
    if len(request_data['description']) < 10:
        return False, "Project description must be at least 10 characters long"
    
    if 'image'not in request_data["image"]:
        return False, "Project must have an image"
    
    if 'user_id' not in request_data or not request_data['user_id'].isdigit():
        return False, "Invalid user id"
    
    
    return True, None
