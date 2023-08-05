import os
import re
import json
import time

DIR_BASE = os.path.dirname(os.path.abspath(__file__))
dir_path = DIR_BASE + "/.app_data"
udata_path = dir_path + "/udata.dat"
ucache_path = dir_path + "/ucache.dat"

regex = re.compile(
    r'^(?:http|ftp)s?://'
)


def checkFiles():
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    if not os.path.exists(udata_path):
        with open(udata_path, 'w') as f:
            f.write('[]')
    if not os.path.exists(ucache_path):
        with open(ucache_path, 'w') as f:
            f.write('[]')


def addLink():
    checkFiles()
    links = getOldLinks()
    link_set = set([x['url'] for x in links])
    link = input('Paste RSS link here: ')
    if re.match(regex, link) is None:
        print("Not a valid url")
        exit()
    title = input('Site-name: ')

    data = {
        'url': link,
        'title': title,
        'time': time.time()
    }
    if data['url'] in link_set:
        print('Already added, exiting')
        exit()
    links.append(data)
    with open(udata_path, 'w') as f:
        json.dump(links, f)


def getOldLinks():
    with open(udata_path, 'r') as f:
        content = f.read()
        data = json.loads(content)
    return data


def listSavedSites():
    sites = getParam('title')
    if len(sites) == 0:
        print('Empty collection. Please update')
        exit()
    for x in sites:
        print(' x ' + x)


def getParam(param):
    checkFiles()
    links_dict = getOldLinks()
    result = []
    for x in links_dict:
        result.append(x[param])
    return result


def updateParam(param, item):
    checkFiles()
    links_dict = getOldLinks()
    if len(links_dict) == 0:
        print('Nothing to update')
        exit()
    valid = []
    for x in links_dict:
        if item != x[param]:
            valid.append(x)
    with open(udata_path, 'w') as f:
        json.dump(valid, f)


def delete_feed():
    listSavedSites()
    item = input('Enter site-name: ')
    updateParam('title', item)


def getProgress():
    checkFiles()
    with open(ucache_path, 'r') as f:
        content = f.read()
        data = json.loads(content)
    return data


def saveProgress(url):
    checkFiles()
    links = getProgress()
    links.extend(url)
    with open(ucache_path, 'w') as f:
        json.dump(list(set(links)), f)


def clear_data():
    choice = input('would you like to clear viewing cache? (y/n): ')
    if choice in ('y', "Y", "yes", "Yes"):
        with open(ucache_path, 'w') as f:
            f.write('[]')

    choice = input('would you like to clear feed sources? (y/n): ')
    if choice in ('y', "Y", "yes", "Yes"):
        with open(udata_path, 'w') as f:
            f.write('[]')
