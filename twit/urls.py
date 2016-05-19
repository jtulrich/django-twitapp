from django.conf.urls import url
from . import views

urlpatterns = [
    # Custom
    url(r'^data/hour/$', views.rest_hourly_tweet_list, name='tweet_list'),
    url(r'^data/day/retweeted/$', views.rest_daily_most_retweeted, name='most_retweeted'),
    url(r'^$', views.info, name='info')
]
