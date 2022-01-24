from django.db import models
from django.contrib.auth.models import User

class UserOTP(models.Model):
    username = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)
    otp = models.CharField(max_length=10)

    def __str__(self):
        return self.username

class UserAgreement(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, primary_key=True)
    agreement = models.BooleanField(default=False)

