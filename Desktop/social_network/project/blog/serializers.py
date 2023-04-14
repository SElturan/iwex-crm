from rest_framework import serializers

from .models import  *


# Users 

class UserRegistrationSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Пароли не совпадают')
        return data

# Post_________________________________________________________________________________________________

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'image', 'created_at', 'updated_at', )


# Comment_____________________________________________________________________________________________

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'content', 'created_at', 'updated_at',)

# Like_____________________________________________________________________________________________


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'author', 'post')
