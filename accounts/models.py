import re

from awesome_avatar.fields import AvatarField
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

try:
    from south.modelsinspector import add_introspection_rules

    add_introspection_rules([], ["^awesome_avatar\.fields\.AvatarField"])
except ImportError:
    pass

GENDER_CHOICES = (
    (True, 'Male'),
    (False, 'Female'),
)


class User(AbstractUser):
    fullname = models.CharField(max_length=255, blank=True, default='')
    avatar = AvatarField(upload_to='avatars', width=200, height=200)
    homepage = models.URLField(default='', blank=True)
    gender = models.BooleanField(default=True, choices=GENDER_CHOICES)
    birthday = models.DateField(blank=True, null=True, default=None)
