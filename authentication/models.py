from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key = True, default=uuid.uuid4,editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.Charfield(max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)
    two_factor_enabled =  models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null= True,blank= True)
    failed_login_attempts = models.PositiveIntegerField(default = 0)
    account_locked_untill = models.DateTimeField(null=True,blank = True)