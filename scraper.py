import re
from urllib.parse import urlparse, urlunparse, urljoin, urldefrag
from bs4 import BeautifulSoup
import addition
import simhash as sh


prev_urls = set()
visited_pages = set()
hash_value_set = set()

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]



def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    parsed = urlparse(url)
    clean_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
    parsed_url = urlparse(clean_url)
    links_list = []
    # check connecting status
    if resp.status != 200:
        return links_list
    content = BeautifulSoup(resp.raw_response.content, 'html.parser')
    text = content.getText()
    num_words = len(text.split())
    if num_words < 100:
        return links_list
    
    hash_value = sh.process_hash(text,3)
    for v in hash_value_set:
        if sh.compare(hash_value,v,0.8):
            print('PASS')
            return links_list
        else:
            continue
    hash_value_set.add(hash_value)

    # Load previously visited URLs from a file
    # prev_urls = set()
    # with open("urls.txt", "r") as f:
    #     for line in f:
    #         prev_urls.add(line.strip())
    # f.close()

    # Write visited URL to 'page_status.txt'
    with open('page_status.txt', 'a') as f:
        if parsed_url not in visited_pages:
            f.write(clean_url)
            f.write('\n')
            visited_pages.add(parsed_url)
    f.close()

    # Use beautiful soup to analyze the content of webpages
    #content = BeautifulSoup(resp.raw_response.content, 'html.parser')
    base_url = urljoin(clean_url, content.base.get('href')) if content.base else clean_url
    for link in content.find_all('a'):
        href = link.get('href')
        if href is not None:
            real_link = urlparse(urljoin(base_url, href))
            real_link = urlunparse((real_link.scheme, real_link.netloc, real_link.path, '', '', ''))
            # Check if the link is valid and not visited before
            if is_valid(real_link) and real_link not in prev_urls:
                links_list.append(real_link)
                # Add the link to the previously visited URLs and write it to the file
                prev_urls.add(real_link)
                with open("urls.txt", "a") as f:
                    f.write(real_link + "\n")

    # Get the text from the soup object
    #text = content.getText()

    # Pass the text to mostcommon() and longestPage() functions
    addition.mostcommon(text)
    addition.longestPage(resp.raw_response.url, text)
    
    return links_list

def pattern_recognition(parsed_url):
    path = parsed_url.path
    path_segments = path.split('/')
    for i, segment in enumerate(path_segments[:-1]):
        if segment in path_segments[i + 1:]:
            return True
    return False

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    allowed_domains = [
        "ics.uci.edu",
        "cs.uci.edu",
        "informatics.uci.edu",
        "stat.uci.edu",
    ]

    try:
        parsed_url = urlparse(url)
        clean_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
        parsed = urlparse(clean_url)
        domain = parsed.netloc

        domain_allowed = False
        for allowed_domain in allowed_domains:
            if domain.endswith(allowed_domain):
                domain_allowed = True
                break

        if not domain_allowed:
            return False

        if pattern_recognition(parsed):
            return False

        if parsed.path.endswith((".mpg", ".ppsx", "nb", ".img")):
            return False

        if parsed.scheme not in set(["http", "https"]):
            return False
        
        if parsed.hostname == None:
            return False
        
        if not parsed.hostname.endswith(('ics.uci.edu', 'cs.uci.edu', 'informatics.uci.edu', 'stat.uci.edu')):
            return False 
           
        if parsed.hostname.endswith(('wics.ics.uci.edu')):
            if re.search(r'(/events/|/wics-hosts|/letter-of)', parsed.path.lower()):
                return False
            
        if re.search( 
            r'(/css/|/js/|/bmp/|/gif/|/jpe?g/|/ico/|/events/|/events|/event|/event/|/wics-hosts|/Nanda/|/Nanda|/seminar|/seminar/'
            + r'|/png/|/tiff?/|/mid/|/mp2/|/mp3/|/mp4/|/index.php/|/stayconnected/|/calendar/|/calendar|/letter-of|/computing|/computing/'
            + r'|/wav/|/avi/|/mov/|/mpeg/|/ram/|/m4v/|/mkv/|/ogg/|/ogv/|pdf|/policies/'
            + r'|/ps/|/eps/|/tex/|/ppt/|/pptx/|/ppsx/|/doc/|/docx/|/xls/|/xlsx/|/names/|/wp-'
            + r'|/data/|/dat/|/exe/|/bz2/|/tar/|/msi/|/bin/|/7z/|/psd/|/dmg/|/iso/'
            + r'|/epub/|/dll/|/cnf/|/tgz/|/sha1/'
            + r'|/thmx/|/mso/|/arff/|/rtf/|/jar/|/csv/'
            + r'|/rm/|/smil/|/wmv/|/swf/|/wma/|/zip/|/rar/|/gz/)', parsed.path.lower()):
            return False
        
                    
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico|htm|war"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
