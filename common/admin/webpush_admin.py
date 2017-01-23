from django.contrib import admin


class GroupAdmin(admin.ModelAdmin):
    list_display = ('browser', 'endpoint', 'auth')


class PushInformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'subscription', 'group')


class SubscriptionInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'browser', 'endpoint', 'auth')
