'''
Created on Sep 16, 2013

@author: antipro
'''
from django import forms

from accounts.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
