import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

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
    links_list = []
    # check connecting status
    if resp.status != 200:
        return links_list
    # Use beautiful soup to analyze the content of webpages
    content = BeautifulSoup(resp.raw_response.content, 'html.parser')
    #print(content)
    base_url = urljoin(url, content.base.get('href')) if content.base else url
    for link in content.find_all('a'):
        href = link.get('href')
        if href is not None:
            real_link = urljoin(base_url,href)
            links_list.append(real_link)
    return links_list

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
        parsed = urlparse(url)
        domain = parsed.netloc

        domain_allowed = False
        for allowed_domain in allowed_domains:
            if domain.endswith(allowed_domain):
                domain_allowed = True
                break

        if not domain_allowed:
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
            
            
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
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

