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
    url(r'^beets$', 'bitter_app.views.public'),
    url(r'^submit$', 'bitter_app.views.submit'),
    url(r'^users/$', 'bitter_app.views.users'),
    url(r'^users/(?P<username>\w{0,30})/$', 'bitter_app.views.users'),
    url(r'^follow$', 'bitter_app.views.follow'),
    

    url(r'^admin/', include(admin.site.urls)),
)
