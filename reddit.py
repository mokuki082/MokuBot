import requests


def fetch(url):

    """ Fetch a json resources from url and return the object """

    content = requests.get(url)
    return content.json()

class RedditAPI():
    url = ''
