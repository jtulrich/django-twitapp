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
