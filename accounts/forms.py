'''
Created on Sep 16, 2013

@author: antipro
'''
from django import forms

from accounts.models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
