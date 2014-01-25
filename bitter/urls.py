from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bitter.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'bitter_app.views.index'), # root
    url(r'^login$', 'bitter_app.views.login_view'), # login
    url(r'^logout$', 'bitter_app.views.logout_view'), # logout
    url(r'^signup$', 'bitter_app.views.signup'), # signup

    url(r'^admin/', include(admin.site.urls)),
)
