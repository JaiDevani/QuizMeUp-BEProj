from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class UserManager(BaseUserManager):
    def create_user(self, username, email, contact,student,staff, password=None, is_active=True, is_student=False, is_staff=False, is_admin=False):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        elif not password:
            raise ValueError('Users must have a password')
        elif not contact:
            raise ValueError('Users must have a contact')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.username = username
        user.set_password(password)
        user.active = is_active
        user.contact = contact
        user.student = is_student
        user.staff = is_staff
        user.admin = is_admin
        user.save(using=self._db)
        return user
    def create_student(self, username, email, contact, student, staff,password=None):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            username,
            email,
            contact,
            student,
            staff,
            password=password,
        )
        user.username = username
        user.student = True
        user.staff = False
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, email, contact, student, staff, password=None):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            username,
            email,
            contact,
            student,
            staff,
            password=password,
        )
        user.username = username
        user.student = False
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, contact,  student=None, staff=None, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            username,
            email,
            contact,
            student,
            staff,
            password=password,
        )
        user.username = username
        user.staff = False
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=255, verbose_name='username')
    contact = models.CharField(max_length=10, verbose_name='contact',unique=True)
    active = models.BooleanField(default=True)
    student = models.BooleanField(default=False)
    staff = models.BooleanField() # a teachers user
    admin = models.BooleanField() # a superuser
    # notice the absence of a "Password field", that's built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','contact','student','staff'] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    @property
    def is_student(self):
        "Is the user a member of staff?"
        return self.is_student

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

    objects = UserManager()

class StudentRecord(models.Model):
    
    email = models.ForeignKey(User, related_name="stud_email",default=1, verbose_name="email", on_delete=models.SET_DEFAULT)
    subject_a = models.CharField(max_length=3)
    subject_b = models.CharField(max_length=3)
    #username = User.objects.raw('SELECT username FROM User where email = email')
    def __str__(self):
        return str(self.email)
    
    def get_scores(self):
        x = []
        x.append(self.subject_a)
        x.append(self.subject_b)
        return x