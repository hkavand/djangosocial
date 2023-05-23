from django.db import models
from django.contrib.auth.models import User

class Post(models.Model): 
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    likes_count = models.PositiveBigIntegerField(default = 0)
    
    class Meta:
        ordering = ['-created_at']
        
class Comment(models.Model): 
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.CharField(max_length = 200)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    parent = models.IntegerField(blank = True, null = True)
    
class Like(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)