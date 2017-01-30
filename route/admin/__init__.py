from django.contrib import admin

from route.admin.suggest_admin import SuggestAdmin
from route.models import Suggest

admin.site.register(Suggest, SuggestAdmin)
