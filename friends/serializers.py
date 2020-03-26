from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from friends.models import Friend

class FriendSerializer(serializers.HyperlinkedModelSerializer):
    '''
    This serializer should only be used for actions taken by the internal program of the server.
    Do NOT pass the user's data DIRECTLY into this serializer, since this serializer has neither 
    read_only_fields nor any advanced validator.
    '''
    class Meta:
        model = Friend
        fields = ('id', 'followee', 'follower', 'mutual', 'not_read')

        validators = [
            UniqueTogetherValidator(
                queryset=Friend.objects.all(),
                fields=['followee', 'follower']
            )
        ]

    def validate(self, data):
        """
        If "followee" and "follower" fields are provided (may not be provided if action is update), 
        enforce followee field and follower field have different values.
        """
        if 'followee' in data.keys() and 'follower' in data.keys() and data['followee'] == data['follower']:
            raise serializers.ValidationError("followee and follower should not be same")
        return data

    # def create(self, validated_data):
    #     print(validated_data)
    #     return Friend(**validated_data)

class FriendReadOnlySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Friend
        fields = ('id', 'followee', 'follower', 'mutual', 'not_read')
        read_only_fields = ('followee', 'follower', 'mutual', 'not_read')

class FriendfollowerSerializer(serializers.HyperlinkedModelSerializer):
    '''
    This serializer should only be used to create a new friendship event by the follower.
    Do NOT use this serializer for update.
    '''
    class Meta:
        model = Friend
        fields = ('id', 'followee', 'follower', 'mutual', 'not_read')
        read_only_fields = ('mutual', 'not_read')

        validators = [
            UniqueTogetherValidator(
                queryset=Friend.objects.all(),
                fields=['followee', 'follower']
            )
        ]

    def validate(self, data):
        """
        enforce followee field and follower field have different values
        """
        if data['followee'] == data['follower']:
            raise serializers.ValidationError("followee and follower should not be same")
        return data