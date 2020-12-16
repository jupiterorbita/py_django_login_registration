from django.db import models
from datetime import date
import re
from bcrypt import checkpw

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
  #=========== REGISTRATION ERRORS =============
  def validate_registration(self, postData):
    
    today = date.today()
    errors = {}
    
    #catch all
    for key in postData.keys():
      if len(postData[key]) == 0:
        errors[key] = "all fields must be completed!"
        return errors

    
    # check FIRST NAME
    if len(postData['first_name']) < 1:
      errors['first_name'] =  "FIRST name cannot be empty"
    elif len(postData['first_name']) < 3:
      errors['first_name'] =  "FIRST name must be at least 3 letters"
    
    # check LAST NAME
    if len(postData['last_name']) < 1:
      errors['last_name'] =  "LAST name cannot be empty"
    elif len(postData['last_name']) < 3:
      errors['last_name'] =  "LAST name must be at least 3 letters"
      
    # check EMAIL
    if len(postData['email']) < 1:
      errors['email'] = "EMAIL cannot be empty"
    elif not EMAIL_REGEX.match(postData['email']):
      errors['email'] = "Invalid email address!"
    # if email exists in DB
    if User.objects.filter(email=postData['email']):
      errors['email'] = "EMAIL already exists, STOP!"
      
    # check BIRTHDAY
    if postData['birthday'] > str(today):
      errors['birthday'] = "BIRTHDAY should be in the past!"
    # check bday AGE
    birthday = postData['birthday']
    bday_result = check_birthday(birthday)
    if bday_result != True:
      errors['birthday'] = "you must be over 13 years to register"
    
    # PASSWORD
    if len(postData['password']) < 1:
      errors['password'] = "PASSWORD cannot be empty!"
    elif len(postData['password']) < 8:
      errors['password'] = "PASSWORD must be at least 8 characters long"
    
    if postData['password'] != postData['password_confirm']:
      errors['password'] = "PASSWORD does not match"
    return errors
  
    # str.isalpha() -- returns a boolean that shows whether a string contains only alphabetic characters
    # time.strptime(string, format) -- changes a string to a time using the given format
    

  # ============= LOGIN ERRORS ==================
  def loginErrors(self, postData):
    
    errors = {}
    
    #check if email is valid
    if len(postData['email']) < 1:
      errors['email'] = "EMAIL cannot be empty!"
      print(">>>>>>>>>>>>>>>")
      print(len(postData['email']))
    elif not EMAIL_REGEX.match(postData['email']):
      errors['email'] = "EMAIL NOT valid format!"
    # check if email is in db
    elif len(User.objects.filter(email=postData['email'])) < 1:
      errors['email'] = "Login error email - not found"
    else: # if email exists continue to password check
      # retrive the user using email
      user_check = User.objects.filter(email=postData['email'])
      print(">>>>>>>>>>>>>>>")
      print(user_check[0])
      if len(postData['password']) < 1:
        errors['password'] = "PASSWORD cannot be empty!"
      elif not checkpw(postData['password'].encode(), user_check[0].password.encode()):
        errors['password'] = "Login Error - Password doesn't match!"
    return errors


def check_birthday(birthday):  
  today = str(date.today())
  today_year_str = ""
  bday_year_str = ""
  
  for i in range(len(birthday)-6):
    bday_year_str += birthday[i]
  for i in range(len(today)-6):
    today_year_str += today[i]

  if (int(today_year_str) - int(bday_year_str)) > 13:
    return True



class User(models.Model):
  first_name = models.CharField(max_length=80)
  last_name = models.CharField(max_length=80)
  email = models.EmailField(max_length=80)
  password = models.CharField(max_length=255)
  birthday = models.DateField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()