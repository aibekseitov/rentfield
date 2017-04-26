from secrets import token_urlsafe

from django.contrib.auth.models import PermissionsMixin, User
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

import uuid

class Profile(models.Model):
    class Types:
        client = 0
        manager = 1
    user = models.OneToOneField(User, related_name='profile')
    token = models.CharField(max_length=50)
    type = models.IntegerField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+77021112233'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=15,validators=[phone_regex], blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return ' - '.join([str(self.user), ("Manager" if (self.type == 1) else "Client"), self.phone_number])
