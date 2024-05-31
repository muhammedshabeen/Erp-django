from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .utils import *
# Create your models here.

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    
    

class UserModel(AbstractUser):
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(_('email address'), unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=12,blank=True,unique=True)
    user_type= models.CharField(default='Employer',max_length=20,null=True,choices=(
        ('HR','HR'),
        ('Project Manager','Project Manager'),
        ('GM','GM'),
        ('Employer','Employer')
    ))
    status = models.CharField(default='Pending',max_length=20,choices=(
        ('Active','Active'),
        ('Inactive','Inactive'),
        ('Deleted','Deleted'),
        ('Pending','Pending')
    ))
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Add related_name here
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name=_('groups'),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Add related_name here
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions'),
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    
class MainTask(BaseContent):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    

class Task(BaseContent):
    main_task = models.ForeignKey(MainTask,on_delete=models.CASCADE)
    description = models.TextField()
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    task_status = models.CharField(default='Assigned',max_length=20,choices=(
        ('Assigned','Assigned'),
        ('In Progress','In Progress'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
        ('Cancelled', 'Cancelled'),
        ('Delayed', 'Delayed'),
        ('Under Review', 'Under Review'),
        ('Blocked', 'Blocked'),
    ))
    # duration = models.IntegerField(default=0)
    time_duration = models.IntegerField()
    
    def __str__(self):
        return self.description