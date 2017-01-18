from django.contrib import admin

from progress.admin.milestone_admin import MilestoneAdmin
from progress.admin.progress_admin import ProgressAdmin
from progress.models import Milestone, Progress

admin.site.register(Milestone, MilestoneAdmin)
admin.site.register(Progress, ProgressAdmin)
