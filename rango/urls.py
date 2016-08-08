from django.conf.urls import patterns, url
from rango import views
from django.contrib.auth.views import password_change, password_change_done

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^about/$', views.about, name='about'),
    url(r'^restricted/$', views.restricted, name='restricted'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^accounts/password_change/$', password_change, {'template_name': 'registration/password_change_form.html'}, name='password_change'),
    url(r'^search/$', views.search, name='search'),
    url(r'^goto/$', views.track_url, name='track_url'),
    url(r'^accounts/password/change/done/$', password_change_done, {'template_name': 'registration/password_change_done.html'}, name='password_change_done'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^like_category/$', views.like_category, name='like_category'),
    url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
)