from rest_framework import serializers
from .models import Author, Post, Comment, Rating

class AuthorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Author
        fields = ['username', 'email', 'telegram_chat_id', 'password']

    def create(self, validated_data):
        user = Author(
            username=validated_data['username'],
            email=validated_data['email'],
            telegram_chat_id=validated_data['telegram_chat_id']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'text', 'publication_date', 'author', 'average_rating']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'text', 'publication_date']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'post', 'author', 'value']
