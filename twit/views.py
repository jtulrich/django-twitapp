from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
from twit.models import Tweet
from twit.serializers import TweetSimpleSerializer, TweetGroupSerializer
from django.shortcuts import render
from .tasks import update_tweets


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def rest_daily_most_retweeted(request):
    """
    Get the most retweeted tweet for each day of data.
    """
    if request.method == 'GET':
        tweets = Tweet.objects.raw("SELECT * FROM GetMostRetweetedTweetByDay()")
        tweets_serial = TweetSimpleSerializer(tweets, many=True)
        return JSONResponse(tweets_serial.data)


@csrf_exempt
def rest_hourly_tweet_list(request):
    """
    Gets a list of all tweets grouped by hour with the most retweeted.
    """
    if request.method == 'GET':
        tweets = Tweet.objects.raw("SELECT * FROM GetTweetsGroupedByHourWithHighestValues()")
        tweets_serial = TweetGroupSerializer(tweets, many=True)
        return JSONResponse(tweets_serial.data)


def info(request):
    return render(request, 'twit/dashboard.html', {})
