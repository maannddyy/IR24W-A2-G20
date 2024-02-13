import re
from urllib.parse import urlparse, urldefrag
import logging
from bs4 import BeautifulSoup


STOP_WORDS = {"a","about","above","after","again","against","all","am","an","and","any","are","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can't","cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during","each","few","for","from","further","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more","most","mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"}
token_frequencies = dict()  # frequencies of all tokens excluding stop words
longest_page = ["ics.uci.edu", 0]
subdomain_frequencies = dict()  # ics.uci.edu subdomains
visited_urls = set()



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
    
    # TO DO (in order of urgency):
    # - KEEP TRACK OF SUBDOMAINS
    # - Detect redirects and if the page redirects your crawler, index the redirected content
    # - Check for similarities
    # - Detect and avoid crawling very large files, especially if they have low information value
    print(url, resp.status)
    if resp.status != 200:
        return list()
    if resp.url != url:
        print("redirect detected from", url, 'to:', resp.url)
        #redirected content stored? idk if needed to index
        redir_content = resp.raw_response.content


    # redir_resp = detect_redirects(resp.url)
    # if redir_resp is not None:
    #     resp = redir_resp


    soup = BeautifulSoup(resp.raw_response.content, "html.parser")
    content = soup.get_text()

    num_tokens = tokenize(content)

    # checks for longest page
    global longest_page
    if num_tokens > longest_page[1]:
        longest_page = [url, num_tokens]

    #keep track of subdomains
    parsed = urlparse(url)
    parsed_netloc = parsed.netloc.split('.')
    if len(parsed_netloc) > 3 and ".".join(parsed_netloc[-3:]) == "ics.uci.edu":
        subdomain_frequencies[parsed.netloc] = subdomain_frequencies.get(parsed.netloc, 0) + 1

    # subdomain = get_subdomains(defrag_link)
    # subdomain_frequencies[subdomain] = subdomain_frequencies.get(subdomain, 0)+ 1

    # extract links using parsed beautiful soup content
    all_links = [link['href'] for link in soup.find_all('a', href=True)]
    valid_links = list()

    for link in all_links:
        defrag_link = urldefrag(link)[0]
        if defrag_link not in visited_urls and is_valid(defrag_link):
            valid_links.append(defrag_link)
            visited_urls.add(defrag_link)

            
    report()
    return valid_links


def tokenize(content):
    # file = open(file_name, "r")
    # content = file.read()

    tokens = re.findall(r'[a-z0-9]+', content.lower())

    # file.close()
    
    # add tokens to frequencies dict
    frequencies = dict()
    for token in tokens:
        if token not in STOP_WORDS:
            token_frequencies[token] = token_frequencies.get(token, 0) + 1   # records frequencies of tokens of all pages crawled
    
    return len(tokens)

def is_trap():
    pass


def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        # swiki seems to have many pages with no content
        parsed_netloc = parsed.netloc.split('.')
        if len(parsed_netloc) < 3 or ".".join(parsed_netloc[-3:]) not in {"ics.uci.edu", "cs.uci.edu", "informatics.uci.edu", "stat.uci.edu"} or parsed.netloc == "swiki.ics.uci.edu":
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1|ppt|ppsx"
            + r"|thmx|mso|arff|rtf|jar|csv|txt"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise

def get_subdomains(url):
    parsed_url = urlparse(url)
    subdomain_parts = parsed_url.netloc.split('.')
    if len(subdomain_parts) >=3:
        return ".".join(subdomain_parts[-3:])
    return parsed_url.netloc
#must sort too


# def detect_redirects(url):
#     # Detect redirects and if the page redirects your crawler, index the redirected content
#     try:
#         response = requests.get(url, allow_redirects=True)
#         redir_url = response.url
#         if redir_url != url:
#             print("redirect detected to:", redir_url)
#         else:
#             print("no redirects")

#         return response
#     except requests.exceptions.RequestException as e:
#         print("error:", e)
#         return None



def report():

    report = f"LONGEST WORD: {longest_word}\nUNIQUE PAGES: {len(visited_urls)}"
    f = open("report.txt", "w")
    f.write(report)
    f.close()

    subdomains = ""

    for key in sorted(subdomain_frequencies.keys()):
        subdomains += f"{key} {subdomain_frequencies[key]}\n"
    
    f = open("subdomains.txt", "w")
    f.write(subdomains)
    f.close()

    words = ""
    count = 0
    for key, value in sorted(subdomain_frequencies.items, key=lambda x:x[1], reverse=True):
        if count > 50:
            break
        words += f"{key}\n"
        count += 1

    f = open("wordfrequencies.txt", "w")
    f.write(words)
    f.close()

    

if __name__ == "__main__":
    pass