from django.contrib import admin


class SuggestAdmin(admin.ModelAdmin):
    list_display = ('address', 'province', 'lat', 'lng')
    list_filter = ('province',)
