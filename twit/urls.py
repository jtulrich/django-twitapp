from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'/data/^$', views.tweet_list, name='tweet_list'),
    url(r'^$', views.test, name='test')
]