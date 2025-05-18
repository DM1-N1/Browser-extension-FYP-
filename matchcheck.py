import pandas as pd

def compare_features(dataset, json_features, feature_order):
    comparison_results = []
    for index, row in dataset.iterrows():
        row_results = {}
        for feature in feature_order:
            dataset_value = row.get(feature)
            json_value = json_features.get(feature)
            row_results[feature] = (dataset_value == json_value)
        comparison_results.append(row_results)
    return comparison_results

dataset_with_url = pd.read_csv('datasets/dataset_with_url.csv')

json_features = {'length_url': 104, 'length_hostname': 10, 'ip': 0, 'nb_dots': 1, 'nb_hyphens': 10, 'nb_at': 0, 'nb_qm': 0, 'nb_and': 0, 'nb_or': 0, 'nb_eq': 0, 'nb_underscore': 0, 'nb_tilde': 0, 'nb_percent': 0, 'nb_slash': 6, 'nb_star': 0, 'nb_colon': 1, 'nb_comma': 0, 'nb_semicolumn': 0, 'nb_dollar': 0, 'nb_space': 0, 'nb_www': 0, 'nb_com': 1, 'nb_dslash': 1, 'http_in_path': 0, 'https_token': 0, 'ratio_digits_url': 0.07692307692307693, 'ratio_digits_host': 0.0, 'punycode': 0, 'port': 0, 'tld_in_path': 0, 'tld_in_subdomain': 0, 'abnormal_subdomain': 0, 'nb_subdomains': 1, 'prefix_suffix': 0, 'random_domain': 0, 'shortening_service': 0, 'nb_redirection': 0, 'nb_external_redirection': 0, 'length_words_raw': 14, 'char_repeat': 0, 'shortest_word_host': 6, 'shortest_word_path': 2, 'longest_words_raw': 10, 'longest_word_host': 6, 'longest_word_path': 10, 'avg_words_raw': 5.571428571428571, 'avg_word_host': 6.0, 'avg_word_path': 5.538461538461538, 'phish_hints': 1, 'domain_in_brand': 0, 'brand_in_subdomain': 0, 'brand_in_path': 0, 'suspecious_tld': 0, 'statistical_report': 0, 'nb_hyperlinks': 0, 'ratio_intHyperlinks': 0, 'ratio_extHyperlinks': 0, 'ratio_nullHyperlinks': 0, 'nb_extCSS': 0, 'ratio_intRedirection': 0, 'ratio_extRedirection': 0, 'ratio_intErrors': 0, 'ratio_extErrors': 0, 'links_in_tags': 0, 'ratio_intMedia': 0, 'ratio_extMedia': 0, 'popup_window': 0, 'safe_anchor': 0, 'onmouseover': 0, 'right_clic': 0, 'empty_title': 1, 'url_numeric_path_length': 8, 'url_numeric_num_subdomains': 0, 'url_numeric_has_ip': 0, 'url_numeric_has_special_chars': 1}

feature_order = ['length_url', 'length_hostname', 'ip', 'nb_dots', 'nb_hyphens', 'nb_at',
       'nb_qm', 'nb_and', 'nb_or', 'nb_eq', 'nb_underscore', 'nb_tilde',
       'nb_percent', 'nb_slash', 'nb_star', 'nb_colon', 'nb_comma',
       'nb_semicolumn', 'nb_dollar', 'nb_space', 'nb_www', 'nb_com',
       'nb_dslash', 'http_in_path', 'https_token', 'ratio_digits_url',
       'ratio_digits_host', 'punycode', 'port', 'tld_in_path',
       'tld_in_subdomain', 'abnormal_subdomain', 'nb_subdomains',
       'prefix_suffix', 'random_domain', 'shortening_service',
       'nb_redirection', 'nb_external_redirection', 'length_words_raw',
       'char_repeat', 'shortest_word_host', 'shortest_word_path',
       'longest_words_raw', 'longest_word_host', 'longest_word_path',
       'avg_words_raw', 'avg_word_host', 'avg_word_path', 'phish_hints',
       'domain_in_brand', 'brand_in_subdomain', 'brand_in_path',
       'suspecious_tld', 'statistical_report', 'nb_hyperlinks',
       'ratio_intHyperlinks', 'ratio_extHyperlinks', 'ratio_nullHyperlinks',
       'nb_extCSS', 'ratio_intRedirection', 'ratio_extRedirection',
       'ratio_intErrors', 'ratio_extErrors', 'links_in_tags', 'ratio_intMedia',
       'ratio_extMedia', 'popup_window', 'safe_anchor', 'onmouseover',
       'right_clic', 'empty_title', 'url_numeric_path_length',
       'url_numeric_num_subdomains', 'url_numeric_has_ip',
       'url_numeric_has_special_chars']

# call the function
results = compare_features(dataset_with_url, json_features, feature_order)



# results is a list of dicts with True/False per feature per row
for i, res in enumerate(results):
    print(f"Row {i} comparison:")
    for feature, match in res.items():
        print(f"  {feature}: {'Match' if match else 'Mismatch'}")


