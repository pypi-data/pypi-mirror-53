import requests


def provide():
    return requests.get('https://www.cs.cmu.edu/~biglou/resources/bad-words.txt').text.splitlines()
