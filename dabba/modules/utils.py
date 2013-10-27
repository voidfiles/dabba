from bunch import Bunch

def json_feed_item(title, description, permalink, image=None, date=None):
    news_item = {
        'title': title,
        'description': description,
        'permalink': permalink,
    }

    if image:
        news_item['image'] = image

    if date:
        news_item['date'] = date

    return Bunch.fromDict(news_item)