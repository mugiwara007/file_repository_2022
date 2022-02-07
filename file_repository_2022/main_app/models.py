from email.policy import default
from django.db import models

class Profiles(models.Model):
    profile_picture = models.ImageField(null=False, blank=True, default='user_profile.png')
    username = models.CharField(max_length=30, null=False, blank=False)
    eMail = models.CharField(max_length=30, null=False, blank=False)
    password = models.CharField(max_length=30, null=False, blank=False)
    security_question = models.CharField(max_length=100, null=False, blank=False)
    security_answer = models.CharField(max_length=100, null=False, blank=False)
    admin = models.BooleanField(default=False, null=False)
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return self.username
