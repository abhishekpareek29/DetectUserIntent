import pandas as pd
from googlesearch import search


def get_google_links(df):
    # df = pd.read_csv('data/lexis.csv')
    query = list(df['query'])
    q_link = {}

    get_query(q_link, query)

    i = 0
    for key, value in q_link.items():
        try:
            df.loc[i, 'google_fuzz_match_url'] = value
            i += 1
        except:
            continue
    return df
    # with open('links.csv', 'a') as f:
    #     df.to_csv(f, header=False)


def get_query(q_link, query):
    for q in query:
        try:
            q = q.replace(u'\xa7', "section")
        except:
            pass
        for j in search(str(q), num=1, stop=1, pause=2):
            q_link[q] = j


if __name__ == "__main__":
    get_google_links()
