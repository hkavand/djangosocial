from django.http import JsonResponse
from rest_framework import serializers
from .models import Post, Comment, Like, User

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source = 'author.username')
    likes_count = serializers.ReadOnlyField()
    is_liked_by_current_user = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at', 'likes_count', 'is_liked_by_current_user', 'comments']
        
    def get_is_liked_by_current_user(self, post):
        if Like.objects.filter(post = post, author = self.context['pk']):
            return True
        else: return False
        
    def get_comments(self, post):
        coms = Comment.objects.filter(post = post, parent__isnull = True)
        cs = CommentSerializer(coms, many = True)
        return cs.data
                
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id']
        
class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    author = serializers.ReadOnlyField(source = 'author.username')
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at', 'post', 'parent', 'replies']
    
    def get_replies(self, comment):
        replies = Comment.objects.filter(post = comment.post, parent = comment.pk)
        cs = CommentSerializer(replies, many = True)
        return cs.data
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
