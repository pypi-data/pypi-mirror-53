import time
import threading
import urwid
import argparse
import random
from .display import FeedsTreeBrowser
from .utils import *
from .input_mod import *

f = None


def insert_feeds(feeds):
    global q, f
    try:
        all_src = []
        n = len(feeds)
        while n > 0:
            s = q.get(timeout=5)
            done = True if n == 1 else False
            f.init_data(s.preview(), done=done)
            all_src.append(s)
            n -= 1
        q.queue.clear()
    except Exception as e:
        print(e)


def _start():
    global q, f
    # cli
    parser = argparse.ArgumentParser(prog='2feeds')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--add',
                       action='store_true', help='add a new feed')
    group.add_argument('-l', '--list', action='store_true',
                       help='list saved feeds')
    group.add_argument('-r', '--remove', action='store_true',
                       help='remove a feed from your collection')
    args = parser.parse_args()
    cli = False
    if args.add or args.list or args.remove:
        cli = True

    if args.add:
        addLink()
    elif args.list:
        listSavedSites()
    elif args.remove:
        delete_feed()

    if cli:
        exit()

    feeds = getParam('url')
    random.shuffle(feeds)
    feeds = tuple(feeds)
    if len(feeds) == 0:
        print('add some feeds using -a option.')
        exit(-1)

    # get feeds
    request_feeds = threading.Thread(target=get_feeds_from_url, args=(feeds,))
    request_feeds.start()

    # init display
    f = FeedsTreeBrowser()

    # grab feeds from queue
    add_feed = threading.Thread(target=insert_feeds, args=(feeds,))
    add_feed.start()

    # run event loop
    f.main()

    request_feeds.join()
    add_feed.join()


if __name__ == "__main__":
    _start()
