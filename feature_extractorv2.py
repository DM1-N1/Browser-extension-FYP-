import content_features as ctnfe
import url_features as urlfe
import external_features as trdfe
import pandas as pd 
import urllib.parse
import tldextract
import requests
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import socket
import math
import whois
import datetime
import ipaddress
from collections import Counter
from statistics import mean



def get_domain(url):
    o = urllib.parse.urlsplit(url)
    return o.hostname, tldextract.extract(url).domain, o.path

# def is_URL_accessible(url):
#     #iurl = url
#     #parsed = urlparse(url)
#     #url = parsed.scheme+'://'+parsed.netloc
#     page = None
#     try:
#         page = requests.get(url, timeout=5)   
#     except:
#         parsed = urlparse(url)
#         url = parsed.scheme+'://'+parsed.netloc
#         if not parsed.netloc.startswith('www'):
#             url = parsed.scheme+'://www.'+parsed.netloc
#             try:
#                 page = requests.get(url, timeout=5)
#             except:
#                 page = None
#                 pass
#         # if not parsed.netloc.startswith('www'):
#         #     url = parsed.scheme+'://www.'+parsed.netloc
#         #     #iurl = iurl.replace('https://', 'https://www.')
#         #     try:
#         #         page = requests.get(url)
#         #     except:        
#         #         # url = 'http://'+parsed.netloc
#         #         # iurl = iurl.replace('https://', 'http://')
#         #         # try:
#         #         #     page = requests.get(url) 
#         #         # except:
#         #         #     if not parsed.netloc.startswith('www'):
#         #         #         url = parsed.scheme+'://www.'+parsed.netloc
#         #         #         iurl = iurl.replace('http://', 'http://www.')
#         #         #         try:
#         #         #             page = requests.get(url)
#         #         #         except:
#         #         #             pass
#         #         pass 
#     if page and page.status_code == 200 and page.content not in ["b''", "b' '"]:
#         return True, url, page
#     else:
#         return False, None, None

def is_URL_accessible(url):
    page = None
    try:
        page = requests.get(url, timeout=5)
    except:
        parsed = urlparse(url)
        url = parsed.scheme + '://' + parsed.netloc
        if not parsed.netloc.startswith('www'):
            url = parsed.scheme + '://www.' + parsed.netloc
            try:
                page = requests.get(url, timeout=5)
            except:
                page = None
    if page and page.status_code == 200 and page.content not in ["b''", "b' '"]:
        return page  # Return only the page object
    else:
        return None
    



 
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


#################################################################################################################################
#              Calculate features from extracted data
#################################################################################################################################


def extract_features2(url):

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
    page = is_URL_accessible(url)
    if page:
        content = page.content
        # Proceed with the rest of the logic
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
    parsed = urlparse(url)
    scheme = parsed.scheme
    
    Href, Link, Anchor, Media, Form, CSS, Favicon, IFrame, Title, Text = extract_data_from_URL(hostname, content, domain, Href, Link, Anchor, Media, Form, CSS, Favicon, IFrame, Title, Text)

    features = {}
    parsed = urlparse(url)
    hostname = parsed.hostname or ''
    path = parsed.path or ''
    netloc = parsed.netloc or ''
    scheme = parsed.scheme or ''
    query = parsed.query or ''

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
    features['nb_www'] = url.count('www')
    features['nb_com'] = url.count('.com')
    # features['nb_dslash'] =  urlfe.count_double_slash(url)
    features['http_in_path'] = int('http' in path)
    # features['https_token'] = urlfe.https_token(scheme)
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
    # features['nb_subdomains'] = urlfe.count_subdomain(url)
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
    features['path_extension'] = path.split('.')[-1] if '.' in path else 0
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        features['nb_redirection'] = len(response.history)
        features['nb_external_redirection'] = sum(1 for r in response.history if urlparse(r.url).netloc != hostname)
    except:
        features['nb_redirection'] = 0
        features['nb_external_redirection'] = 0
    words_raw = re.findall(r'\w+', url)
    # features['length_words_raw'] = len(words_raw)
    char_count = Counter(url)
    # features['char_repeat'] = sum(1 for count in char_count.values() if count > 1)
    # features['char_repeat'] = urlfe.char_repeat(words_raw)
    host_words = re.findall(r'\w+', hostname)
    path_words = re.findall(r'\w+', path)
    # features['shortest_words_raw'] = min((len(w) for w in words_raw), default=0)
    # features['shortest_word_host'] = min((len(w) for w in host_words), default=0)
    # features['shortest_word_path'] = min((len(w) for w in path_words), default=0)
    # features['longest_words_raw'] = max((len(w) for w in words_raw), default=0)
    # features['longest_word_host'] = max((len(w) for w in host_words), default=0)
    # features['longest_word_path'] = max((len(w) for w in path_words), default=0)
    # features['avg_words_raw'] = mean((len(w) for w in words_raw)) if words_raw else 0
    # features['avg_word_host'] = mean((len(w) for w in host_words)) if host_words else 0
    # features['avg_word_path'] = mean((len(w) for w in path_words)) if path_words else 0

    features['shortest_words_raw'] = urlfe.shortest_word_length(words_raw)
    # features['shortest_word_host'] = urlfe.shortest_word_length(words_raw_host)
    features['shortest_word_path'] = urlfe.shortest_word_length(words_raw_path)
    features['longest_words_raw'] = urlfe.longest_word_length(words_raw)
    features['longest_word_host'] = urlfe.longest_word_length(words_raw_host)
    features['longest_word_path'] = urlfe.longest_word_length(words_raw_path)
    # features['avg_words_raw'] = urlfe.average_word_length(words_raw)
    # features['avg_word_host'] = urlfe.average_word_length(words_raw_host)
    features['avg_word_path'] = urlfe.average_word_length(words_raw_path)
    suspicious_patterns = ['@', '%', 'http://', 'https://']
    # features['phish_hints'] = int(any(pattern in url for pattern in suspicious_patterns))
    features['phish_hints'] = urlfe.phish_hints(url)
    brand_keywords = ['paypal', 'bank', 'login', 'secure']
    features['domain_in_brand'] = int(any(brand in hostname for brand in brand_keywords))
    features['brand_in_subdomain'] = int(any(brand in subdomain for brand in brand_keywords))
    features['brand_in_path'] = int(any(brand in path for brand in brand_keywords))
    suspicious_tlds = ['.zip', '.review', '.country', '.kim', '.cricket']
    features['suspecious_tld'] = int(any(tld in hostname for tld in suspicious_tlds))
    features['statistical_report'] = 0
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        hyperlinks = soup.find_all('a', href=True)
        # features['nb_hyperlinks'] = len(hyperlinks)
        features['nb_hyperlinks'] = ctnfe.nb_hyperlinks(Href, Link, Media, Form, CSS, Favicon)
        internal_links = [link for link in hyperlinks if hostname in link['href']]
        external_links = [link for link in hyperlinks if hostname not in link['href']]
        null_links = [link for link in hyperlinks if link['href'] in ['#', '']]
        total_links = len(hyperlinks)
        # features['ratio_intHyperlinks'] = len(internal_links) / total_links if total_links else 0
        # features['ratio_extHyperlinks'] = len(external_links) / total_links if total_links else 0
        # features['ratio_nullHyperlinks'] = len(null_links) / total_links if total_links else 0
        features['ratio_intHyperlinks'] = ctnfe.internal_hyperlinks(Href, Link, Media, Form, CSS, Favicon)
        features['ratio_extHyperlinks'] = ctnfe.external_hyperlinks(Href, Link, Media, Form, CSS, Favicon)
        features['ratio_nullHyperlinks'] = ctnfe.null_hyperlinks(Href, Link, Media, Form, CSS, Favicon)
        features['nb_extCSS'] = len([link for link in soup.find_all('link', href=True) if hostname not in link['href']])
        media_tags = soup.find_all(['img', 'video', 'audio', 'source'])
        internal_media = [tag for tag in media_tags if hostname in tag.get('src', '')]
        external_media = [tag for tag in media_tags if hostname not in tag.get('src', '')]
        total_media = len(media_tags)
        features['ratio_intMedia'] = len(internal_media) / total_media if total_media else 0
        features['ratio_extMedia'] = len(external_media) / total_media if total_media else 0
        forms = soup.find_all('form')
        features['sfh'] = int(any(hostname not in form.get('action', '') for form in forms))
        features['login_form'] = int(any('password' in (input_.get('type') or '').lower() 
                                        for form in forms
                                        for input_ in form.find_all('input')))
        # features['iframe'] = int(bool(soup.find('iframe')))
        features['iframe'] = ctnfe.iframe(IFrame)
        features['popup_window'] = int('window.open' in response.text)
        # features['safe_anchor'] = int(any('rel' in a.attrs and 'noopener' in a['rel'] for a in hyperlinks))
        features['safe_anchor'] = ctnfe.safe_anchor(Anchor)
        # features['onmouseover'] = int('onmouseover' in response.text)
        features['onmouseover'] = ctnfe.onmouseover(Text)
        features['right_clic'] = int('contextmenu' in response.text)
        features['empty_title'] = int(not soup.title or not soup.title.string.strip())
        # features['domain_in_title'] = int(hostname in (soup.title.string if soup.title else ''))
        # features['domain_with_copyright'] = int('copyright' in response.text.lower())
        features['domain_with_copyright'] = ctnfe.domain_with_copyright(extracted_domain.domain, Text)
        features['submit_email'] = int(bool(re.search(r'mailto:', response.text)))
        # features['external_favicon'] = int(any(hostname not in link.get('href', '') for link in soup.find_all('link', rel='icon')))
        features['external_favicon'] = ctnfe.external_favicon(Favicon)
        features['links_in_tags'] = len(hyperlinks)
    except:
            features.update({
        'nb_hyperlinks': 0, 'ratio_intHyperlinks': 0, 'ratio_extHyperlinks': 0, 'ratio_nullHyperlinks': 0,
        'nb_extCSS': 0, 'ratio_intMedia': 0, 'ratio_extMedia': 0, 'sfh': 0, 'login_form': 0, 'iframe': 0,
        'popup_window': 0, 'safe_anchor': 0, 'onmouseover': 0, 'right_clic': 0, 'empty_title': 0,
        'domain_in_title': 0, 'domain_with_copyright': 0, 'submit_email': 0, 'external_favicon': 0, 'links_in_tags': 0
    })
    # try:
    #     int_redir = [r for r in response.history if hostname in r.url]
    #     ext_redir = [r for r in response.history if hostname not in r.url]
    #     total_redir = len(response.history)
    #     features['ratio_intRedirection'] = len(int_redir) / total_redir if total_redir else 0
    #     features['ratio_extRedirection'] = len(ext_redir) / total_redir if total_redir else 0
    # except:
    #     features['ratio_intRedirection'] = 0
    #     features['ratio_extRedirection'] = 0
    # try:
    #     features['ratio_intErrors'] = int('404' in response.text or '403' in response.text)
    #     features['ratio_extErrors'] = 0
    # except:
    #     features['ratio_intErrors'] = 0
    #     features['ratio_extErrors'] = 0

    features['ratio_intRedirection'] = ctnfe.internal_redirection(Href, Link, Media, Form, CSS, Favicon)
    features['ratio_extRedirection'] = ctnfe.external_redirection(Href, Link, Media, Form, CSS, Favicon)
    features['ratio_intErrors'] = ctnfe.internal_errors(Href, Link, Media, Form, CSS, Favicon)
    features['ratio_extErrors'] = ctnfe.external_errors(Href, Link, Media, Form, CSS, Favicon)
    # try:
    #     domain_info = whois.whois(hostname)
    #     features['whois_registered_domain'] = int(domain_info.domain_name is not None)
    #     if domain_info.creation_date and domain_info.expiration_date:
    #         creation = domain_info.creation_date
    #         expiration = domain_info.expiration_date
    #         if isinstance(creation, list): creation = creation[0]
    #         if isinstance(expiration, list): expiration = expiration[0]
    #         features['domain_registration_length'] = (expiration - creation).days
    #         features['domain_age'] = (datetime.datetime.now() - creation).days
    #     else:
    #         features['domain_registration_length'] = 0
    #         features['domain_age'] = 0
    # except:
    #     # features['whois_registered_domain'] = 0
    #     # features['domain_registration_length'] = 0
    #     # features['domain_age'] = 0
    # features['whois_registered_domain'] = trdfe.whois_registered_domain(domain),
    # features['domain_registration_length'] = trdfe.domain_registration_length(domain)
    # features['domain_age'] = trdfe.domain_age(domain)
    # features['domain_age'] = 9368  
    # features['web_traffic'] = 0
    # features['web_traffic'] = trdfe.web_traffic(url)
    # try:
    #     features['dns_record'] = int(bool(socket.gethostbyname(hostname)) if hostname else 0)
    # except socket.gaierror:
    #     features['dns_record'] = 0
    # features['dns_record'] = trdfe.dns_record(domain)
    # features['google_index'] = 0
    features['google_index'] = trdfe.google_index(url)
    features['page_rank'] = 0
    features['url_numeric_domain'] = int(bool(re.search(r'\d', hostname)))
    features['url_numeric_path_length'] = sum(c.isdigit() for c in path)
    features['url_numeric_num_subdomains'] = hostname.count('.') - 1
    features['url_numeric_has_ip'] = features['ip']
    features['url_numeric_has_special_chars'] = int(bool(re.search(r'[^a-zA-Z0-9]', url)))
    print(url)
    print(features)
    return features    
