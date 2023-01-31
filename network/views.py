from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import User, Post, Following, Like


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def view_allPosts(request, pageNumber):
    # Return all posts
    allPost = Post.objects.all().order_by('-date')
    p = Paginator(allPost, 2)
    page = p.page(pageNumber)

    nextExist = page.has_next()

    return JsonResponse([[post.serialize() for post in page.object_list], nextExist], safe=False)


def view_followings(request):
    # Return a list of followed users
    followings = Following.objects.filter(follower=request.user)
    return JsonResponse([following.serialize() for following in followings], safe=False)


def view_following_posts(request, pageNumber):
    followings = Following.objects.filter(follower=request.user).values("followed")
    
    followings = [following["followed"] for following in followings]
    
    posts = Post.objects.filter(user__in=followings)

    p = Paginator(posts,2)
    page = p.page(pageNumber)

    nextExist = page.has_next()

    return JsonResponse([[post.serialize() for post in page.object_list], nextExist], safe=False)


def view_profile_page(request, username):
    # return the selected users profile datas
    selectedUser = User.objects.get(username=username)
    return JsonResponse(selectedUser.serialize())

def view_profile_page_posts(request, username, pageNumber):
    # return the selected user posts
    selectedUser = User.objects.get(username=username)
    selectedUsersPosts = Post.objects.filter(user=selectedUser).order_by("-date")

    p = Paginator(selectedUsersPosts, 2)
    page = p.page(pageNumber)

    nextExist = page.has_next()

    return JsonResponse([[post.serialize() for post in page.object_list], nextExist], safe=False)

# check whether the selected user is followed by the current user
def follow_or_unfollow(request, username):
    selectedUser = User.objects.get(username=username)
    try:
        Following.objects.get(followed=selectedUser, follower=request.user)
        followed = True
    except: followed = False

    return JsonResponse({"followed": followed}, safe=False)

# do following or unfollowing
@login_required
def do_follow_or_unfollow(request, selectedUsername):
    selectedUser = User.objects.get(username=selectedUsername)
    try:
        Following.objects.get(follower=request.user, followed=selectedUser).delete()
        selectedUser.numberOfFollowers -= 1
        request.user.numberOfFollowed -= 1
        follow = "Unfollowed"
    except:
        Following.objects.create(follower=request.user, followed=selectedUser)
        selectedUser.numberOfFollowers += 1
        request.user.numberOfFollowed += 1
        follow = "Followed"
        

    selectedUser.save()
    request.user.save()
    return JsonResponse({"save": follow}, safe=False)
    
def get_Current_User(request):
    return JsonResponse(request.user.serialize())

@csrf_exempt
@login_required
def compose(request):
    print("HAS")
    if request.method == "POST":
        content = request.POST["content"]
        if(content != ""):
            Post.objects.create(user=request.user, content=content)

    return HttpResponseRedirect(reverse("index"))

def alreadyLiked(request, id):
    selectedPost = Post.objects.get(pk=id)

    try:
        Like.objects.get(user=request.user, post=selectedPost)
        liked = True
    except: liked = False

    return JsonResponse({"liked": liked}, safe=False)

@login_required
def doLikeOrUnlike(request, id):
    selectedPost = Post.objects.get(pk=id)

    try:
        Like.objects.get(user=request.user, post=selectedPost).delete()
        selectedPost.likes -= 1
        liked = False
    except:
        Like.objects.create(user=request.user, post=selectedPost)
        selectedPost.likes += 1
        liked = True

    selectedPost.save()
    return JsonResponse({"liked": liked}, safe=False)

@login_required
def deletePost(request, id):
    try:
        postToBeDeleted = Post.objects.get(pk=id)
        postToBeDeleted.delete()
        deleted = True
    except:
        deleted = False

    return JsonResponse({"deleted": deleted}, safe=False)