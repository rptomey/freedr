# CS50w Capstone Project - Freedr

## Overview
My final project submission for CS50w is "Freedr", which was named as a portmanteau of "Free Reader". Many people, myself included, have mourned the sunsetting of Google Reader. In the time since, I've looked at other RSS reader options and found them somewhat inscrutable, so I decided this could be an opportunity to build something that I could make use of myself.

Freedr is an RSS reader app with a few goals in mind...

First, I wanted it to be something that I can share with friends without worrying about the maintenance costs. This meant that, while I did include a database, I wanted to be very careful with what kind and how much data I was saving to it. I couldn't very well call it a free RSS reader if I needed to ask people to help me with storage costs.

Second, I wanted users to be able to bookmark articles for reading later. Because I'm not saving every article that comes in until a user marks it as read, there's a possible user experience of seeing something interesting, not having the time to read it, and coming back to find it gone. There are other alternative scenarios that could benefit from bookmarking functionality as well.

Third, I wanted to offer a simple, clean interface that was consistent across desktop and mobile devices. A lot of CSS fiddling went into making something that I was happy with.

Finally, I wanted to ultimately include at least some minor discoverability features. I'm logging every subscribed feed in one of my database tables, which means I can show users the current most popular subscriptions.

## Distinctiveness and Complexity
The requirements for this project can be summarized thusly:
* be distinct from previous projects
* be more advanced than previous projects
* utilize Django (including at least one model) and JavaScript
* be mobile responsive

I believe I have satisified all four of these requirements.

In terms of distinctiveness, this is the first project I've made for the course that actually interacts with other websites. Everything else has been self-contained. Freedr required that I account for XML feeds that passed unexpected or undesirable data. These considerations are visible in decisions like breaking down feed names into acronyms when a character limit was exceeded, setting a maximum size for images included in markup, and supplying default values as a fallback when fields like "Author" didn't get included with a feed entry.

While the Network project did have some similarities in terms of the interface, I made the decision to use a single-column scroll in order to keep the experience consistent across desktop and mobile browsers. I'm pleased with how much the interface looks like other sites that I'm interacting with on a regular basis, and it has less noise than sites with an ulterior advertising motive would include.

In terms of it being advanced, I was able to build on some of the ideas from previous projects. For example, I realized that it would be undesirable for the page to refresh when bookmarking an article in the middle of a feed and leveraged the Fetch API to update the database without negatively impacting the user's experience.

Where I built upon this further was by making my `add_subscription()` function in `views.py` handle multiple types of requests. If it receives a POST request, the it knows the new subscription came from the Manage Subscriptions page and can redirect the user where I want them to go. On the other hand, if it receives a PUT request, it knows the new subscription came from a page for a specific feed, and it handles adding the feed to their subscriptions without redirecting them.

I had to make a few other decisions that I would also argue fit the bill for disctinctiveness and complexity. While I won't run through all of them, I'll highlight how I chose to handle limits for bookmarks. As noted before, one of my goals was to keep the app's overhead in check. I picked a limit of 30 bookmarks based off of what I decided was a reasonable amount of unread posts for a user to save for later.

From there, I had to decide on how to handle additional bookmarks. Rather than refuse to add them, I opted for a first in, first out (FIFO) model where the last added bookmarks will get dropped if the current count is 30 or higher. I also had to make a decision about where to inform the user of this policy and decided an info box on the Bookmarks page made the most sense.

The other requirements were more straightforward. As is evident, I used Django for my backend, and the static file `freedr.js` includes two functions for toggling bookmark status of feed entries and for toggling subscription status of feeds.

In terms of mobile responsiveness, I made sure that the site looks good for different sizes of viewports, and I included a navigation menu that will change to a hamburger menu for smaller browser windows.

## File Explanation
I won't get into every file; however, I will call out noteworthy files here...

`freedr.js` includes two functions for leveraging the Fetch API when adding/removing bookmarks and toggling subscription status for feeds.

`models.py` includes the 4 models that I decided to create: User, Feed, Subscription, Bookmark. User enables the site to save data associated with specific users and lets them log in. Feed is used to aggregate all the RSS feeds that users are following in order to aid with discoverability. Subscription ties together the previous two models. Bookmark allows users to save articles for later.

`utils.py` is used for interacting with and cleaning up the data from RSS feeds.

## How to Run
As a webapp written using Django, Freedr uses the standard `python manage.py runserver` command. Run it once you've opened the code in a command line interface. A `requirements.txt` file has been included to show any other libraries that need to be installed.

Once you have Freedr running on your localhost, open a web browser and create a new user. From there, you should be directed to the Manage Subscriptions page, where you may add new RSS feed URLs to follow. If you need a test case, I suggest `https://www.stereogum.com/feed/`; however, feel free to supply your own. Once you've subscribed to at least one feed, you should be able to return to the homepage and begin reading and/or bookmarking articles.