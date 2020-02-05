from django.shortcuts import render,HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .forms import RegisterForm
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate, login
from .models import User, StudentRecord
from django.contrib.auth.forms import User
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def index(request):
      return render(request, "index.html")

def about(request):
      return render(request, "about.html")

def contact(request):
      return render(request, "contact.html")

def register(request):
      form = RegisterForm(request.POST or None)
      context = {
            "form": form
      }
      if form.is_valid():
            print(form.cleaned_data)
            username = form.cleaned_data.get("username")
            email  = form.cleaned_data.get("email")
            contact  = form.cleaned_data.get("contact")
            password  = form.cleaned_data.get("password")
            password2 = form.cleaned_data.get("password2")
            posting = form.cleaned_data.get("posting")
            if (password and password2 and password!=password2):
                  print("Error bc")
            else:
                  if posting == "Select a role":
                        raise forms.ValidationError("Please select student or staff")
                  elif posting == "Student":
                        new_user  = User.objects.create_student(username, email, contact, True, False, password)
                        print(new_user)
                  else:
                        new_user  = User.objects.create_staffuser(username, email, contact, False, True, password)
                        print(new_user) 

      return render(request, "register.html", context)
#staff links
def staff_request(request):
      return render(request, "t_index.html")

def staff_quiz(request):
      return HttpResponse("Existing Quiz ")

def staff_class(request):  
      query_results = StudentRecord.objects.all()
      return render(request, "staff/studentlist.html", {'students':query_results})
#student links
def stud_request(request):
      return render(request, "s_index.html")

def stud_history(request):
      return HttpResponse("History ")
def stud_scores(request):
      return HttpResponse("Scores ")

def stud_test(request):
      return render(request, "students/test.html")

def login_user(request):  
      if request.method == 'POST':
            #form = AuthenticationForm(request=request, data=request.POST)
            print(request.POST)
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                  if user.is_admin==True:
                        return render(request, "index.html")
                  elif user.student==True:
                        return redirect('stud_request')
                  elif user.staff==True:
                        return redirect('staff_request')
                        
      form = AuthenticationForm()
      return render(request = request,template_name = "login.html",context={"form":form})

def logout_request(request):
    logout(request)
    return render(request, "index.html")

