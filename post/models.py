from django.db import models
from django.conf import settings

#스택 테이블 별도로   
class TechStack(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

#게시물 
class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='post_image/', blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    tech_stacks = models.ManyToManyField(TechStack, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_posts',
        blank=True    
    )

    def __str__(self):
        return self.title
    
    def like_count(self):
        return self.likes.count()
#댓글
class Comment(models.Model):
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments'
        )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
        )
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_comments',
        blank=True 
    )

    def __str__(self):
        return self.content[:20]
    
    def like_count(self):
        return self.likes.count()
