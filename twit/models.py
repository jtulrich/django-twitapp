from django.db import models
from django.utils import timezone


class Tweet(models.Model):
    tweet_id = models.TextField(null=True)
    text = models.CharField(null=True, max_length=140)
    favorite_count = models.IntegerField(null=True)
    retweet_count = models.IntegerField(null=True)
    user_name = models.TextField(null=True)
    user_screen_name = models.TextField(null=True)
    user_location = models.TextField(null=True)
    user_location_latitude = models.FloatField(null=True)
    user_location_longitude = models.FloatField(null=True)
    created_at = models.DateTimeField(null=True, db_index=True)
    import_time = models.DateTimeField(null=True, default=timezone.now)

    def __str__(self):
        return self.text