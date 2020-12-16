from django.contrib import messages
from django.http import request
from .models import User
from re import error
from django.shortcuts import redirect, render
import bcrypt
from bcrypt import checkpw

def index(request):
  print('\n --------- index / -------')
  if "user_session_id" in request.session:
    print('user already logged in! maybe clear session?')
  return render(request, 'index.html')

def success(request):
  if "user_session_id" not in request.session:
    return redirect('/')
  else:
    logged_in_user = User.objects.get(id=request.session['user_session_id'])
    
    context = {
      'logged_in_user' : logged_in_user
    }
  return render(request, 'success.html', context)

def register(request):
  print('\n --------- register method -------')
  if request.method == "POST":
    errors = User.objects.validate_registration(request.POST)
    if len(errors) > 0:
      for key_category, message_val in errors.items():
        messages.error(request, message_val, extra_tags="danger")
        # messages.error(request, message_val, extra_tags=key_category)
      return redirect('/')
    else:
      # create user vars from POST:
      first_name = request.POST['first_name']
      last_name = request.POST['last_name']
      email = request.POST['email']
      birthday = request.POST['birthday']

      password = request.POST['password']
      hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
      
      #create the user in db
      User.objects.create(first_name=first_name, last_name=last_name, email=email, birthday=birthday, password=hashed_pw)
      
      # once we create the user, we have the email from POST
      # log them in -> put in session
      request.session['user_session_id'] = User.objects.get(email=request.POST['email']).id
      
      messages.success(request, "welcome from REGISTRATION")
      return redirect('/success')

def login(request):
  print('\n --------- login method -------')
  if request.method == "POST":
    print(request.POST)
    
    errors = User.objects.loginErrors(request.POST)
    
    if errors:
      for key, value in errors.items():
        messages.error(request, value, extra_tags="danger")
      return redirect('/')
    else:
      request.session['user_session_id'] = User.objects.get(email=request.POST['email']).id
      messages.success(request, "Welcome from login!")
      return redirect('/success')

  return redirect('/')

def logout(request):
  print('\n --------- LOGOUT ⛔ -------')
  if "user_session_id" in request.session:
    request.session.pop('user_session_id')
    request.session.clear()
    messages.warning(request, "session cleared - all users logged out!")

    return redirect('/')
  else:
    messages.warning(request, "nothing to clear", extra_tags="warning")
    return redirect('/')
  # get user form db
  # if list is empty they are not in db = kick them out! or retry
  # userList = User.objects.filter(email=request.POST['email'])
  # if userList:
  #   user = userList[0]
  # return redirect('/')
