from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^data/$', views.grouped_tweet_list, name='tweet_list'),
    url(r'^data/most_retweeted/$', views.most_retweeted, name='most_retweeted'),
    url(r'^data/update/$', views.tweet_update, name='tweet_update'),
    url(r'^$', views.info, name='info')
]