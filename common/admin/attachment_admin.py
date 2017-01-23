from django.contrib import admin


class AttachmentAdmin(admin.ModelAdmin):
    search_fields = ('file',)
