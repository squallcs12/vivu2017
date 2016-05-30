from django.conf.urls import url
from django.contrib.auth import views

urlpatterns = [
    url(r'^logout/$', views.logout, {'template_name': 'accounts/logged_out.html'}, name='logout'),
    url(r'^password_change/$', views.password_change, {
        'template_name': 'accounts/password_change.html',
        'extra_context': {
            'active_changepassword': True,
        }
    }, name='password_change'),
    url(r'^password_change/done/$', views.password_change_done, {
        'template_name': 'accounts/password_change_done.html'}, name='password_change_done'),

    url(r'^password_reset/$', views.password_reset,
        {'template_name': 'accounts/password_reset.html'}, name='password_reset'),
    url(r'^password_reset/done/$', views.password_reset_done,
        {'template_name': 'accounts/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm,
        {'template_name': 'accounts/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete,
        {'template_name': 'accounts/password_reset_complete.html'}, name='password_reset_complete'),
]
