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
    def __init__(self, url, progress):
        self.url = url
        self.stories = []
        self.init(progress)
        self.pos = 0

    def __len__(self):
        return len(self.stories)

    def init(self, progress):
        p = feedparser.parse(self.url)
        exception = p.get('bozo_exception', None)
        if exception is not None:
            exit(-1)  # exit if no internet connection; no attempt to reconnect
        for i in range(len(p.entries)):
            url = p.entries[i].link
            if url not in progress:
                self.stories.append(
                    {"name": strip_tags(p.entries[i].title), "url": url, "children": [{"name": strip_tags(p.entries[i].description)}]})

    def preview(self):
        # added return
        if self.pos > len(self.stories):
            return None
        count = 0
        end = len(self.stories) if self.pos + \
            3 > len(self.stories) else self.pos + 3
        for i in range(self.pos, end):
            count += 1
        result = self.stories[self.pos:end]
        self.pos += count
        return result

# add dependency ?


def get_feeds_from_url(urls, progress):
    for url in urls:
        try:
            r = RSS_parser(url, progress)
            if len(r) == 0:
                continue
            q.put(r)
        except Exception as e:
            pass  # is it okay to pass ?


def check_if_empty(all_feeds):
    if len(list(filter(lambda x: x.pos >= len(x.stories), all_feeds))) == len(
        all_feeds
    ):
        return True
    return False
