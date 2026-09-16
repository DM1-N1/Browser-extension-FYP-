# Data augmentation script.
#
# WHY THIS EXISTS (see notes.txt for the full writeup):
# Analysis of dataset_phishing.csv showed the legitimate class is heavily
# skewed toward simple, query-string-free URLs: 96.6% of legitimate rows have
# zero '?' in the URL, vs only 76.2% of phishing rows. The model learned that
# having a query string with '=' / '&' at all is a mildly suspicious signal,
# which is true for THIS dataset's sample of legitimate sites but false in
# general - wikis, search engines, e-commerce, forums and docs sites all
# legitimately use query strings. This caused real legitimate pages such as
# Wikipedia's edit interface (?title=...&action=edit&section=4) to be
# misclassified as phishing.
#
# This script adds real, live, legitimate URLs that DO use query strings,
# spread across several unrelated domains/categories so the model isn't just
# learning "query strings are fine on wikipedia.org specifically". Features
# are extracted with the same extract_features_super() used by the live app,
# so the new rows are computed identically to how app.py would see them.

import pandas as pd
from feature_extractorv3 import extract_features_super

WIKI_TITLES = [
    'Python_(programming_language)', 'Artificial_intelligence', 'Climate_change',
    'World_War_II', 'Albert_Einstein', 'Machine_learning', 'Great_Barrier_Reef',
    'Renaissance', 'Quantum_mechanics', 'Photosynthesis', 'Solar_System',
    'Human_rights', 'Internet', 'DNA', 'Democracy',
]

WIKTIONARY_WORDS = [
    'hello', 'world', 'computer', 'science', 'love',
    'time', 'water', 'music', 'history', 'language',
]

SEARCH_TERMS = [
    'python', 'javascript', 'machine-learning', 'climate-change', 'cybersecurity',
    'react', 'docker', 'blockchain', 'data-science', 'linux',
]

YOUTUBE_IDS = [
    'dQw4w9WgXcQ', 'jNQXAC9IVRw', '9bZkp7q19f0', 'kJQP7kiw5Fk', 'JGwWNGJdvx8',
    '3JZ_D3ELwOQ', 'fJ9rUzIMcZQ', 'YQHsXMglC9A', 'RgKAFK5djSk', 'OPf0YbXqDm0',
]


def build_urls():
    urls = []

    for title in WIKI_TITLES:
        urls.append(f'https://en.wikipedia.org/w/index.php?title={title}&action=edit')
        urls.append(f'https://en.wikipedia.org/w/index.php?title={title}&action=history')
    for term in SEARCH_TERMS:
        urls.append(f'https://en.wikipedia.org/w/index.php?search={term}&title=Special:Search&fulltext=1')

    for word in WIKTIONARY_WORDS:
        urls.append(f'https://en.wiktionary.org/w/index.php?title={word}&action=edit')

    for vid in YOUTUBE_IDS:
        urls.append(f'https://www.youtube.com/watch?v={vid}&t=10s')

    for term in SEARCH_TERMS:
        urls.append(f'https://stackoverflow.com/search?q={term}')
        urls.append(f'https://github.com/search?q={term}&type=repositories')
        urls.append(f'https://old.reddit.com/search?q={term}')
        urls.append(f'https://developer.mozilla.org/en-US/search?q={term}')
        urls.append(f'https://www.npmjs.com/search?q={term}')
        urls.append(f'https://pypi.org/search/?q={term}')
        urls.append(f'https://html.duckduckgo.com/html/?q={term}')
        urls.append(f'https://arxiv.org/search/?searchtype=all&query={term}')
        urls.append(f'https://www.ebay.com/sch/i.html?_nkw={term}')
        urls.append(f'https://www.imdb.com/find/?q={term}')
        urls.append(f'https://search.usa.gov/search?query={term}&affiliate=usagov')

    return list(dict.fromkeys(urls))  # de-dupe, keep order


def main():
    no_url_path = 'datasets/dataset_no_url.csv'
    with_url_path = 'datasets/dataset_with_url.csv'

    dataset_no_url = pd.read_csv(no_url_path)
    dataset_with_url = pd.read_csv(with_url_path)

    with_url_feature_cols = [c for c in dataset_with_url.columns if c != 'status']
    no_url_feature_cols = [c for c in dataset_no_url.columns if c != 'status']

    urls = build_urls()
    new_with_url_rows = []
    new_no_url_rows = []
    failed = []

    for i, url in enumerate(urls, 1):
        try:
            feats = extract_features_super(url)
            row_with = {c: feats.get(c, 0) for c in with_url_feature_cols}
            row_with['status'] = 0
            row_no = {c: feats.get(c, 0) for c in no_url_feature_cols}
            row_no['status'] = 0
            new_with_url_rows.append(row_with)
            new_no_url_rows.append(row_no)
            print(f'[{i}/{len(urls)}] OK   {url}')
        except Exception as e:
            failed.append((url, str(e)))
            print(f'[{i}/{len(urls)}] FAIL {url}: {e}')

    print()
    print(f'Processed {len(new_with_url_rows)}/{len(urls)} URLs successfully, {len(failed)} failed.')

    if new_with_url_rows:
        dataset_with_url = pd.concat(
            [dataset_with_url, pd.DataFrame(new_with_url_rows)[dataset_with_url.columns]],
            ignore_index=True,
        )
        dataset_no_url = pd.concat(
            [dataset_no_url, pd.DataFrame(new_no_url_rows)[dataset_no_url.columns]],
            ignore_index=True,
        )
        dataset_with_url.to_csv(with_url_path, index=False)
        dataset_no_url.to_csv(no_url_path, index=False)
        print('Saved updated dataset_with_url.csv and dataset_no_url.csv.')

    if failed:
        print()
        print('Failed URLs (skipped):')
        for u, e in failed:
            print(' -', u, '|', e)


if __name__ == '__main__':
    main()
