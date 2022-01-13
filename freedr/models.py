from django.contrib.auth.models import AbstractUser
from django.db import models

# Because this model inherits from AbstractUser,
# it will already have fields for a username, email, password, etc.
class User(AbstractUser):
    def bookmark_count(self):
        return self.bookmarks.count()

    def bookmarked_urls(self):
        bookmark_rows = self.bookmarks.all()
        bookmark_urls = [bookmark.url for bookmark in bookmark_rows]
        return bookmark_urls

    def subscription_count(self):
        return self.subscriptions.count()

    def all_subscriptions(self):
        sub_rows = self.subscriptions.all()
        subs = [sub.feed for sub in sub_rows]
        return subs

# Model for feed details
class Feed(models.Model):
    name = models.CharField(max_length=100)
    feed_url = models.CharField(max_length=500)
    description = models.CharField(max_length=500)

    def subscriber_count(self):
        return self.subscriptions.count()

# Model for keeping track of subscriptions
class Subscription(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.PROTECT, related_name="subscriptions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")

# Model for allowing users to save articles for later
class Bookmark(models.Model):
    feed_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=500)
    description = models.CharField(max_length=1500)
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")