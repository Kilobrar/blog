from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    numberOfFollowers = models.PositiveIntegerField(default=0)
    numberOfFollowed = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.username}"

    def serialize(self):
        return {
            "username": self.username,
            "followers": self.numberOfFollowers,
            "followed": self.numberOfFollowed
        }

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user}: {self.content}"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "date": self.date,
            "likes": self.likes
        }

class Following(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")
    followed= models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.follower} -> {self.followed}"

    def serialize(self):
        return {
            "follower": self.follower.username,
            "followed": self.followed.username
        }

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liker")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likedPost")

    def __str__(self):
        return f"{self.user} <3 {self.post}"

