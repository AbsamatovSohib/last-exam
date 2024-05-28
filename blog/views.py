from rest_framework import generics
from django.utils.timezone import now, timedelta
from .models import Post, Category, Comment

from . import serializers


class PostListAPI(generics.ListAPIView):
    queryset = Post.is_main.all()
    serializer_class = serializers.PostSerializer


class ViewedPostsAPI(generics.ListAPIView):
    queryset = Post.is_main.order_by('-views')[:10]
    serializer_class = serializers.PostSerializer


class WeeklyPostsAPI(generics.ListAPIView):
    queryset = Post.is_main.filter(created_at__gt=now() - timedelta(days=7))
    serializer_class = serializers.PostSerializer


class MonthlyPostsAPI(generics.ListAPIView):
    queryset = Post.is_main.filter(created_at__gt=now() - timedelta(days=30))
    serializer_class = serializers.PostSerializer


class RecommendedPostsAPI(generics.ListAPIView):
    queryset = Post.is_main.filter(is_recommended=True)
    serializer_class = serializers.PostSerializer


class PostDetailAPI(generics.RetrieveAPIView):
    queryset = Post.is_main.all()
    serializer_class = serializers.PostSerializer

    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj


class PostCreateAPI(generics.CreateAPIView):
    serializer_class = serializers.PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostUpdateAPI(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Post.is_main.all()
    serializer_class = serializers.PostCreateSerializer


class PostCommentsAPI(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post_slug = self.kwargs.get('post_slug')
        return super().get_queryset().filter(post__id=post_id, post__slug=post_slug)


class CommentCreateAPI(generics.CreateAPIView):
    serializer_class = serializers.CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
