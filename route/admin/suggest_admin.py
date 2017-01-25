from django.contrib import admin


class SuggestAdmin(admin.ModelAdmin):
    list_display = ('name', 'hash_id', 'address', 'province', 'lat', 'lng')
    list_filter = ('province',)
