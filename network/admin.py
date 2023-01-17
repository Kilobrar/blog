from django.contrib import admin

from .models import Following, Post, User, Like

# Register your models here.
admin.site.register(User)
admin.site.register(Following)
admin.site.register(Post)
admin.site.register(Like)
