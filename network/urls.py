
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("compose", views.compose, name="compose"),

    #API routes
    path("allPost/<int:pageNumber>", views.view_allPosts, name="allPost"),
    path("followings", views.view_followings, name="followings"),
    path("followingPosts/<int:pageNumber>", views.view_following_posts, name="followingPosts"),
    path("profilePage/<str:username>", views.view_profile_page, name="profilePage"),
    path("profilePagePosts/<str:username>/<int:pageNumber>", views.view_profile_page_posts, name="profilePagePosts"),
    path("followOrUnfollow/<str:username>", views.follow_or_unfollow, name="followOrUnfollow"),
    path("doFollowOrUnfollow/<str:selectedUsername>", views.do_follow_or_unfollow, name="doFollowOrUnfollow"), 
    path("getCurrentUser", views.get_Current_User, name="getCurrentUser"),
    path("alreadyLiked/<int:id>", views.alreadyLiked, name="alreadyLiked"),
    path("doLikeOrUnlike/<int:id>", views.doLikeOrUnlike, name="doLikeOrUnlike")
]
