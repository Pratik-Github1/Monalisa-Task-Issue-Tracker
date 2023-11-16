from datetime import date
from django.contrib.auth.models import User
from django.db import models
from random import randint

class Sub_Admin_Table(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_sub_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sub_admins_created')

    def __str__(self):
        return self.user.username
    
class Manager_Table(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='hrs_created')

    def __str__(self):
        return self.user.username