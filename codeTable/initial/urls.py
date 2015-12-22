from django.conf.urls import url

from . import views

app_name = 'initial'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^submitCode', views.submitCode, name='submitCode'),
]