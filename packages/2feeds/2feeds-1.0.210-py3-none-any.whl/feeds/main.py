import time
import threading
import urwid
import argparse
import random
from feeds.display import FeedsTreeBrowser
from feeds.utils import *
from feeds.input_mod import *

f = None


def insert_feeds(feeds):
    global q, f
    try:
        all_src = []
        while True:
            s = q.get(timeout=7)
            content = s.preview()
            all_src.append(s)
            # added new check for None
            if content is None:
                continue
            f.init_data(content)
        q.queue.clear()
    except Exception as e:
        pass
    finally:
        f.done = True


def _start():
    global q, f, progress
    # cli
    parser = argparse.ArgumentParser(prog='2feeds')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--add',
                       action='store_true', help='add a new feed')
    group.add_argument('-l', '--list', action='store_true',
                       help='list saved feeds')
    group.add_argument('-r', '--remove', action='store_true',
                       help='remove a feed from your collection')
    group.add_argument('-c', '--clear', action='store_true',
                       help='clear feed collection and/or clear viewing cache')
    args = parser.parse_args()
    cli = False
    if args.add or args.list or args.remove or args.clear:
        cli = True

    if args.add:
        addLink()
    elif args.list:
        listSavedSites()
    elif args.remove:
        delete_feed()
    elif args.clear:
        clear_data()

    if cli:
        exit()

    feeds = getParam('url')
    random.shuffle(feeds)
    feeds = tuple(feeds)
    if len(feeds) == 0:
        print('add some feeds using -a option.')
        exit(-1)

    # get feeds
    progress = set(getProgress())
    request_feeds = threading.Thread(
        target=get_feeds_from_url, args=(feeds, progress,))
    request_feeds.start()

    # init display
    f = FeedsTreeBrowser()

    # grab feeds from queue
    add_feed = threading.Thread(target=insert_feeds, args=(feeds,))
    add_feed.start()

    # run event loop
    links = f.main()
    if links != []:
        saveProgress(links)

    request_feeds.join()
    add_feed.join()


if __name__ == "__main__":
    _start()
