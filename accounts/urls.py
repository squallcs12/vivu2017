from django.conf.urls import url

from accounts.views import set_password_view, social_view
from accounts.views.profile_view import EditProfileView, ProfileView


urlpatterns = [

    url(r'^profile', ProfileView.as_view(editable=True), name='profile'),
    url(r'^edit_profile', EditProfileView.as_view(), name='edit_profile'),

    url(r'^set_password', set_password_view.main, name='set_user_password'),
    url(r'^password_set/done/$', set_password_view.done, name='password_set_done'),

    url(r'^social', social_view.main, name='social_list'),
]
