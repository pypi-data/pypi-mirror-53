import queue
import threading
import feedparser
from html.parser import HTMLParser

q = queue.Queue()


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data().strip()


class RSS_parser:
    def __init__(self, url):
        self.url = url
        self.stories = []
        self.init()
        self.pos = 0

    def init(self):
        p = feedparser.parse(self.url)
        for i in range(len(p.entries)):
            self.stories.append(
                {"name": strip_tags(p.entries[i].title), "url": p.entries[i].link, "children": [{"name": strip_tags(p.entries[i].description)}]})

    def preview(self):
        if self.pos > len(self.stories):
            return
        count = 0
        end = len(self.stories) if self.pos + \
            3 > len(self.stories) else self.pos + 3
        for i in range(self.pos, end):
            count += 1
        result = self.stories[self.pos:end]
        self.pos += count
        return result


def get_feeds_from_url(urls):
    for url in urls:
        try:
            q.put(RSS_parser(url))
        except Exception as e:
            exit()


def check_if_empty(all_feeds):
    if len(list(filter(lambda x: x.pos >= len(x.stories), all_feeds))) == len(
        all_feeds
    ):
        return True
    return False
