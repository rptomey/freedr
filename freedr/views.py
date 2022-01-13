from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseForbidden
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Feed, Subscription, Bookmark
from .utils import pull_feed_details, pull_feed

import json
import logging

# Create your views here.

def index(request):
    user = request.user
    if user.is_authenticated and user.subscription_count() >= 1:
        subs = Subscription.objects.filter(user=user)
        all_entries = []

        for sub in subs:
            entries = pull_feed(sub.feed.feed_url)
            all_entries.extend(entries)

        all_entries_sorted = sorted(all_entries, key=lambda row: row["published"], reverse=True)

        paginator = Paginator(all_entries_sorted, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "freedr/index.html", {
            "page_obj": page_obj
        })
    elif user.is_authenticated:
        return redirect("manage_subs")
    else:
        return redirect("login")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "freedr/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "freedr/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "freedr/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "freedr/register.html", {
                "message": "Username already taken."
            })
        
        # Assuming no exception, login and send to index
        login(request, user)
        return redirect("index")
    else:
        return render(request, "freedr/register.html")

@login_required
def manage_subscriptions(request):
    top_feeds = Feed.objects.all().order_by("-subscriptions")[:10]
    return render(request, "freedr/subscriptions.html", {
        "top_feeds": top_feeds
    })

@csrf_exempt
@login_required
def add_subscription(request):
    if request.method == "POST":
        user = request.user
        url = request.POST["url"]
        
        if not Feed.objects.filter(feed_url=url).exists():
            feed_details = pull_feed_details(url)
            title = feed_details.title if feed_details.has_key("title") else "publication name missing"
            description = feed_details.description if feed_details.has_key("description") else "publication description missing"

            try:
                new_feed = Feed(
                    name = title,
                    feed_url = url,
                    description = description
                )
                new_feed.save()
            except:
                logging.exception("message")
                return redirect("index")
        
        feed = Feed.objects.get(feed_url=url)

        if not Subscription.objects.filter(user=user, feed=feed).exists():
            try:
                new_sub = Subscription(
                    feed = feed,
                    user = user
                )
                new_sub.save()
            except:
                logging.exception("message")

        return redirect("feed", id=feed.id)
    
    if request.method == "PUT":
        user = request.user
        data = json.loads(request.body)
        url = data.get("url")

        if not url.endswith("/"):
            url = url + "/"

        if not Feed.objects.filter(feed_url=url).exists():
            feed_details = pull_feed_details(url)
            title = feed_details.title if feed_details.has_key("title") else "publication name missing"
            description = feed_details.description if feed_details.has_key("description") else "publication description missing"

            try:
                new_feed = Feed(
                    name = title,
                    feed_url = url,
                    description = description
                )
                new_feed.save()
            except:
                logging.exception("message")
                return redirect("index")
        
        feed = Feed.objects.get(feed_url=url)

        if not Subscription.objects.filter(user=user, feed=feed).exists():
            try:
                new_sub = Subscription(
                    feed = feed,
                    user = user
                )
                new_sub.save()
            except:
                logging.exception("message")

        return JsonResponse({"message": "Subscribed to feed"})

@csrf_exempt
@login_required
def unsubscribe(request, id):
    if request.method == "GET":
        user = request.user
        feed = Feed.objects.get(id=id)

        try:
            Subscription.objects.get(user=user, feed=feed).delete()
        except:
            logging.exception("message")

        return redirect("manage_subs")
    
    if request.method == "PUT":
        user = request.user
        feed = Feed.objects.get(id=id)

        try:
            Subscription.objects.get(user=user, feed=feed).delete()
        except:
            logging.exception("message")

        return JsonResponse({"message": "Unsubscribed from feed"})
            
def view_feed(request, id):
    feed = Feed.objects.get(id=id)
    entries = pull_feed(feed.feed_url)
    
    paginator = Paginator(entries, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "freedr/feed.html", {
        "feed": feed,
        "page_obj": page_obj
    })

@csrf_exempt
@login_required
def save_entry(request):
    if request.method == "PUT":
        user = request.user
        data = json.loads(request.body)
        feed_name = data.get("publication")
        title = data.get("title")
        url = data.get("link")
        description = data.get("description")

        if Bookmark.objects.filter(user=user).count() >= 30:
            Bookmark.objects.filter(user=user).order_by("date_added").first().delete()

        try:
            new_bookmark = Bookmark(
                feed_name = feed_name,
                title = title,
                url = url,
                description = description,
                user = user
            )
            new_bookmark.save()
        except:
            logging.exception("message")

        return JsonResponse({"message": "Added to bookmarks"})

@csrf_exempt
@login_required
def delete_entry(request):
    if request.method == "PUT":
        user = request.user
        data = json.loads(request.body)
        url = data.get("link")

        try:
            Bookmark.objects.get(user=user, url=url).delete()
            return JsonResponse({"message": "Removed from bookmarks"})
        except:
            return HttpResponseForbidden({"message": "Bookmark not found"})

@login_required
def view_bookmarks(request):
    user = request.user
    bookmarks = Bookmark.objects.filter(user=user)
    
    paginator = Paginator(bookmarks, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "freedr/bookmarks.html", {
        "page_obj": page_obj
    })

# TODO: Polish CSS on feed sub unsub buttons