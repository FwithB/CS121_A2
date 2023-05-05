import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from utils.response import Response
from collections import defaultdict

#before to dig the data, first prepare the tokenize function

#takes a file path as input and returns a set of stopwords. It opens the file, reads it line by line, 
#and adds each non-empty line to a set after removing any leading and trailing whitespaces. This function is essential for preprocessing text in 
#natural language processing tasks, as it allows us to remove common words, such as "the" and "is", 
#which do not provide any meaningful information.

def load_stopwords(file_path):
    stopwords_set = set()
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                stopwords_set.add(line)
    return stopwords_set


# takes a text string and a set of stopwords as input and returns a list of filtered words. 
#It works by first splitting the input text on non-word characters (using regular expressions), 
#converting each word to lowercase, and then checking if it is a valid word
#(i.e., it is not an empty string, is an ASCII string, and is not in the stopwords set). 
#If the word passes these checks, it is added to the list of filtered words.



def tokenize(text, stopwords):
    words = re.split(r"[\W_À-ÖØ-öø-ÿ]+", text)
    filtered_words = []
    for word in words:
        word = word.lower()
        if word and word.isascii() and word not in stopwords:
            filtered_words.append(word)
    return filtered_words

  
    
 #tokenizes the input text and removes stopwords. 
#It first loads the stopwords from the "stop.txt" file using the load_stopwords function 
#and then calls the tokenize function with the text and the set of stopwords as inputs. 
#This function simplifies the process of tokenizing and filtering text by combining these two tasks. 
    
    
def word_tk(text):
    stop = load_stopwords("stop.txt")
    text_words = tokenize(text, stop)
    return text_words
  
  
# start to check the page that contain the longest amount of text


#reads the information about the longest page from a file and returns the URL of that page and the word count. 
#The function reads the file line by line and creates a list of non-empty lines. If the list contains at least two elements, 
#it returns the first element as the URL and the second element as the word count (after converting it to an integer). 
#Otherwise, it returns None and 0.

def read_longest_page(file_path):
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file if line.strip()]

    if len(lines) < 2:
        return None, 0
    else:
        return lines[0], int(lines[1])

 # writes the URL and word count of the longest page to a file.
#It opens the file in write mode and writes the URL on the first line and the word count on the second line.
#This function is useful for keeping track of the longest page found so far in the crawling process.   
    
def write_longest_page(file_path, url, count):
    with open(file_path, "w") as file:
        file.write(f"{url}\n{count}")

        
#that updates the record of the longest page, given a URL and its text. 
#The function first tokenizes the input text using the word_tk function, calculates the token count, 
#and reads the current longest page information from the "longest.txt" file. 
#If the token count is greater than the previous count, 
#the function writes the new URL and token count to the "longest.txt" file, updating the record.        
        
        
def longestPage(url, text):
    tokens = word_tk(text)
    token_count = len(tokens)

    file_path = "longest.txt"
    prev_url, prev_count = read_longest_page(file_path)

    if token_count > prev_count:
        write_longest_page(file_path, url, token_count)

  #that reads word frequencies from a file and returns them as a defaultdict of integer values. 
#The function reads the file line by line and, for each non-empty line, 
#splits it into a word and a count (using regular expressions). 
#It then adds the word and its count (converted to an integer) to the defaultdict.
  
  
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

#writes word frequencies to a file. The function opens the file in write mode and 
#writes each word and its corresponding count on a separate line. 
#This function helps store word frequency data to track the most common words in the crawled web pages.


def write_word_frequencies(file_path, word_frequencies):
    with open(file_path, "w") as file:
        for word, count in word_frequencies.items():
            file.write(f"{word} {count}\n")

            
#updates the list of the 50 most common words in the given text. 
#It reads the word frequencies from the "Com_words.txt" file and tokenizes the input text using the word_tk function. 
#It then iterates through the token list, updating the word frequencies. 
#The function sorts the updated word frequencies first alphabetically and then by count, in descending order.
#Finally, it writes the updated            
            
            
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
#takes a file path as input and returns a list of URLs. 
#It reads the file line by line and appends each non-empty line (after stripping leading and trailing whitespaces) 
#to the list of URLs. This function is essential for processing a list of URLs in the crawling process.


def read_urls(file_path):
    urls = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                urls.append(line)
    return urls


#takes a list of URLs and returns a defaultdict containing the count of subdomains for the "ics.uci.edu" domain. 
#The function iterates over the URLs and parses each URL to extract the subdomain.
#If the URL belongs to the "ics.uci.edu" domain, the function increments the subdomain count in the defaultdict.

def get_subdomain_counts(urls):
    subdomains = defaultdict(int)
    for url in urls:
        parsed_url = urlparse(url)
        hostnames = parsed_url.hostname.split('.')
        subdomain = parsed_url.hostname.split('.')[0]
        if 'ics' in hostnames and 'uci' in hostnames and 'edu' in hostnames:
            full_subdomain = f'https://{subdomain}.ics.uci.edu'
            subdomains[full_subdomain] += 1
    return subdomains


#reads the URLs from the "page_status.txt" file, calculates the subdomain counts using the get_subdomain_counts() function,
#and sorts the subdomain counts in alphabetical and descending order based on their count. 
#This function helps in obtaining a list of unique subdomains and their counts.

def getSub():
    file_path = 'page_status.txt'
    urls = read_urls(file_path)
    subdomains = get_subdomain_counts(urls)

    sorted_subdomains = dict(sorted(subdomains.items(), key=lambda key: key[0]))
    sorted_subdomains = dict(sorted(sorted_subdomains.items(), key=lambda item: item[1], reverse=True))

    return sorted_subdomains
  

# for the total page

#function that takes a file path as input and returns the total number of pages (i.e., lines) in the file.
#The function reads the file line by line, incrementing the total_pages counter for each line.

def count_total_pages(file_path):
    total_pages = 0
    with open(file_path, 'r') as file:
        for line in file:
            total_pages += 1
    return total_pages


#reads the total number of pages from the "page_status.txt" file using the count_total_pages() function.
#This function allows for an easy retrieval of the total number of unique pages encountered during the crawling process.

def get_total_pages():
    file_path = 'page_status.txt'
    total_pages = count_total_pages(file_path)
    return total_pages



#creates a report containing various statistics, such as the total unique pages, longest page, 50 most common words, and unique subdomains. 
def generate_report():
    total_pages = get_total_pages()
    longest_url, longest_count = read_longest_page("longest.txt")
    common_words = read_word_frequencies("Com_words.txt")
    subdomains = getSub()

    with open('report.txt', 'w') as f:
        f.write(f"NO.1 Total Unique Pages: {total_pages}\n")
        f.write(f"NO.2 Longest page: {longest_url}\tWords: {longest_count}\n\n")
        f.write("NO.3  50 most Common Words:\n")
        
        threshold = 50
        for idx, (word, count) in enumerate(common_words.items(), start=1):
            if len(word) <= 1:
                threshold += 1
                continue
            if idx > threshold:
                break
            f.write(f"{word}, {count}\n")
        
        f.write("\nNO.4 Unique subdomains\n")
        for subdomain, count in subdomains.items():
            f.write(f"{subdomain}, {count}\n")
  
  
  
  
  
