import re
import math
import ipaddress
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from collections import Counter

def extract_features(url):
    features = {}
    parsed = urlparse(url)
    hostname = parsed.hostname or ''
    path = parsed.path or ''
    subdomain = '.'.join(hostname.split('.')[:-2]) if len(hostname.split('.')) > 2 else ''

    # Length-based
    features['length_url'] = len(url)
    features['length_hostname'] = len(hostname)

    # IP presence
    try:
        ipaddress.ip_address(hostname)
        features['ip'] = 1
    except:
        features['ip'] = 0

    # Character counts
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

    # Keyword checks
    features['http_in_path'] = int('http' in path)

    # Digit ratios
    features['ratio_digits_url'] = sum(c.isdigit() for c in url) / len(url)
    features['ratio_digits_host'] = sum(c.isdigit() for c in hostname) / len(hostname) if hostname else 0

    features['punycode'] = int('xn--' in hostname)
    features['port'] = parsed.port if parsed.port else 0

    # TLD checks
    tlds = ['.com', '.net', '.org', '.info', '.biz']
    features['tld_in_path'] = int(any(tld in path for tld in tlds))
    features['tld_in_subdomain'] = int(any(tld in subdomain for tld in tlds))

    # Abnormal subdomain
    features['abnormal_subdomain'] = int(bool(re.search(r'[^a-zA-Z0-9.-]', subdomain)))

    # Prefix-suffix
    features['prefix_suffix'] = int('-' in hostname)

    # Shannon entropy
    def shannon_entropy(data):
        if not data: return 0
        p = [data.count(c) / len(data) for c in set(data)]
        return -sum(pi * math.log2(pi) for pi in p)

    features['random_domain'] = int(shannon_entropy(hostname) > 4.5)

    # Shorteners
    shortening_services = ['bit.ly', 'goo.gl', 'tinyurl.com', 'ow.ly', 't.co']
    features['shortening_service'] = int(any(service in hostname for service in shortening_services))

    # Path extension as integer length of extension, or 0
    features['path_extension'] = len(path.split('.')[-1]) if '.' in path else 0

    # Redirections
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        features['nb_redirection'] = len(response.history)
        features['nb_external_redirection'] = sum(1 for r in response.history if urlparse(r.url).hostname != hostname)
    except:
        features['nb_redirection'] = 0
        features['nb_external_redirection'] = 0

    # Word metrics
    words_raw = re.findall(r'\w+', url)
    host_words = re.findall(r'\w+', hostname)
    path_words = re.findall(r'\w+', path)

    features['shortest_words_raw'] = min((len(w) for w in words_raw), default=0)
    features['shortest_word_path'] = min((len(w) for w in path_words), default=0)
    features['longest_words_raw'] = max((len(w) for w in words_raw), default=0)
    features['longest_word_host'] = max((len(w) for w in host_words), default=0)
    features['longest_word_path'] = max((len(w) for w in path_words), default=0)

    # Hints
    suspicious_patterns = ['@', '%', 'http://', 'https://']
    features['phish_hints'] = int(any(p in url for p in suspicious_patterns))

    # Brand presence
    brands = ['paypal', 'bank', 'login', 'secure']
    features['domain_in_brand'] = int(any(b in hostname for b in brands))
    features['brand_in_subdomain'] = int(any(b in subdomain for b in brands))
    features['brand_in_path'] = int(any(b in path for b in brands))

    # Suspicious TLDs
    bad_tlds = ['.zip', '.review', '.country', '.kim', '.cricket']
    features['suspecious_tld'] = int(any(tld in hostname for tld in bad_tlds))

    # Static value
    features['statistical_report'] = 0

    # Web page analysis
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        hyperlinks = soup.find_all('a', href=True)
        internal = [a for a in hyperlinks if hostname in a['href']]
        external = [a for a in hyperlinks if hostname not in a['href']]
        nulls = [a for a in hyperlinks if a['href'] in ['#', '']]

        features['nb_hyperlinks'] = len(hyperlinks)
        total_links = len(hyperlinks)
        features['ratio_intHyperlinks'] = len(internal) / total_links if total_links else 0
        features['ratio_extHyperlinks'] = len(external) / total_links if total_links else 0
        features['ratio_nullHyperlinks'] = len(nulls) / total_links if total_links else 0

        features['nb_extCSS'] = len([l for l in soup.find_all('link', href=True) if hostname not in l['href']])
        media = soup.find_all(['img', 'video', 'audio', 'source'])
        features['ratio_intMedia'] = len([m for m in media if hostname in m.get('src', '')]) / len(media) if media else 0
        features['ratio_extMedia'] = len([m for m in media if hostname not in m.get('src', '')]) / len(media) if media else 0

        forms = soup.find_all('form')
        features['sfh'] = int(any(hostname not in f.get('action', '') for f in forms))
        features['login_form'] = int(any('password' in (i.get('type') or '') for f in forms for i in f.find_all('input')))
        features['iframe'] = int(bool(soup.find('iframe')))
        features['popup_window'] = int('window.open' in response.text)
        features['safe_anchor'] = int(any('noopener' in a.get('rel', []) for a in hyperlinks))
        features['onmouseover'] = int('onmouseover' in response.text)
        features['right_clic'] = int('contextmenu' in response.text)
        features['empty_title'] = int(not soup.title or not soup.title.string.strip())
        features['domain_in_title'] = int(hostname in (soup.title.string if soup.title else ''))
        features['domain_with_copyright'] = int('copyright' in response.text.lower())
        features['submit_email'] = int('mailto:' in response.text)
        features['external_favicon'] = int(any(hostname not in l.get('href', '') for l in soup.find_all('link', rel='icon')))
        features['links_in_tags'] = len(hyperlinks)
    except:
        for key in ['nb_hyperlinks', 'ratio_intHyperlinks', 'ratio_extHyperlinks', 'ratio_nullHyperlinks',
                    'nb_extCSS', 'ratio_intMedia', 'ratio_extMedia', 'sfh', 'login_form', 'iframe',
                    'popup_window', 'safe_anchor', 'onmouseover', 'right_clic', 'empty_title',
                    'domain_in_title', 'domain_with_copyright', 'submit_email', 'external_favicon', 'links_in_tags']:
            features[key] = 0

    try:
        redir_total = len(response.history)
        redir_int = sum(1 for r in response.history if hostname in r.url)
        redir_ext = redir_total - redir_int
        features['ratio_intRedirection'] = redir_int / redir_total if redir_total else 0
        features['ratio_extRedirection'] = redir_ext / redir_total if redir_total else 0
    except:
        features['ratio_intRedirection'] = 0
        features['ratio_extRedirection'] = 0

    # Basic error indication
    features['ratio_intErrors'] = int('404' in response.text or '403' in response.text) if 'response' in locals() else 0
    features['ratio_extErrors'] = 0

    # Other signals
    features['google_index'] = 0
    features['page_rank'] = 0
    features['url_numeric_domain'] = int(bool(re.search(r'\d', hostname)))
    features['url_numeric_path_length'] = sum(c.isdigit() for c in path)
    features['url_numeric_num_subdomains'] = hostname.count('.') - 1
    features['url_numeric_has_ip'] = features['ip']
    features['url_numeric_has_special_chars'] = int(bool(re.search(r'[^a-zA-Z0-9]', url)))

    print(url)
    print(features)
    print("Total features extracted:", len(features))
    return features
