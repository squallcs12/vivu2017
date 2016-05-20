from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth import views
from social.backends.google import GooglePlusAuth

from accounts.views import set_password_view, social_view
from accounts.views.profile_view import EditProfileView, ProfileView

urlpatterns = [
    url(r'^login/$', views.login, {
        'template_name': 'accounts/login.html',
        'extra_context': {
            'plus_scope': ','.join(GooglePlusAuth.DEFAULT_SCOPE),
            'plus_id': settings.SOCIAL_AUTH_GOOGLE_PLUS_KEY,
        },
    }, name='login'),
    url(r'^logout/$', views.logout, {'template_name': 'accounts/logged_out.html'}, name='logout'),
    url(r'^password_change/$', views.password_change, {
        'template_name': 'accounts/password_change.html',
    }, name='password_change'),
    url(r'^password_change/done/$', views.password_change_done, {
        'template_name': 'accounts/password_change_done.html'}, name='password_change_done'),

    url(r'^password_reset/$', views.password_reset,
        {'template_name': 'accounts/password_reset.html'}, name='password_reset'),
    url(r'^password_reset/done/$', views.password_reset_done,
        {'template_name': 'password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm,
        {'template_name': 'accounts/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete,
        {'template_name': 'accounts/password_reset_complete.html'}, name='password_reset_complete'),

    url(r'^profile', ProfileView.as_view(editable=True), name='profile'),
    url(r'^edit_profile', EditProfileView.as_view(), name='accounts_edit_profile'),

    url(r'^set_password', set_password_view.main, name='set_user_password'),
    url(r'^password_set/done/$', set_password_view.done, name='password_set_done'),

    url(r'^social', social_view.main, name='accounts_social_list'),
]
