from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("subscribe", views.add_subscription, name="subscribe"),
    path("unsubscribe/<str:id>", views.unsubscribe, name="unsubscribe"),
    path("feed/<str:id>", views.view_feed, name="feed"),
    path("add-bookmark", views.save_entry, name="add_bookmark"),
    path("remove-bookmark", views.delete_entry, name="remove_bookmark"),
    path("manage-subscriptions", views.manage_subscriptions, name="manage_subs"),
    path("bookmarks", views.view_bookmarks, name="bookmarks")
]
