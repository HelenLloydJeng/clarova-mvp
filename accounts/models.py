from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Organisation(models.Model):
    name = models.CharField(max_length=120, unique=True)
    sector = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    ROLE_ADMIN = 'admin'
    ROLE_APPROVER = 'approver'
    ROLE_EDITOR = 'editor'
    ROLE_LEARNER = 'learner'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_APPROVER, 'Approver'),
        (ROLE_EDITOR, 'Editor'),
        (ROLE_LEARNER, 'Learner'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, null=True, blank=True, on_delete=models.SET_NULL)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_EDITOR)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

