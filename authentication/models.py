from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db.models import CASCADE

import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key = True, default=uuid.uuid4,editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)
    two_factor_enabled =  models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null= True,blank= True)
    failed_login_attempts = models.PositiveIntegerField(default = 0)
    account_locked_untill = models.DateTimeField(null=True,blank = True)
    # Avoid reverse accessor conflicts
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # Unique related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # Unique related_name
        blank=True,
    )
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
class UserDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name = 'devices')
    device_id = models.UUIDField(default = uuid.uuid4,editable = False)
    device_name = models.CharField(max_length = 100)
    device_type = models.CharField(max_length =  50)
    is_trusted = models.BooleanField(default = False)
    last_used = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add= True)
    
class LoginHistory(models.Model):
    user = models.ForeignKey(User,on_delete= CASCADE, related_name = 'login_history')
    login_datetime = models.DateTimeField(auto_now_add = True)
    ip_address = models.GenericIPAddressField()
    device_info = models.CharField(max_length = 255)
    status = models.CharField(max_length = 20)
    
    location = models.CharField(max_length = 255, blank = True, null = True)
    