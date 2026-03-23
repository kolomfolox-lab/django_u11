import random
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def exp_time_now():
    return timezone.now() + timedelta(minutes=2)

def generate_code():
    return random.randint(100000, 999999)

class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.PositiveIntegerField(default=generate_code)
    expired_date = models.DateTimeField(default=exp_time_now)
