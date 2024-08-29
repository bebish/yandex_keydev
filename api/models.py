from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Author(AbstractUser):
    telegram_chat_id = models.CharField(max_length=150, unique=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_author_set',  
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_author_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


class Post(models.Model):
    text = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    average_rating = models.FloatField(default=0)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    post = models.ForeignKey(Post, related_name='ratings', on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
