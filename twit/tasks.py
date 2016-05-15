from __future__ import absolute_import

from celery import shared_task
from django.conf import settings
from twit.models import Tweet
from datetime import datetime
import requests
import tweepy


@shared_task
def update_tweets():
    updated = 0
    try:
        auth = tweepy.OAuthHandler(settings.TWITTER_API_CONSUMER_KEY, settings.TWITTER_API_CONSUMER_SECRET)
        auth.set_access_token(settings.TWITTER_API_ACCESS_KEY, settings.TWITTER_API_ACCESS_SECRET)

        api = tweepy.API(auth)

        # Get new tweets
        for tweet in tweepy.Cursor(api.search, q="#"+settings.TWITTER_HASHTAG).items():
            if Tweet.objects.filter(tweet_id=tweet.id_str).count() == 0:
                # Create a new Tweet
                new_tweet = Tweet()
                new_tweet.tweet_id = tweet.id_str
                new_tweet.text = tweet.text
                if tweet.coordinates is not None:
                    new_tweet.user_location_longitude = tweet.coordinates[0]
                    new_tweet.user_location_latitude = tweet.coordinates[1]
                new_tweet.favorite_count = tweet.favorite_count
                new_tweet.retweet_count = tweet.retweet_count
                new_tweet.created_at = tweet.created_at
                new_tweet.import_time = datetime.now()
                if tweet.user is not None:
                    new_tweet.user_name = tweet.user.name
                    new_tweet.user_screen_name = tweet.user.screen_name
                    new_tweet.user_location = tweet.user.location
                    if new_tweet.user_location is not None and \
                        (new_tweet.user_location_longitude is None
                         or new_tweet.user_location_latitude is None):
                        temp_coords = get_coords_for_location(new_tweet.user_location)
                        new_tweet.user_location_longitude = temp_coords[0]
                        new_tweet.user_location_latitude = temp_coords[1]
                new_tweet.save()

        # Clean up old tweets
        delete_date = datetime.datetime.now() - datetime.timedelta(days=7)
        Tweet.objects.filter(created_at__lte=delete_date).delete()

        # Set success key
        updated = 1
    except Exception:
        updated = sys.exc_info()[0]
        print("Unexpected error:", sys.exc_info()[0])
    finally:
        return updated


def get_coords_for_location(location):
    request_params = {
        'key': settings.GOOGLE_API_KEY,
        'address': location
    }
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=request_params)
    response_json = response.json()
    if response_json is not None:
        if len(response_json['results']) > 0:
            coords = response_json['results'][0]['geometry']['location']
            return [coords['lng'], coords['lat']]
    return [0,0]