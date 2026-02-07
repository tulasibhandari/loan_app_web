from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom user model matching PyQt5 App"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('officer', 'Officer'),
        ('accountant', 'Accountant'),
        ('user', 'User'),
    ]

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='user')
    post = models.CharField(max_length=100, blank=True, null=True)
    full_name_nepali = models.CharField(max_length=200, blank=True, null=True)
    reset_code = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    