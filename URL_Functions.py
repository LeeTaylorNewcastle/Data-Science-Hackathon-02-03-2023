# Author: Lee Taylor
import requests
from bs4 import BeautifulSoup as BS
from Deprecated.python_.Process_HTML import extract_elements
import re


INTERVAL = 3600
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}


def url_to_soup_obj(url: str) -> BS:
    try:
        page = requests.get(url, headers=HEADERS)
    except requests.exceptions.MissingSchema:
        print(f"\n[WARINING] - <link: {url}> - INVALID!")
        print("LINK DOES NOT CONTAIN PROTOCOL i.e 'https://'")
        return
    return BS(page.content, 'html5lib')


def google_search(search_str: str):
    # Convert search to google search URL
    gsearch_url = f"https://www.google.com/search?q={'+'.join(search_str.lower().split())}"
    # Generate 'soup' object of google search
    gsearch_soup = url_to_soup_obj(gsearch_url)
    # Extract URLs
    elms = extract_elements(str(gsearch_soup), elm='cite')
    # For-loop extracts URLs into list
    urls = []
    for string in elms:
        if string.__contains__("www."):
            urls.append(string.split()[0])
    # Return list of URLs
    return urls


def remove_code(text):
    # Use a regular expression to find any instances of code and scripts
    code = re.findall(r'<.*?>', text)
    # Remove all instances of code and scripts from the text
    clean_text = re.sub(r'<.*?>', '', text)
    # Return the resulting text
    return clean_text


def extract_text(soup, headers=True):
    # Find all HTML elements that contain the main content
    if headers: content_elements = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "a", "li", "span", "strong", "em"])
    elif not headers: content_elements = soup.find_all(["p", "a", "li", "span", "strong", "em"])
    # Concatenate the text from all content elements
    content = [element.text.strip() for element in content_elements]
    for i, v in enumerate(content):
        content[i] = v.replace('\n', '')
        content[i] = content[i].replace('  ', '')
    # Remove keywords
    content = [element for element in content if element.strip() != '']    # Remove blanks
    content = [element for element in content if len(element.split()) > 8] # Remove lines with less than X words
    content = [element for element in content if not element.lower().__contains__('site')]
    content = [element for element in content if not element.lower().__contains__('cookie')]
    content = [element for element in content if not element.lower().__contains__('sign in')]
    content = [element for element in content if not element.lower().__contains__('instagram')]
    content = [element for element in content if not element.lower().__contains__('contact us')]
    print(content)
    # Combine content into a string
    content = '\n'.join(set(content))
    content = remove_code(content)
    print(content)
    # content = [element for element in content if len(element) != '']
    # Return the resulting text
    return content


if __name__ == '__main__':
    # # Url to soup (text)
    # _ = url_to_soup_obj("https://registry.elevategreece.gov.gr/company/i-love-dyslexia-english-language-innovation-eli-ike/")
    #
    # # Write file
    # with open("HTML Files/registry.elevategreece.gov", 'w', encoding='utf-8-sig') as f:
    #     f.write(str(_))

    # Test-case company = 'AkzoNobel'
    urls = google_search(search_str="AkzoNobel")
    print(urls)

    soup1 = url_to_soup_obj(urls[0])
    soup1_text = extract_text(soup1)

    print(soup1_text)
    print('\n'.join(soup1_text))

    # Mark end of if-name-main section
    pass




