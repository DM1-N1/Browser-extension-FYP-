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



# Ask wether to have path extension as always 0 or suttin else

def extract_features(url):
    parsed_url = urlparse(url)
    
    # Extract URL features
    features = {}
    
    # Length of URL
    features['length_url'] = len(url)
    
    # Number of dots in the URL
    features['nb_dots'] = parsed_url.netloc.count('.')
    
    # Number of hyphens in the URL
    features['nb_hyphens'] = url.count('-')
    
    # Number of "@" symbols in the URL
    features['nb_at'] = url.count('@')
    
    # Number of question marks in the URL
    features['nb_qm'] = url.count('?')
    
    # Number of "and" operators in the URL (for logical comparisons)
    features['nb_and'] = url.count('&')
    
    # Number of "or" operators in the URL (for logical comparisons)
    features['nb_or'] = url.count('|')
    
    # Number of equal signs in the URL
    features['nb_eq'] = url.count('=')
    
    # Number of underscores in the URL
    features['nb_underscore'] = url.count('_')
    
    # Number of tildes (~)
    features['nb_tilde'] = url.count('~')
    
    # Percentage of digits in the URL
    features['nb_percent'] = url.count('%')
    
    # Number of slashes in the URL
    features['nb_slash'] = url.count('/')
    
    # Number of stars (*) in the URL
    features['nb_star'] = url.count('*')
    
    # Number of colons (:) in the URL
    features['nb_colon'] = url.count(':')
    
    # Number of commas in the URL
    features['nb_comma'] = url.count(',')
    
    # Number of semicolons in the URL
    features['nb_semicolumn'] = url.count(';')
    
    # Number of dollar signs in the URL
    features['nb_dollar'] = url.count('$')
    
    # Number of spaces in the URL
    features['nb_space'] = url.count(' ')
    
    # Number of "www" in the URL
    features['nb_www'] = url.count('www')
    
    # Number of ".com" in the URL
    features['nb_com'] = url.count('.com')
    
    # Number of slashes ("//") in the URL
    features['nb_dslash'] = url.count('//')
    
    # Other features
    features['http_in_path'] = 1 if 'http' in parsed_url.path else 0
    features['https_token'] = 1 if 'https' in parsed_url.scheme else 0
    features['punycode'] = 1 if re.search(r'xn--', parsed_url.netloc) else 0
    
    # Number of subdomains in the domain
    features['nb_subdomains'] = parsed_url.netloc.count('.') - 1
    
    # Length of the URL path
    features['url_numeric_path_length'] = len(parsed_url.path)
    
    # Extract the domain name and perform additional feature extraction
    features['url_numeric_domain'] = parsed_url.netloc
    
    return features