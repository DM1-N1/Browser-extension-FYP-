

# import re
# import socket
# import math
# import whois
# import requests
# import datetime
# import ipaddress
# from urllib.parse import urlparse
# from bs4 import BeautifulSoup
# from collections import Counter
# from statistics import mean


# def extract_features(url):
#     features = {}
#     parsed = urlparse(url)
#     hostname = parsed.hostname or ''
#     path = parsed.path or ''
#     netloc = parsed.netloc or ''
#     scheme = parsed.scheme or ''
#     query = parsed.query or ''
#     features['length_url'] = len(url)
#     features['length_hostname'] = len(hostname)
#     try:
#         ipaddress.ip_address(hostname)
#         features['ip'] = 1
#     except:
#         features['ip'] = 0
#     features['nb_dots'] = url.count('.')
#     features['nb_hyphens'] = url.count('-')
#     features['nb_at'] = url.count('@')
#     features['nb_qm'] = url.count('?')
#     features['nb_and'] = url.count('&')
#     features['nb_or'] = url.count('|')
#     features['nb_eq'] = url.count('=')
#     features['nb_underscore'] = url.count('_')
#     features['nb_tilde'] = url.count('~')
#     features['nb_percent'] = url.count('%')
#     features['nb_slash'] = url.count('/')
#     features['nb_star'] = url.count('*')
#     features['nb_colon'] = url.count(':')
#     features['nb_comma'] = url.count(',')
#     features['nb_semicolumn'] = url.count(';')
#     features['nb_dollar'] = url.count('$')
#     features['nb_space'] = url.count(' ')
#     features['nb_www'] = url.count('www')
#     features['nb_com'] = url.count('.com')
#     features['nb_dslash'] = url.count('//')
#     features['http_in_path'] = int('http' in path)
#     features['https_token'] = int('https' in url)
#     digits_url = sum(c.isdigit() for c in url)
#     features['ratio_digits_url'] = digits_url / len(url) if len(url) > 0 else 0
#     digits_host = sum(c.isdigit() for c in hostname)
#     features['ratio_digits_host'] = digits_host / len(hostname) if len(hostname) > 0 else 0
#     features['punycode'] = int('xn--' in hostname)
#     features['port'] = parsed.port if parsed.port else 0
#     tlds = ['.com', '.net', '.org', '.info', '.biz']
#     features['tld_in_path'] = int(any(tld in path for tld in tlds))
#     subdomain = hostname.replace(parsed.hostname.split('.')[-2] + '.' + parsed.hostname.split('.')[-1], '')
#     features['tld_in_subdomain'] = int(any(tld in subdomain for tld in tlds))
#     features['abnormal_subdomain'] = int(re.search(r'[^a-zA-Z0-9.-]', subdomain) is not None)
#     features['nb_subdomains'] = subdomain.count('.') if subdomain else 0
#     features['prefix_suffix'] = int('-' in hostname)
#     def shannon_entropy(data):
#         if not data:
#             return 0
#         entropy = 0
#         for x in set(data):
#             p_x = data.count(x) / len(data)
#             entropy -= p_x * math.log2(p_x)  # Use math.log2 instead of bit_length
#             return entropy

#     features['random_domain'] = int(shannon_entropy(hostname) > 4.5)
#     shortening_services = ['bit.ly', 'goo.gl', 'tinyurl.com', 'ow.ly', 't.co']
#     features['shortening_service'] = int(any(service in hostname for service in shortening_services))
#     features['path_extension'] = path.split('.')[-1] if '.' in path else 0
#     try:
#         response = requests.get(url, timeout=5, allow_redirects=True)
#         features['nb_redirection'] = len(response.history)
#         features['nb_external_redirection'] = sum(1 for r in response.history if urlparse(r.url).netloc != hostname)
#     except:
#         features['nb_redirection'] = 0
#         features['nb_external_redirection'] = 0
#     words_raw = re.findall(r'\w+', url)
#     features['length_words_raw'] = len(words_raw)
#     char_count = Counter(url)
#     features['char_repeat'] = sum(1 for count in char_count.values() if count > 1)
#     host_words = re.findall(r'\w+', hostname)
#     path_words = re.findall(r'\w+', path)
#     features['shortest_words_raw'] = min((len(w) for w in words_raw), default=0)
#     features['shortest_word_host'] = min((len(w) for w in host_words), default=0)
#     features['shortest_word_path'] = min((len(w) for w in path_words), default=0)
#     features['longest_words_raw'] = max((len(w) for w in words_raw), default=0)
#     features['longest_word_host'] = max((len(w) for w in host_words), default=0)
#     features['longest_word_path'] = max((len(w) for w in path_words), default=0)
#     features['avg_words_raw'] = mean((len(w) for w in words_raw)) if words_raw else 0
#     features['avg_word_host'] = mean((len(w) for w in host_words)) if host_words else 0
#     features['avg_word_path'] = mean((len(w) for w in path_words)) if path_words else 0
#     suspicious_patterns = ['@', '%', 'http://', 'https://']
#     features['phish_hints'] = int(any(pattern in url for pattern in suspicious_patterns))
#     brand_keywords = ['paypal', 'bank', 'login', 'secure']
#     features['domain_in_brand'] = int(any(brand in hostname for brand in brand_keywords))
#     features['brand_in_subdomain'] = int(any(brand in subdomain for brand in brand_keywords))
#     features['brand_in_path'] = int(any(brand in path for brand in brand_keywords))
#     suspicious_tlds = ['.zip', '.review', '.country', '.kim', '.cricket']
#     features['suspecious_tld'] = int(any(tld in hostname for tld in suspicious_tlds))
#     features['statistical_report'] = 0
#     try:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         hyperlinks = soup.find_all('a', href=True)
#         features['nb_hyperlinks'] = len(hyperlinks)
#         internal_links = [link for link in hyperlinks if hostname in link['href']]
#         external_links = [link for link in hyperlinks if hostname not in link['href']]
#         null_links = [link for link in hyperlinks if link['href'] in ['#', '']]
#         total_links = len(hyperlinks)
#         features['ratio_intHyperlinks'] = len(internal_links) / total_links if total_links else 0
#         features['ratio_extHyperlinks'] = len(external_links) / total_links if total_links else 0
#         features['ratio_nullHyperlinks'] = len(null_links) / total_links if total_links else 0
#         features['nb_extCSS'] = len([link for link in soup.find_all('link', href=True) if hostname not in link['href']])
#         media_tags = soup.find_all(['img', 'video', 'audio', 'source'])
#         internal_media = [tag for tag in media_tags if hostname in tag.get('src', '')]
#         external_media = [tag for tag in media_tags if hostname not in tag.get('src', '')]
#         total_media = len(media_tags)
#         features['ratio_intMedia'] = len(internal_media) / total_media if total_media else 0
#         features['ratio_extMedia'] = len(external_media) / total_media if total_media else 0
#         forms = soup.find_all('form')
#         features['sfh'] = int(any(hostname not in form.get('action', '') for form in forms))
#         features['login_form'] = int(any('password' in (input_.get('type') or '').lower() 
#                                          for form in forms
#                                          for input_ in form.find_all('input')))
#         features['iframe'] = int(bool(soup.find('iframe')))
#         features['popup_window'] = int('window.open' in response.text)
#         features['safe_anchor'] = int(any('rel' in a.attrs and 'noopener' in a['rel'] for a in hyperlinks))
#         features['onmouseover'] = int('onmouseover' in response.text)
#         features['right_clic'] = int('contextmenu' in response.text)
#         features['empty_title'] = int(not soup.title or not soup.title.string.strip())
#         features['domain_in_title'] = int(hostname in (soup.title.string if soup.title else ''))
#         features['domain_with_copyright'] = int('copyright' in response.text.lower())
#         features['submit_email'] = int(bool(re.search(r'mailto:', response.text)))
#         features['external_favicon'] = int(any(hostname not in link.get('href', '') for link in soup.find_all('link', rel='icon')))
#         features['links_in_tags'] = len(hyperlinks)
#     except:
#             features.update({
#         'nb_hyperlinks': 0, 'ratio_intHyperlinks': 0, 'ratio_extHyperlinks': 0, 'ratio_nullHyperlinks': 0,
#         'nb_extCSS': 0, 'ratio_intMedia': 0, 'ratio_extMedia': 0, 'sfh': 0, 'login_form': 0, 'iframe': 0,
#         'popup_window': 0, 'safe_anchor': 0, 'onmouseover': 0, 'right_clic': 0, 'empty_title': 0,
#         'domain_in_title': 0, 'domain_with_copyright': 0, 'submit_email': 0, 'external_favicon': 0, 'links_in_tags': 0
#     })
#     try:
#         int_redir = [r for r in response.history if hostname in r.url]
#         ext_redir = [r for r in response.history if hostname not in r.url]
#         total_redir = len(response.history)
#         features['ratio_intRedirection'] = len(int_redir) / total_redir if total_redir else 0
#         features['ratio_extRedirection'] = len(ext_redir) / total_redir if total_redir else 0
#     except:
#         features['ratio_intRedirection'] = 0
#         features['ratio_extRedirection'] = 0
#     try:
#         features['ratio_intErrors'] = int('404' in response.text or '403' in response.text)
#         features['ratio_extErrors'] = 0
#     except:
#         features['ratio_intErrors'] = 0
#         features['ratio_extErrors'] = 0
#     try:
#         domain_info = whois.whois(hostname)
#         features['whois_registered_domain'] = int(domain_info.domain_name is not None)
#         if domain_info.creation_date and domain_info.expiration_date:
#             creation = domain_info.creation_date
#             expiration = domain_info.expiration_date
#             if isinstance(creation, list): creation = creation[0]
#             if isinstance(expiration, list): expiration = expiration[0]
#             features['domain_registration_length'] = (expiration - creation).days
#             features['domain_age'] = (datetime.datetime.now() - creation).days
#         else:
#             features['domain_registration_length'] = 0
#             features['domain_age'] = 0
#     except:
#         features['whois_registered_domain'] = 0
#         features['domain_registration_length'] = 0
#         features['domain_age'] = 0
#     features['web_traffic'] = 0
#     features['dns_record'] = int(bool(socket.gethostbyname(hostname)) if hostname else 0)
#     features['google_index'] = 0
#     features['page_rank'] = 0
#     features['url_numeric_domain'] = int(bool(re.search(r'\d', hostname)))
#     features['url_numeric_path_length'] = sum(c.isdigit() for c in path)
#     features['url_numeric_num_subdomains'] = hostname.count('.') - 1
#     features['url_numeric_has_ip'] = features['ip']
#     features['url_numeric_has_special_chars'] = int(bool(re.search(r'[^a-zA-Z0-9]', url)))
#     print(features)
#     return features




import re
import socket
import math
import whois
import requests
import datetime
import ipaddress
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from collections import Counter
from statistics import mean


def extract_features(url):
    features = {}
    parsed = urlparse(url)
    hostname = parsed.hostname or ''
    path = parsed.path or ''
    netloc = parsed.netloc or ''
    scheme = parsed.scheme or ''
    query = parsed.query or ''
    features['length_url'] = len(url)
    features['length_hostname'] = len(hostname)
    try:
        ipaddress.ip_address(hostname)
        features['ip'] = 1
    except:
        features['ip'] = 0
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
    features['nb_dslash'] = url.count('//')
    features['http_in_path'] = int('http' in path)
    features['https_token'] = int('https' in url)
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
    features['nb_subdomains'] = subdomain.count('.') if subdomain else 0
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
    features['length_words_raw'] = len(words_raw)
    char_count = Counter(url)
    features['char_repeat'] = sum(1 for count in char_count.values() if count > 1)
    host_words = re.findall(r'\w+', hostname)
    path_words = re.findall(r'\w+', path)
    features['shortest_words_raw'] = min((len(w) for w in words_raw), default=0)
    features['shortest_word_host'] = min((len(w) for w in host_words), default=0)
    features['shortest_word_path'] = min((len(w) for w in path_words), default=0)
    features['longest_words_raw'] = max((len(w) for w in words_raw), default=0)
    features['longest_word_host'] = max((len(w) for w in host_words), default=0)
    features['longest_word_path'] = max((len(w) for w in path_words), default=0)
    features['avg_words_raw'] = mean((len(w) for w in words_raw)) if words_raw else 0
    features['avg_word_host'] = mean((len(w) for w in host_words)) if host_words else 0
    features['avg_word_path'] = mean((len(w) for w in path_words)) if path_words else 0
    suspicious_patterns = ['@', '%', 'http://', 'https://']
    features['phish_hints'] = int(any(pattern in url for pattern in suspicious_patterns))
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
        features['nb_hyperlinks'] = len(hyperlinks)
        internal_links = [link for link in hyperlinks if hostname in link['href']]
        external_links = [link for link in hyperlinks if hostname not in link['href']]
        null_links = [link for link in hyperlinks if link['href'] in ['#', '']]
        total_links = len(hyperlinks)
        features['ratio_intHyperlinks'] = len(internal_links) / total_links if total_links else 0
        features['ratio_extHyperlinks'] = len(external_links) / total_links if total_links else 0
        features['ratio_nullHyperlinks'] = len(null_links) / total_links if total_links else 0
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
        features['iframe'] = int(bool(soup.find('iframe')))
        features['popup_window'] = int('window.open' in response.text)
        features['safe_anchor'] = int(any('rel' in a.attrs and 'noopener' in a['rel'] for a in hyperlinks))
        features['onmouseover'] = int('onmouseover' in response.text)
        features['right_clic'] = int('contextmenu' in response.text)
        features['empty_title'] = int(not soup.title or not soup.title.string.strip())
        features['domain_in_title'] = int(hostname in (soup.title.string if soup.title else ''))
        features['domain_with_copyright'] = int('copyright' in response.text.lower())
        features['submit_email'] = int(bool(re.search(r'mailto:', response.text)))
        features['external_favicon'] = int(any(hostname not in link.get('href', '') for link in soup.find_all('link', rel='icon')))
        features['links_in_tags'] = len(hyperlinks)
    except:
            features.update({
        'nb_hyperlinks': 0, 'ratio_intHyperlinks': 0, 'ratio_extHyperlinks': 0, 'ratio_nullHyperlinks': 0,
        'nb_extCSS': 0, 'ratio_intMedia': 0, 'ratio_extMedia': 0, 'sfh': 0, 'login_form': 0, 'iframe': 0,
        'popup_window': 0, 'safe_anchor': 0, 'onmouseover': 0, 'right_clic': 0, 'empty_title': 0,
        'domain_in_title': 0, 'domain_with_copyright': 0, 'submit_email': 0, 'external_favicon': 0, 'links_in_tags': 0
    })
    try:
        int_redir = [r for r in response.history if hostname in r.url]
        ext_redir = [r for r in response.history if hostname not in r.url]
        total_redir = len(response.history)
        features['ratio_intRedirection'] = len(int_redir) / total_redir if total_redir else 0
        features['ratio_extRedirection'] = len(ext_redir) / total_redir if total_redir else 0
    except:
        features['ratio_intRedirection'] = 0
        features['ratio_extRedirection'] = 0
    try:
        features['ratio_intErrors'] = int('404' in response.text or '403' in response.text)
        features['ratio_extErrors'] = 0
    except:
        features['ratio_intErrors'] = 0
        features['ratio_extErrors'] = 0
    try:
        domain_info = whois.whois(hostname)
        features['whois_registered_domain'] = int(domain_info.domain_name is not None)
        if domain_info.creation_date and domain_info.expiration_date:
            creation = domain_info.creation_date
            expiration = domain_info.expiration_date
            if isinstance(creation, list): creation = creation[0]
            if isinstance(expiration, list): expiration = expiration[0]
            features['domain_registration_length'] = (expiration - creation).days
            features['domain_age'] = (datetime.datetime.now() - creation).days
        else:
            features['domain_registration_length'] = 0
            features['domain_age'] = 0
    except:
        features['whois_registered_domain'] = 0
        features['domain_registration_length'] = 0
        features['domain_age'] = 0
    features['web_traffic'] = 0
    try:
        features['dns_record'] = int(bool(socket.gethostbyname(hostname)) if hostname else 0)
    except socket.gaierror:
        features['dns_record'] = 0
    features['google_index'] = 0
    features['page_rank'] = 0
    features['url_numeric_domain'] = int(bool(re.search(r'\d', hostname)))
    features['url_numeric_path_length'] = sum(c.isdigit() for c in path)
    features['url_numeric_num_subdomains'] = hostname.count('.') - 1
    features['url_numeric_has_ip'] = features['ip']
    features['url_numeric_has_special_chars'] = int(bool(re.search(r'[^a-zA-Z0-9]', url)))
    print(features)
    return features

# Ask wether to have path extension as always 0 or suttin else