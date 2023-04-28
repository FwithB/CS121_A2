import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from utils.response import Response
from collections import defaultdict

#before to dig the data, first prepare the tokenize function

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
  
  
# start to check the page that contain the longest amount of text

def read_longest_page(file_path):
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file if line.strip()]

    if len(lines) < 2:
        return None, 0
    else:
        return lines[0], int(lines[1])

    
def write_longest_page(file_path, url, count):
    with open(file_path, "w") as file:
        file.write(f"{url}\n{count}")

        
def longestPage(url, text):
    tokens = word_tk(text)
    token_count = len(tokens)

    file_path = "longest.txt"
    prev_url, prev_count = read_longest_page(file_path)

    if token_count > prev_count:
        write_longest_page(file_path, url, token_count)

  
  
  
  # the following function deal with the 50 common words
    
def read_word_frequencies(file_path):
    word_frequencies = defaultdict(int)
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                word, count = re.split(r"[\W_À-ÖØ-öø-ÿ]+", line)
                word_frequencies[word] = int(count)
    return word_frequencies

def write_word_frequencies(file_path, word_frequencies):
    with open(file_path, "w") as file:
        for word, count in word_frequencies.items():
            file.write(f"{word} {count}\n")

def mostCommon(text):
    file_path = "Com_words.txt"
    words = read_word_frequencies(file_path)

    token_list = word_tk(text)
    for token in token_list:
        words[token] += 1

    sorted_words = dict(sorted(words.items(), key=lambda key: key[0], reverse=True))
    sorted_words = dict(sorted(sorted_words.items(), key=lambda item: item[1], reverse=True))

    write_word_frequencies(file_path, sorted_words)
  
  
  
  
  
  
  
  
  
  
  
