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

def mostcommon(text):
    file_path = "Com_words.txt"
    words = read_word_frequencies(file_path)

    token_list = word_tk(text)
    for token in token_list:
        words[token] += 1

    sorted_words = dict(sorted(words.items(), key=lambda key: key[0], reverse=True))
    sorted_words = dict(sorted(sorted_words.items(), key=lambda item: item[1], reverse=True))

    write_word_frequencies(file_path, sorted_words)
  
  
  
  
  # for the subdomain

def read_urls(file_path):
    urls = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                urls.append(line)
    return urls

def get_subdomain_counts(urls):
    subdomains = defaultdict(int)
    for url in urls:
        parsed_url = urlparse(url)
        subdomain = parsed_url.hostname.split('.')[0]
        full_subdomain = f'https://{subdomain}.ics.uci.edu'
        subdomains[full_subdomain] += 1
    return subdomains

def getSub():
    file_path = 'page_status.txt'
    urls = read_urls(file_path)
    subdomains = get_subdomain_counts(urls)

    sorted_subdomains = dict(sorted(subdomains.items(), key=lambda key: key[0]))
    sorted_subdomains = dict(sorted(sorted_subdomains.items(), key=lambda item: item[1], reverse=True))

    return sorted_subdomains
  

# for the total page

def count_total_pages(file_path):
    total_pages = 0
    with open(file_path, 'r') as file:
        for line in file:
            total_pages += 1
    return total_pages

def get_total_pages():
    file_path = 'page_status.txt'
    total_pages = count_total_pages(file_path)
    return total_pages


def generate_report():
    total_pages = get_total_pages()
    longest_url, longest_count = read_longest_page("longest.txt")
    common_words = read_word_frequencies("Com_words.txt")
    subdomains = getSub()

    with open('report.txt', 'w') as f:
        f.write(f"NO.1 Total Unique Pages: {total_pages}\n")
        f.write(f"NO.2 Longest page: {longest_url}\tWords: {longest_count}\n\n")
        f.write("NO.3  50 most Common Words:\n")
        
        for idx, (word, count) in enumerate(common_words.items(), start=1):
            if idx > 50:
                break
            f.write(f"{word}, {count}\n")
        
        f.write("\nNO.4 Unique subdomains\n")
        for subdomain, count in subdomains.items():
            f.write(f"{subdomain}, {count}\n")
  
  
  
  
  
