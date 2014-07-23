from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'root.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'common.views.home_view.main', name='homepage'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^/', include('common.urls')),
)
