from django.db import models
from django.utils import timezone


class Tweet(models.Model):
    tweet_id = models.TextField(null=True)
    text = models.CharField(null=True, max_length=140)
    user_location = models.TextField(null=True)
    user_location_latitude = models.FloatField(null=True)
    user_location_longitude = models.FloatField(null=True)
    user_lang = models.TextField(null=True)
    created_at = models.DateTimeField(null=True, db_index=True)
    import_time = models.DateTimeField(null=True, default=timezone.now)

    def __str__(self):
        return self.text

    def __init__(self):
        if self.user_location is not None:
            self.get_coordinates_for_user_location()

    def get_coordinates_for_user_location(self):
        # TODO: Complete this function
        self.user_location_latitude = -90
        self.user_location_longitude = -180
