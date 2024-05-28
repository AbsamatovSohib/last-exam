from rest_framework import serializers
from . import models


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Post

        fields = ('id', 'slug', 'title', 'category', 'author', 'image',
                  'content', 'views', 'created_at', 'updated_at', 'recommended',
                  'is_published',
        )


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Post
        fields = (
            'title',  'content', 'image',
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ('post', 'owner', 'content', 'created_at', 'updated_at'
        )


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ('post', 'content',)
