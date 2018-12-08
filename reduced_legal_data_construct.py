import pandas as pd
from googlesearch import search

df = pd.read_csv('data/Bad_Citation_Searches.csv')
query = list(df['query'])
q_link = {}

for q in query:
    try:
        q = q.replace(u'\xa7', "section")
    except:
        pass
    for j in search(str(q), num=1, stop=1, pause=2):
        q_link[q] = j

i = 0
for key, value in q_link.items():
    df.loc[i, 'google_fuzz_match_url'] = j
    i += 1
with open('google_links.csv', 'a') as f:
    df.to_csv(f, header=False)
