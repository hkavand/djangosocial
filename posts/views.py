from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Post, Like, Comment, User
from .seializers import PostSerializer, LikeSerializer, CommentSerializer, UserSerializer

class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        return Comment.objects.filter(post = self.kwargs['pk'])

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {'pk': self.request.user}
    
    def perform_create(self, serializer):
        serializer.save(author = self.request.user)
        
class PostsOfUser(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_context(self):
        return {'pk': self.request.user}
    
    def get_queryset(self):
        return Post.objects.filter(author = self.kwargs['pk'])
     
class UsersLiked(generics.ListAPIView):
    serializer_class = UserSerializer
    
    def get_queryset(self):
        likes = Like.objects.filter(post = self.kwargs['pk'])
        users = []
        for like in likes:
            users.append(User.objects.get(pk = like.author.pk)) 
        return users
        
class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_context(self):
        return {'pk': self.request.user}
    
    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk = kwargs['pk'], author = self.request.user)
        
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else: 
            raise ValidationError('this post does not belong to you.')
        
class LikeCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk = self.kwargs['pk'])
        return Like.objects.filter(author = user, post = post)
        
    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already liked this post.')
        post = Post.objects.get(pk = self.kwargs['pk'])
        post.likes_count += 1
        post.save()
        serializer.save(author = self.request.user, post = post)
        
    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else: 
            raise ValidationError("you never liked this post")