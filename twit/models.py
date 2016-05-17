from django.db import models
from django.utils import timezone


class Tweet(models.Model):
    tweet_id = models.TextField(null=True)
    text = models.TextField(null=True)
    favorite_count = models.IntegerField(null=True)
    retweet_count = models.IntegerField(null=True)
    retweet_original = models.BooleanField(null=False, default=False)
    user_name = models.TextField(null=True)
    user_screen_name = models.TextField(null=True)
    user_location = models.TextField(null=True)
    user_location_latitude = models.FloatField(null=True)
    user_location_longitude = models.FloatField(null=True)
    created_at = models.DateTimeField(null=True, db_index=True)
    import_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.text


class GeocodeLog(models.Model):
    run_date = models.DateTimeField(null=False)
    run_count = models.IntegerField(null=False)

    def __str__(self):
        return str(self.run_date) + ": " + str(self.run_count)