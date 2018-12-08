import pandas as pd
import requests
import urllib.parse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from fuzzysearch import find_near_matches
from fuzzywuzzy import process
import time

base_url = "https://www.law.cornell.edu/search/site/"

"""
https://stackoverflow.com/questions/17740833/checking-fuzzy-approximate-substring-existing-in-a-longer-string-in-python
"""


def if_true(lst):
    # print(lst)
    for l in lst[:5]:
        if l == 1:
            return 1
    return 0


def fuzzy_extract(qs, ls, threshold):
    '''fuzzy matches 'qs' in 'ls' and returns list of
    tuples of (word,index)
    '''
    for word, _ in process.extractBests(qs, (ls,), score_cutoff=threshold):
        # print('word {}'.format(word))
        for match in find_near_matches(qs, word, max_l_dist=10):
            match = word[match.start:match.end]
            # print('match {}'.format(match))
            index = ls.find(match)
            yield (match, index)


def fuzzy_match(sdr, row):
    # print(sdr, row)
    text_a, text_p = row[0], row[1]
    fuzzy_dist_a = []
    fuzzy_dist_p = []
    for a in text_a:
        try:
            # print(list(fuzzy_extract(sdr, a, 50)))
            fuzzy_dist_a.append(1 if (len(a) > 5 and len(list(fuzzy_extract(sdr, a, 50))) > 0) else 0)
        except:
            fuzzy_dist_a.append(0)

    for p in text_p:
        try:
            # print(list(fuzzy_extract(sdr, p, 50)))
            fuzzy_dist_p.append(1 if (len(p) > 5 and len(list(fuzzy_extract(sdr, p, 50))) > 0) else 0)
        except:
            fuzzy_dist_p.append(0)

    return if_true(fuzzy_dist_a) or if_true(fuzzy_dist_p)


def request_data(sdr):
    # r_url = requests.get(base_url + urllib.parse.quote_plus(sdr))
    # print(r_url)
    # data = r_url.text
    page = urlopen(base_url + urllib.parse.quote_plus(sdr))
    soup = BeautifulSoup(page, 'html.parser')
    name_box = soup.find(attrs={'class': 'search-results apachesolr_search-results'})
    if name_box is None:
        return [], []
    text_a = [s.get('href').strip() + '|' + s.getText().strip() for s in name_box.findAll('a', href=True)]
    text_p = [s.getText().strip() for s in name_box.findAll('p')]

    return text_a, text_p


def get_crnl(df):
    queries = df["sdr"].values
    print("len", len(queries))
    result = []
    count = 0
    max_count = 1208
    for q in queries:
        print(count)
        count = count + 1
        if count < max_count:
            continue
        try:
            text_a, text_p = request_data(q)
            if text_a is not None and len(text_a) > 0:
                text_a = '##'.join(text_a)
            else:
                text_a = ""
            if text_p is not None and len(text_p):
                text_p = '##'.join(text_p)
            else:
                text_p = ""
            result.append(','.join([q, text_a, text_p]))
            if count % 100 == 0:
                with open("crnl.csv", "a") as f:
                    for r in result:
                        f.write('\n' + r)
                # time.sleep(0.01)
                result = []
            # if count == 10:
            #     break
        except:
            print("except", count)
            continue


def main():
    # input = pd.read_csv("/Users/saurabh/Downloads/Bad_Citation_Searches.csv")
    # input.columns = ["query", "y_n"]
    # input_s = input.sample(5)
    # get_crnl(input)
    # try:
    #     input['cornell'] = input["sdr"].apply(lambda row: request_data(row))
    # except:
    #     pass
    # input.to_csv('sdr.csv', index=False)
    # data = []
    n_i = pd.read_fwf("/Users/saurabh/PycharmProjects/lnhack/crnl.csv")
    n_i.drop(n_i.columns[1:], axis=1, inplace=True)
    n_i.columns = ["data"]
    n_i['query'] = n_i['data'].apply(lambda x: query_split(x))
    n_i['y_n'] = n_i['data'].apply(lambda x: get_crnl_label(x))
    # with open("/Users/saurabh/PycharmProjects/lnhack/crnl.csv") as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         data.append(get_crnl_label(line))
    # print(len(data))
    # print(crnl_df.head(5))
    # merge_df = pd.merge(n_i, input, on='query', how='left')
    header = ["query", "y_n"]
    n_i.to_csv('sdr_labeled-1.csv', index=False, columns=header)
    print("")
    print("")


def query_split(data):
    line_split = data.split(',', 1)
    return line_split[0]


def get_crnl_label(line):
    line_split = line.split(',', 1)
    query = line_split[0]
    text_a_href = line_split[1]
    text_p = ""
    if len(line_split) > 2:
        text_p = line_split[2]
    if text_a_href is not None and len(text_a_href) > 1:
        text_a_href_split = text_a_href.split('##')
        text_a = []
        for txts in text_a_href_split:
            if '|' in text_a_href_split:
                text_a.append(txts.split('|')[1])
            else:
                text_a.append(txts)
        text_p_split = []
        if text_p != "":
            text_p_split = text_p.split('##')
        label = fuzzy_match(query, (text_a, text_p_split))
        return label
    else:
        return 0


if __name__ == '__main__':
    # print(request_data("22A:1-4"))
    # print(get_crnl_label(
    #     "501.204,https://www.law.cornell.edu/wex/inbox/florida|Florida##https://www.law.cornell.edu/topn/chief_financial_officers_act_of_1990|Chief Financial Officers Act of 1990,forth in Florida Statutes Title XXXIII, Chapter 501, Part II (§ 501.204).   Remedies include significant ...##Chief Financial Officers Act of 1990 Pub. L. 101-576, Nov. 15, 1990, 104 Stat. 2838  ..."))
    main()
