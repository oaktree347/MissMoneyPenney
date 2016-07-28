from chatbot import *
from Legobot import Message

def test_wiki_search():
    msg = Message('!wtf United States')
    assert wiki_search(msg) == 'I found this: https://en.wikipedia.org/wiki/United_States'