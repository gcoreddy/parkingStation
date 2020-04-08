from parking import views
from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url('^$', views.getQuery, name='getQuery'),
    url(r'^admin/',admin.site.urls),
]