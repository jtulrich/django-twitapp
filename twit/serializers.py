from rest_framework import serializers
from .models import Tweet


class TweetSerializer(serializers.Serializer):
    tweet_id = serializers.CharField(read_only=True)
    text = serializers.CharField(required=True, allow_blank=True, max_length=140)
    user_location = serializers.CharField(required=False)
    user_location_longitude = serializers.CharField(required=False)
    user_location_latitude = serializers.CharField(required=False)
    user_lang = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(required=True)
    import_time = serializers.DateTimeField(required=False)

    class Meta:
        ordering = ('created_at',)

    def create(self, validated_data):
        """
        Create and return a new `Tweet` instance, given the validated data.
        """
        return Tweet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Tweet` instance, given the validated data.
        """
        instance.tweet_id = validated_data.get('id', instance.tweet_id)
        instance.text = validated_data.get('text', instance.text)
        instance.user_location = validated_data.get('user_location', instance.user.location)
        instance.user_lang = validated_data.get('user_lang', instance.user_lang)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()
        return instance


class TweetSimpleSerializer(serializers.Serializer):
    tweet_text = serializers.CharField(required=True, allow_blank=True)
    tweet_latitude = serializers.FloatField(required=False)
    tweet_longitude = serializers.FloatField(required=False)
    tweet_date = serializers.DateTimeField(required=True)
    user_screen_name = serializers.CharField(required=True)

    class Meta:
        ordering = ('tweet_date',)

    def create(self, validated_data):
        """
        Create and return a new `TweetSimple` instance, given the validated data.
        """
        return validated_data

    def update(self, instance, validated_data):
        """
        Update and return an existing `TweetSimple` instance, given the validated data. TODO: FAKE BETTER.
        """
        return instance



class TweetGroupSerializer(serializers.Serializer):
    tweet_hour = serializers.DateTimeField(required=True)
    tweet_hour_count = serializers.IntegerField(required=True)
    tweet_user = serializers.CharField(required=True)
    tweet_text = serializers.CharField(required=True, allow_blank=True)
    tweet_latitude = serializers.FloatField(required=False)
    tweet_longitude = serializers.FloatField(required=False)
    tweet_score_type = serializers.CharField(required=True)
    tweet_score = serializers.IntegerField(required=True)

    class Meta:
        ordering = ('tweet_hour',)

    def create(self, validated_data):
        """
        Create and return a new `TweetGroup` instance, given the validated data.
        """
        return validated_data

    def update(self, instance, validated_data):
        """
        Update and return an existing `TweetGroup` instance, given the validated data. TODO: FAKE BETTER.
        """
        return instance
