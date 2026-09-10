from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('creator', 'Creator'),
        ('audience', 'Audience'),
    ]

    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='audience')

    def __str__(self):
        return self.username

class Comic(models.Model):
    GENRE_CHOICES = [
        ('action', 'Action'),
        ('romance', 'Romance'),
        ('fantasy', 'Fantasy'),
        ('horror', 'Horror'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comics')
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    cover_image = models.ImageField(upload_to='comic_covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ComicPage(models.Model):
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE, related_name='pages')
    image = models.ImageField(upload_to='comic_pages/')
    page_number = models.PositiveIntegerField()

    class Meta:
        ordering = ['page_number']

    def __str__(self):
        return f"{self.comic.title} - Page {self.page_number}"


class Comment(models.Model):
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.comic.title}"

class Like(models.Model):
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comic', 'user')

    def __str__(self):
        return f"{self.user.username} likes {self.comic.title}"
