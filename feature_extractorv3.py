
import math
import content_features as ctnfe
import url_features as urlfe
import external_features as trdfe
import pandas as pd 
import urllib.parse
import tldextract
import requests
import json
import csv
import os
import re
from bs4 import BeautifulSoup

def is_URL_accessible(url):
    #iurl = url
    #parsed = urlparse(url)
    #url = parsed.scheme+'://'+parsed.netloc
    page = None
    try:
        page = requests.get(url, timeout=5)   
    except:
        parsed = urllib.parse.urlparse(url)
        url = parsed.scheme+'://'+parsed.netloc
        if not parsed.netloc.startswith('www'):
            url = parsed.scheme+'://www.'+parsed.netloc
            try:
                page = requests.get(url, timeout=5)
            except:
                page = None
                pass
        # if not parsed.netloc.startswith('www'):
        #     url = parsed.scheme+'://www.'+parsed.netloc
        #     #iurl = iurl.replace('https://', 'https://www.')
        #     try:
        #         page = requests.get(url)
        #     except:        
        #         # url = 'http://'+parsed.netloc
        #         # iurl = iurl.replace('https://', 'http://')
        #         # try:
        #         #     page = requests.get(url) 
        #         # except:
        #         #     if not parsed.netloc.startswith('www'):
        #         #         url = parsed.scheme+'://www.'+parsed.netloc
        #         #         iurl = iurl.replace('http://', 'http://www.')
        #         #         try:
        #         #             page = requests.get(url)
        #         #         except:
        #         #             pass
        #         pass 
    if page and page.status_code == 200 and page.content not in ["b''", "b' '"]:
        return True, url, page
    else:
        return False, None, None

def get_domain(url):
    o = urllib.parse.urlsplit(url)
    return o.hostname, tldextract.extract(url).domain, o.path


def getPageContent(url):
    parsed = urllib.parse.urlparse(url)
    url = parsed.scheme+'://'+parsed.netloc
    try:
        page = requests.get(url)
    except:
        if not parsed.netloc.startswith('www'):
            url = parsed.scheme+'://www.'+parsed.netloc
            page = requests.get(url)
    if page.status_code != 200:
        return None, None
    else:    
        return url, page.content
 
    
    
#################################################################################################################################
#              Data Extraction Process
#################################################################################################################################

def extract_data_from_URL(hostname, content, domain, Href, Link, Anchor, Media, Form, CSS, Favicon, IFrame, Title, Text):
    Null_format = ["", "#", "#nothing", "#doesnotexist", "#null", "#void", "#whatever",
               "#content", "javascript::void(0)", "javascript::void(0);", "javascript::;", "javascript"]

    soup = BeautifulSoup(content, 'html.parser', from_encoding='iso-8859-1')

    # collect all external and internal hrefs from url
    for href in soup.find_all('a', href=True):
        dots = [x.start(0) for x in re.finditer('\.', href['href'])]
        if hostname in href['href'] or domain in href['href'] or len(dots) == 1 or not href['href'].startswith('http'):
            if "#" in href['href'] or "javascript" in href['href'].lower() or "mailto" in href['href'].lower():
                 Anchor['unsafe'].append(href['href']) 
            if not href['href'].startswith('http'):
                if not href['href'].startswith('/'):
                    Href['internals'].append(hostname+'/'+href['href']) 
                elif href['href'] in Null_format:
                    Href['null'].append(href['href'])  
                else:
                    Href['internals'].append(hostname+href['href'])   
        else:
            Href['externals'].append(href['href'])
            Anchor['safe'].append(href['href'])

    # collect all media src tags
    for img in soup.find_all('img', src=True):
        dots = [x.start(0) for x in re.finditer('\.', img['src'])]
        if hostname in img['src'] or domain in img['src'] or len(dots) == 1 or not img['src'].startswith('http'):
            if not img['src'].startswith('http'):
                if not img['src'].startswith('/'):
                    Media['internals'].append(hostname+'/'+img['src']) 
                elif img['src'] in Null_format:
                    Media['null'].append(img['src'])  
                else:
                    Media['internals'].append(hostname+img['src'])   
        else:
            Media['externals'].append(img['src'])
           
    
    for audio in soup.find_all('audio', src=True):
        dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
        if hostname in audio['src'] or domain in audio['src'] or len(dots) == 1 or not audio['src'].startswith('http'):
             if not audio['src'].startswith('http'):
                if not audio['src'].startswith('/'):
                    Media['internals'].append(hostname+'/'+audio['src']) 
                elif audio['src'] in Null_format:
                    Media['null'].append(audio['src'])  
                else:
                    Media['internals'].append(hostname+audio['src'])   
        else:
            Media['externals'].append(audio['src'])
            
    for embed in soup.find_all('embed', src=True):
        dots = [x.start(0) for x in re.finditer('\.', embed['src'])]
        if hostname in embed['src'] or domain in embed['src'] or len(dots) == 1 or not embed['src'].startswith('http'):
             if not embed['src'].startswith('http'):
                if not embed['src'].startswith('/'):
                    Media['internals'].append(hostname+'/'+embed['src']) 
                elif embed['src'] in Null_format:
                    Media['null'].append(embed['src'])  
                else:
                    Media['internals'].append(hostname+embed['src'])   
        else:
            Media['externals'].append(embed['src'])
           
    for i_frame in soup.find_all('iframe', src=True):
        dots = [x.start(0) for x in re.finditer('\.', i_frame['src'])]
        if hostname in i_frame['src'] or domain in i_frame['src'] or len(dots) == 1 or not i_frame['src'].startswith('http'):
            if not i_frame['src'].startswith('http'):
                if not i_frame['src'].startswith('/'):
                    Media['internals'].append(hostname+'/'+i_frame['src']) 
                elif i_frame['src'] in Null_format:
                    Media['null'].append(i_frame['src'])  
                else:
                    Media['internals'].append(hostname+i_frame['src'])   
        else: 
            Media['externals'].append(i_frame['src'])
           

    # collect all link tags
    for link in soup.findAll('link', href=True):
        dots = [x.start(0) for x in re.finditer('\.', link['href'])]
        if hostname in link['href'] or domain in link['href'] or len(dots) == 1 or not link['href'].startswith('http'):
            if not link['href'].startswith('http'):
                if not link['href'].startswith('/'):
                    Link['internals'].append(hostname+'/'+link['href']) 
                elif link['href'] in Null_format:
                    Link['null'].append(link['href'])  
                else:
                    Link['internals'].append(hostname+link['href'])   
        else:
            Link['externals'].append(link['href'])

    for script in soup.find_all('script', src=True):
        dots = [x.start(0) for x in re.finditer('\.', script['src'])]
        if hostname in script['src'] or domain in script['src'] or len(dots) == 1 or not script['src'].startswith('http'):
            if not script['src'].startswith('http'):
                if not script['src'].startswith('/'):
                    Link['internals'].append(hostname+'/'+script['src']) 
                elif script['src'] in Null_format:
                    Link['null'].append(script['src'])  
                else:
                    Link['internals'].append(hostname+script['src'])   
        else:
            Link['externals'].append(link['href'])
           
            
    # collect all css
    for link in soup.find_all('link', rel='stylesheet'):
        dots = [x.start(0) for x in re.finditer('\.', link['href'])]
        if hostname in link['href'] or domain in link['href'] or len(dots) == 1 or not link['href'].startswith('http'):
            if not link['href'].startswith('http'):
                if not link['href'].startswith('/'):
                    CSS['internals'].append(hostname+'/'+link['href']) 
                elif link['href'] in Null_format:
                    CSS['null'].append(link['href'])  
                else:
                    CSS['internals'].append(hostname+link['href'])   
        else:
            CSS['externals'].append(link['href'])
    
    for style in soup.find_all('style', type='text/css'):
        try: 
            start = str(style[0]).index('@import url(')
            end = str(style[0]).index(')')
            css = str(style[0])[start+12:end]
            dots = [x.start(0) for x in re.finditer('\.', css)]
            if hostname in css or domain in css or len(dots) == 1 or not css.startswith('http'):
                if not css.startswith('http'):
                    if not css.startswith('/'):
                        CSS['internals'].append(hostname+'/'+css) 
                    elif css in Null_format:
                        CSS['null'].append(css)  
                    else:
                        CSS['internals'].append(hostname+css)   
            else: 
                CSS['externals'].append(css)
        except:
            continue
            
    # collect all form actions
    for form in soup.findAll('form', action=True):
        dots = [x.start(0) for x in re.finditer('\.', form['action'])]
        if hostname in form['action'] or domain in form['action'] or len(dots) == 1 or not form['action'].startswith('http'):
            if not form['action'].startswith('http'):
                if not form['action'].startswith('/'):
                    Form['internals'].append(hostname+'/'+form['action']) 
                elif form['action'] in Null_format or form['action'] == 'about:blank':
                    Form['null'].append(form['action'])  
                else:
                    Form['internals'].append(hostname+form['action'])   
        else:
            Form['externals'].append(form['action'])
            

    # collect all link tags
    for head in soup.find_all('head'):
        for head.link in soup.find_all('link', href=True):
            dots = [x.start(0) for x in re.finditer('\.', head.link['href'])]
            if hostname in head.link['href'] or len(dots) == 1 or domain in head.link['href'] or not head.link['href'].startswith('http'):
                if not head.link['href'].startswith('http'):
                    if not head.link['href'].startswith('/'):
                        Favicon['internals'].append(hostname+'/'+head.link['href']) 
                    elif head.link['href'] in Null_format:
                        Favicon['null'].append(head.link['href'])  
                    else:
                        Favicon['internals'].append(hostname+head.link['href'])   
            else:
                Favicon['externals'].append(head.link['href'])
                
        for head.link in soup.findAll('link', {'href': True, 'rel':True}):
            isicon = False
            if isinstance(head.link['rel'], list):
                for e_rel in head.link['rel']:
                    if (e_rel.endswith('icon')):
                        isicon = True
            else:
                if (head.link['rel'].endswith('icon')):
                    isicon = True
       
            if isicon:
                 dots = [x.start(0) for x in re.finditer('\.', head.link['href'])]
                 if hostname in head.link['href'] or len(dots) == 1 or domain in head.link['href'] or not head.link['href'].startswith('http'):
                     if not head.link['href'].startswith('http'):
                        if not head.link['href'].startswith('/'):
                            Favicon['internals'].append(hostname+'/'+head.link['href']) 
                        elif head.link['href'] in Null_format:
                            Favicon['null'].append(head.link['href'])  
                        else:
                            Favicon['internals'].append(hostname+head.link['href'])   
                 else:
                     Favicon['externals'].append(head.link['href'])
                     
                    
    # collect i_frame
    for i_frame in soup.find_all('iframe', width=True, height=True, frameborder=True):
        if i_frame['width'] == "0" and i_frame['height'] == "0" and i_frame['frameborder'] == "0":
            IFrame['invisible'].append(i_frame)
        else:
            IFrame['visible'].append(i_frame)
    for i_frame in soup.find_all('iframe', width=True, height=True, border=True):
        if i_frame['width'] == "0" and i_frame['height'] == "0" and i_frame['border'] == "0":
            IFrame['invisible'].append(i_frame)
        else:
            IFrame['visible'].append(i_frame)
    for i_frame in soup.find_all('iframe', width=True, height=True, style=True):
        if i_frame['width'] == "0" and i_frame['height'] == "0" and i_frame['style'] == "border:none;":
            IFrame['invisible'].append(i_frame)
        else:
            IFrame['visible'].append(i_frame)
          
    # get page title
    try:
        Title = soup.title.string
    except:
        pass
    
    # get content text
    Text = soup.get_text()
    
    return Href, Link, Anchor, Media, Form, CSS, Favicon, IFrame, Title, Text

def extract_features3(url):
    def words_raw_extraction(domain, subdomain, path):
        w_domain = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", domain.lower())
        w_subdomain = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", subdomain.lower())   
        w_path = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", path.lower())
        raw_words = w_domain + w_path + w_subdomain
        w_host = w_domain + w_subdomain
        raw_words = list(filter(None,raw_words))
        return raw_words, list(filter(None,w_host)), list(filter(None,w_path))
        
    Href = {'internals':[], 'externals':[], 'null':[]}
    Link = {'internals':[], 'externals':[], 'null':[]}
    Anchor = {'safe':[], 'unsafe':[], 'null':[]}
    Media = {'internals':[], 'externals':[], 'null':[]}
    Form = {'internals':[], 'externals':[], 'null':[]}
    CSS = {'internals':[], 'externals':[], 'null':[]}
    Favicon = {'internals':[], 'externals':[], 'null':[]}
    IFrame = {'visible':[], 'invisible':[], 'null':[]}
    Title =''
    Text= ''
    state, resolved_url, response = is_URL_accessible(url)
    if state:
        content = response.content
    else:
        content = ""

    hostname, domain, path = get_domain(url)
    extracted_domain = tldextract.extract(url)
    domain = extracted_domain.domain+'.'+extracted_domain.suffix
    subdomain = extracted_domain.subdomain
    tmp = url[url.find(extracted_domain.suffix):len(url)]
    pth = tmp.partition("/")
    path = pth[1] + pth[2]
    words_raw, words_raw_host, words_raw_path= words_raw_extraction(extracted_domain.domain, subdomain, pth[2])
    tld = extracted_domain.suffix
    parsed = urllib.parse.urlparse(url)
    scheme = parsed.scheme
    
    Href, Link, Anchor, Media, Form, CSS, Favicon, IFrame, Title, Text = extract_data_from_URL(hostname, content, domain, Href, Link, Anchor, Media, Form, CSS, Favicon, IFrame, Title, Text)

    features = {}
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname or ''
    path = parsed.path or ''
    netloc = parsed.netloc or ''
    scheme = parsed.scheme or ''
    query = parsed.query or ''

    # Fill in all features (many are placeholders for now)
    features['length_url'] = len(url)
    features['length_hostname'] = len(hostname)
    features['ip'] = urlfe.having_ip_address(url)
    features['nb_dots'] = url.count('.')
    features['nb_hyphens'] = url.count('-')
    features['nb_at'] = url.count('@')
    features['nb_qm'] = url.count('?')
    features['nb_and'] = url.count('&')
    features['nb_or'] = url.count('|')
    features['nb_eq'] = url.count('=')
    features['nb_underscore'] = url.count('_')
    features['nb_tilde'] = url.count('~')
    features['nb_percent'] = url.count('%')
    features['nb_slash'] = url.count('/')
    features['nb_star'] = url.count('*')
    features['nb_colon'] = url.count(':')
    features['nb_comma'] = url.count(',')
    features['nb_semicolumn'] = url.count(';')
    features['nb_dollar'] = url.count('$')
    features['nb_space'] = url.count(' ')
    features['nb_www'] = 1 if 'www' in url else 0
    features['nb_com'] = url.count('.com')
    features['nb_dslash'] = url.count('//')
    features['http_in_path'] = int('http' in path)
    features['https_token'] = urlfe.https_token(scheme)
    digits_url = sum(c.isdigit() for c in url)
    features['ratio_digits_url'] = digits_url / len(url) if len(url) > 0 else 0
    digits_host = sum(c.isdigit() for c in hostname)
    features['ratio_digits_host'] = digits_host / len(hostname) if len(hostname) > 0 else 0
    features['punycode'] = int('xn--' in hostname)
    features['port'] = parsed.port if parsed.port else 0
    tlds = ['.com', '.net', '.org', '.info', '.biz']
    features['tld_in_path'] = int(any(tld in path for tld in tlds))
    subdomain = hostname.replace(parsed.hostname.split('.')[-2] + '.' + parsed.hostname.split('.')[-1], '')
    features['tld_in_subdomain'] = int(any(tld in subdomain for tld in tlds))
    features['abnormal_subdomain'] = int(re.search(r'[^a-zA-Z0-9.-]', subdomain) is not None)
    features['nb_subdomains'] = urlfe.count_subdomain(url)
    features['prefix_suffix'] = int('-' in hostname)

    def shannon_entropy(data):
        if not data:
            return 0
        entropy = 0
        for x in set(data):
            p_x = data.count(x) / len(data)
            entropy -= p_x * math.log2(p_x)
        return entropy

    features['random_domain'] = int(shannon_entropy(hostname) > 4.5)
    shortening_services = ['bit.ly', 'goo.gl', 'tinyurl.com', 'ow.ly', 't.co']
    features['shortening_service'] = int(any(service in hostname for service in shortening_services))
    # response = requests.get(url, timeout=5, allow_redirects=True)
    # features['nb_redirection'] = len(response.history)
    # features['nb_external_redirection'] = sum(1 for r in response.history if urllib.parse.urlparse(r.url).netloc != hostname)
    if state and response is not None:
        features['nb_redirection'] = len(response.history)
        features['nb_external_redirection'] = sum(
        1 for r in response.history if urllib.parse.urlparse(r.url).netloc != hostname
    )
    else:
        features['nb_redirection'] = 0
        features['nb_external_redirection'] = 0

    features['length_words_raw'] = urlfe.length_word_raw(words_raw)
    features['char_repeat'] = urlfe.char_repeat(words_raw)
    features['shortest_word_host'] = urlfe.shortest_word_length(words_raw_host)
    features['shortest_word_path'] = urlfe.shortest_word_length(words_raw_path)
    features['longest_words_raw'] = urlfe.longest_word_length(words_raw)
    features['longest_word_host'] = urlfe.longest_word_length(words_raw_host)
    features['longest_word_path'] = urlfe.longest_word_length(words_raw_path)
    features['avg_words_raw'] = urlfe.average_word_length(words_raw)
    features['avg_word_host'] = urlfe.average_word_length(words_raw_host)
    features['avg_word_path'] = urlfe.average_word_length(words_raw_path)
    features['phish_hints'] = urlfe.phish_hints(url)
    brand_keywords = ['paypal', 'bank', 'login', 'secure']
    features['domain_in_brand'] = int(any(brand in hostname for brand in brand_keywords))
    features['brand_in_subdomain'] = int(any(brand in subdomain for brand in brand_keywords))
    features['brand_in_path'] = int(any(brand in path for brand in brand_keywords))
    features['suspecious_tld'] = urlfe.suspecious_tld(tld)
    features['statistical_report'] = 0

    features['nb_hyperlinks'] = ctnfe.nb_hyperlinks(Href, Link, Media, Form, CSS, Favicon)
    features['ratio_intHyperlinks'] = ctnfe.internal_hyperlinks(Href, Link, Media, Form, CSS, Favicon)
    features['ratio_extHyperlinks'] = ctnfe.external_hyperlinks(Href, Link, Media, Form, CSS, Favicon)
    features['ratio_nullHyperlinks'] = ctnfe.null_hyperlinks(hostname, Href, Link, Media, Form, CSS, Favicon)
    features['nb_extCSS'] = ctnfe.external_css(CSS)
    features['ratio_intRedirection'] = ctnfe.internal_redirection(Href, Link, Media, Form, CSS, Favicon)
    features['ratio_extRedirection'] = ctnfe.external_redirection(Href, Link, Media, Form, CSS, Favicon)
    features['ratio_intErrors'] = ctnfe.internal_errors(Href, Link, Media, Form, CSS, Favicon)
    features['ratio_extErrors'] = ctnfe.external_errors(Href, Link, Media, Form, CSS, Favicon)
    features['links_in_tags'] = ctnfe.links_in_tags(Link)
    features['ratio_intMedia'] = ctnfe.internal_media(Media)
    features['ratio_extMedia'] = ctnfe.external_media(Media)
    features['popup_window'] = ctnfe.popup_window(Text)
    features['safe_anchor'] = ctnfe.safe_anchor(Anchor)
    features['onmouseover'] = ctnfe.onmouseover(Text)
    features['right_clic'] = ctnfe.right_clic(Text)
    features['empty_title'] = ctnfe.empty_title(Title)

    features['url_numeric_path_length'] = sum(c.isdigit() for c in path)
    features['url_numeric_num_subdomains'] = hostname.count('.') - 1
    features['url_numeric_has_ip'] = features['ip']
    features['url_numeric_has_special_chars'] = int(bool(re.search(r'[^a-zA-Z0-9]', url)))

    print(url)
    print(features)
    print("This is how many features we have",len(features))
    return features    

extract_features3("https://parade.com/425836/joshwigler/the-amazing-race-host-phil-keoghan-previews-the-season-27-premiere/")