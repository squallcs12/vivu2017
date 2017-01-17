from django.contrib import admin

from progress.models import Progress, Milestone


class MilestoneInline(admin.TabularInline):
    model = Milestone


class ProgressAdmin(admin.ModelAdmin):
    inlines = [
        MilestoneInline,
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProgressAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['state'].queryset = form.base_fields['state'].queryset.filter(progress=obj)
        return form

admin.site.register(Progress, ProgressAdmin)
