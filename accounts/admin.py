'''
Created on Apr 13, 2014

@author: antipro
'''
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts import models


admin.site.register(models.User, UserAdmin)
