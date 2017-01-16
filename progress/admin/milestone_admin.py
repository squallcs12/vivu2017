from django.contrib import admin

from progress.models import Milestone


class MilestoneAdmin(admin.ModelAdmin):
    pass


admin.site.register(Milestone, MilestoneAdmin)
