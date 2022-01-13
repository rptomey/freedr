from email.utils import parsedate_to_datetime
from .models import Feed

import feedparser
import re

def pull_feed_details(feed_url):
    feed = feedparser.parse(feed_url)
    feed_details = feed.feed
    return feed_details

def pull_feed(feed_url):
    feed_obj = Feed.objects.get(feed_url=feed_url)
    feed_id = feed_obj.id

    feed = feedparser.parse(feed_url)
    feed_title = feed.feed.title if feed.feed.has_key("title") else "Publication Unknown"
    concise_feed_title = feed_title if len(feed_title) <= 15 else re.sub('[^A-Z\-:]','', feed_title)
    feed_entries = feed.entries
    feed_dictionaries = []

    for entry in feed_entries:
        dictionary = {
            "publication": feed_title,
            "publication_concise": concise_feed_title,
            "feed_id": feed_id,
            "title": entry.title if entry.has_key("title") else "Headline",
            "link": entry.link if entry.has_key("link") else feed_url,
            "author": entry.author if entry.has_key("author") else "Anonymous",
            "published": parsedate_to_datetime(entry.published) if entry.has_key("published") else "Unknown Date/Time",
            "description": entry.description if entry.has_key("description") else "No preview available."
        }
        feed_dictionaries.append(dictionary)
    
    return feed_dictionaries