from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('login', views.login_user, name="login_user"),
    path('register', views.register, name="register"),
    path('logout', views.login_user, name="logout_request"),

    #student links
    path('student', views.stud_request, name="stud_request"),
    path('student/history', views.stud_history, name="stud_history"),
    path('student/scores', views.stud_scores, name="stud_scores"),
    path('student/test', views.stud_test, name="stud_test"),
    #staff links
    path('staff', views.staff_request, name="staff_request"),
    path('staff/quiz', views.staff_quiz, name="staff_quiz"),
    path('staff/students', views.staff_class, name="staff_class"),
]