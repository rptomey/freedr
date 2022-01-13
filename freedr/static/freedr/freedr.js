function toggleBookmark(element) {
    if (element.className == 'bookmark-button saved') {
        let storyUrl = '';

        while (element.className != 'feed-entry' && element.tagName != 'BODY') {
            element = element.parentElement;
        }
        
        if (element.className == 'feed-entry') {
            storyUrl = element.querySelector('.entry-link').href;

            fetch('/remove-bookmark', {
                method: 'PUT',
                body: JSON.stringify({
                    link: storyUrl
                })
            })
            .then(() => {
                element.querySelector('.bookmark-button').className = 'bookmark-button unsaved';
            });
        }
    }
    else if (element.className == 'bookmark-button unsaved') {
        let feedName = '';
        let headline = '';
        let storyUrl = '';
        let storyDescription = '';

        while (element.className != 'feed-entry' && element.tagName != 'BODY') {
            element = element.parentElement;
        }

        if (element.className == 'feed-entry') {
            feedName = element.querySelector('.entry-publication span').textContent;
            headline = element.querySelector('.entry-link').textContent;
            storyUrl = element.querySelector('.entry-link').href;
            storyDescription = element.querySelector('.entry-description').innerHTML;

            fetch('/add-bookmark', {
                method: 'PUT',
                body: JSON.stringify({
                    publication: feedName,
                    title: headline,
                    link: storyUrl,
                    description: storyDescription
                })
            })
            .then(() => {
                element.querySelector('.bookmark-button').className = 'bookmark-button saved';
            });
        }
    }
    else {
        console.log('something is wrong');
    }
}

function toggleSubscribeFromFeed(element) {
    button = element;

    while (element.className != 'feed-details' && element.tagName != 'BODY') {
        element = element.parentElement;
    }

    if (element.className == 'feed-details' && button.className.includes('feed-subscribe-button')) {
        feedUrl = element.querySelector('.feed-url').textContent;
        
        fetch('/subscribe', {
            method: 'PUT',
            body: JSON.stringify({
                url: feedUrl
            })
        })
        .then(() => {
            button.className = 'btn btn-danger feed-unsubscribe-button';
            button.innerHTML = 'Unsubscribe';
        });
    }
    else if (element.className == 'feed-details' && button.className.includes('feed-unsubscribe-button')) {
        feedId = element.dataset.feedId;

        fetch(`/unsubscribe/${feedId}`, {
            method: 'PUT'
        })
        .then(() => {
            button.className = 'btn btn-light feed-subscribe-button';
            button.innerHTML = 'Subscribe';
        })
    }
    else {
        console.log('something is wrong');
    }
}