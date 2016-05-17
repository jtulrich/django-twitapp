from __future__ import absolute_import

from celery import shared_task
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models import Sum
from django.utils import timezone
from twit.models import Tweet, GeocodeLog
import requests
import sys
import tweepy
import pytz


@shared_task
def update_tweets():
    updated = 0
    try:
        auth = tweepy.OAuthHandler(settings.TWITTER_API_CONSUMER_KEY, settings.TWITTER_API_CONSUMER_SECRET)
        auth.set_access_token(settings.TWITTER_API_ACCESS_KEY, settings.TWITTER_API_ACCESS_SECRET)

        api = tweepy.API(auth)

        # Get Google Geocode Limits
        today = timezone.now()
        geocode_count = GeocodeLog.objects.filter(run_date__year=today.year,
                                                  run_date__month=today.month,
                                                  run_date__day=today.day).aggregate(Sum('run_count'))
        geocode_count = geocode_count['run_count__sum']
        if geocode_count is None:
            geocode_count = 0

        # Get Twitter Old Tweet Limits
        old_tweet_limit = 5
        old_tweet_count = 0

        # Get new tweets
        for tweet in tweepy.Cursor(api.search, q="#"+settings.TWITTER_HASHTAG).items():
            try:
                if Tweet.objects.filter(tweet_id=tweet.id_str).count() == 0:
                    # Create a new Tweet
                    new_tweet = Tweet()
                    new_tweet.tweet_id = tweet.id_str
                    new_tweet.text = tweet.text
                    if tweet.coordinates is not None:
                        new_tweet.user_location_longitude = tweet.coordinates['coordinates'][0]
                        new_tweet.user_location_latitude = tweet.coordinates['coordinates'][1]
                    new_tweet.favorite_count = tweet.favorite_count
                    new_tweet.retweet_count = tweet.retweet_count
                    new_tweet.retweet_original = False
                    if new_tweet.retweet_count > 0 and not hasattr(tweet, "retweeted_status"):
                        new_tweet.retweet_original = True
                    new_tweet.created_at = pytz.timezone('UTC').localize(tweet.created_at)
                    new_tweet.import_time = today
                    if tweet.user is not None:
                        new_tweet.user_name = tweet.user.name
                        new_tweet.user_screen_name = tweet.user.screen_name
                        new_tweet.user_location = tweet.user.location
                        if new_tweet.user_location is not None and \
                                (new_tweet.user_location_longitude is None or
                                    new_tweet.user_location_latitude is None):
                            temp_coordinates = get_coords_for_location(new_tweet.user_location, geocode_count)
                            if temp_coordinates != [-180, -180]:
                                new_tweet.user_location_longitude = temp_coordinates[0]
                                new_tweet.user_location_latitude = temp_coordinates[1]
                            geocode_count += 1
                    new_tweet.save()
                else:
                    # Check a few back, but stop trying to get tweets when we're hitting old ones
                    old_tweet_count += 1
                    if old_tweet_count >= old_tweet_limit:
                        break
            except Exception:
                print("Tweet Import error: ", sys.exc_info()[0])

        # Clean up old tweets
        delete_date = today - timedelta(days=7)
        Tweet.objects.filter(created_at__lte=delete_date).delete()

        # Geocode old tweets if there is time
        if geocode_count < settings.GOOGLE_GEOCODING_LIMIT:
            lost_tweets = Tweet.objects.filter(user_location_latitude__isnull=1, user_location_longitude__isnull=1)
            for lost_tweet in lost_tweets:
                temp_coordinates = get_coords_for_location(lost_tweet.user_location, geocode_count)
                if temp_coordinates != [-180, -180]:
                    new_tweet.user_location_longitude = temp_coordinates[0]
                    new_tweet.user_location_latitude = temp_coordinates[1]
                geocode_count += 1

        # Make GeocodeLog for run
        new_geocode = GeocodeLog()
        new_geocode.run_count = geocode_count
        new_geocode.run_date = today
        new_geocode.save()

        # Set success key
        updated = 1
    except Exception:
        updated = 0
        print("Unexpected error: ", sys.exc_info()[0])
    finally:
        return updated


def get_coords_for_location(location, geocode_count):
    # Make sure we don't exceed the Google Geocode Limit too much
    if geocode_count >= settings.GOOGLE_GEOCODING_LIMIT:
        return [-180, -180]

    try:
        request_params = {
            'key': settings.GOOGLE_API_KEY,
            'address': location
        }
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=request_params)
        response_json = response.json()
        if response_json is not None:
            if len(response_json['results']) > 0:
                coordinates = response_json['results'][0]['geometry']['location']
                return [coordinates['lng'], coordinates['lat']]
    except Exception:
        print("Unable to geocode: ", sys.exc_info()[0])
    finally:
        return [0, 0]