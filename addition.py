import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from utils.response import Response



def load_stopwords(file_path):
    stopwords_set = set()
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                stopwords_set.add(line)
    return stopwords_set

  
def tokenize(text, stopwords):
    words = re.split(r"[\W_À-ÖØ-öø-ÿ]+", text)
    filtered_words = []
    for word in words:
        word = word.lower()
        if word and word.isascii() and word not in stopwords:
            filtered_words.append(word)
    return filtered_words

  
def word_tk(text):
    stop = load_stopwords("stop.txt")
    text_words = tokenize(text, stop)
    return text_words
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
