from django.contrib import admin

from .models import User, Feed, Subscription, Bookmark

# Register your models here.
admin.site.register(User)
admin.site.register(Feed)
admin.site.register(Subscription)
admin.site.register(Bookmark)