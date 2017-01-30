from django.contrib import admin


class SuggestAdmin(admin.ModelAdmin):
    list_display = ('name', 'hash_id', 'address', 'province', 'lat', 'lng', 'is_approved', 'is_chosen')
    list_filter = ('province',)
