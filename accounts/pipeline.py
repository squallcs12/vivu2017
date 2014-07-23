'''
Created on Aug 26, 2013

@author: antipro
'''
from django.http import HttpResponseRedirect
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from social_auth.exceptions import AuthException
from django.contrib.auth.models import User

def redirect_associate_by_email(details, user=None, *args, **kwargs):
    if user:
        return None

    if kwargs['request'].session.get('confirm_password'):
        del kwargs['request'].session['confirm_password']
        kwargs['request'].session.modified = True
        return None

    email = details.get('email')

    if email:
        # try to associate accounts registered with the same email address,
        # only if it's a single object. AuthException is raised if multiple
        # objects are returned
        # Allow case-insensitive match, since real-world email address is case-insensitive
        try:
            user = User.objects.get(email=email)
            return HttpResponseRedirect("/accounts/password_confirm")
        except MultipleObjectsReturned:
            raise AuthException(kwargs['backend'], 'Not unique email address.')
        except ObjectDoesNotExist:
            return None
