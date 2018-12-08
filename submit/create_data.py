import pandas as pd
import re
from fuzzysearch import find_near_matches
from fuzzywuzzy import process

keywords = ["section", "code", "motion", "law", "article", "penal", "rule", "form", "exhibit", "act", "criminal",
            "probate", "chapter", "proposition"]

states_map = {'AL': 'Alabama', 'AK': 'Alaska', 'AS': 'American Samoa', 'AZ': 'Arizona', 'AR': 'Arkansas',
              'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'DC': 'District Of Columbia',
              'FM': 'Federated States Of Micronesia', 'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii',
              'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky',
              'LA': 'Louisiana', 'ME': 'Maine', 'MH': 'Marshall Islands', 'MD': 'Maryland', 'MA': 'Massachusetts',
              'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana',
              'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico',
              'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'MP': 'Northern Mariana Islands',
              'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PW': 'Palau', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico',
              'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas',
              'UT': 'Utah', 'VT': 'Vermont', 'VI': 'Virgin Islands', 'VA': 'Virginia', 'WA': 'Washington',
              'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'}

rule_book = ['AL Rule', 'Alabama Rule', 'AK Rule', 'Alaska Rule', 'AS Rule', 'American Samoa Rule', 'AZ Rule',
             'Arizona Rule', 'AR Rule', 'Arkansas Rule', 'CA Rule', 'California Rule', 'CO Rule', 'Colorado Rule',
             'CT Rule', 'Connecticut Rule', 'DE Rule', 'Delaware Rule', 'DC Rule', 'District Of Columbia Rule',
             'FM Rule',
             'Federated States Of Micronesia Rule', 'FL Rule', 'Florida Rule', 'GA Rule', 'Georgia Rule', 'GU Rule',
             'Guam Rule', 'HI Rule', 'Hawaii Rule', 'ID Rule', 'Idaho Rule', 'IL Rule', 'Illinois Rule', 'IN Rule',
             'Indiana Rule', 'IA Rule', 'Iowa Rule', 'KS Rule', 'Kansas Rule', 'KY Rule', 'Kentucky Rule', 'LA Rule',
             'Louisiana Rule', 'ME Rule', 'Maine Rule', 'MH Rule', 'Marshall Islands Rule', 'MD Rule', 'Maryland Rule',
             'MA Rule', 'Massachusetts Rule', 'MI Rule', 'Michigan Rule', 'MN Rule', 'Minnesota Rule', 'MS Rule',
             'Mississippi Rule', 'MO Rule', 'Missouri Rule', 'MT Rule', 'Montana Rule', 'NE Rule', 'Nebraska Rule',
             'NV Rule', 'Nevada Rule', 'NH Rule', 'New Hampshire Rule', 'NJ Rule', 'New Jersey Rule', 'NM Rule',
             'New Mexico Rule', 'NY Rule', 'New York Rule', 'NC Rule', 'North Carolina Rule', 'ND Rule',
             'North Dakota Rule', 'MP Rule', 'Northern Mariana Islands Rule', 'OH Rule', 'Ohio Rule', 'OK Rule',
             'Oklahoma Rule', 'OR Rule', 'Oregon Rule', 'PW Rule', 'Palau Rule', 'PA Rule', 'Pennsylvania Rule',
             'PR Rule',
             'Puerto Rico Rule', 'RI Rule', 'Rhode Island Rule', 'SC Rule', 'South Carolina Rule', 'SD Rule',
             'South Dakota Rule', 'TN Rule', 'Tennessee Rule', 'TX Rule', 'Texas Rule', 'UT Rule', 'Utah Rule',
             'VT Rule',
             'Vermont Rule', 'VI Rule', 'Virgin Islands Rule', 'VA Rule', 'Virginia Rule', 'WA Rule', 'Washington Rule',
             'WV Rule', 'West Virginia Rule', 'WI Rule', 'Wisconsin Rule', 'WY Rule', 'Wyoming Rule']


def rule_box(strs):
    for rule in rule_book:
        if process.extractOne(rule, strs)[1] > 90:
            return 1
    return 0


def calculate_num_upper_chars(strs):
    num_U = sum(c.isUpper() for c in strs)
    num_L = sum(c.isLower() for c in strs)
    num_d = strs.count('.')


def if_keyword(strs):
    num_keywords = 0
    for k in keywords:
        if k in strs.lower():
            num_keywords += 1
    if len(strs) < 30 and num_keywords >= 1:
        return 1
    elif 31 < len(strs) < 50 and num_keywords >= 2:
        return 1
    elif 50 < len(strs) < 100 and num_keywords >= 3:
        return 1
    elif len(strs) < 150 and num_keywords >= 5:
        return 1
    num_states = 0
    for k, v in states_map:
        if k in strs.lower() or v in strs.lower():
            num_states += 1
    if len(strs) < 30 and num_states >= 1 and num_keywords >= 1:
        return 1

    return 0


def if_only_num(strs):
    if len(strs) < 15:
        if re.match("^[0-9.:\-]", strs) is not None:
            if len(strs) < 6:
                return 1
            elif strs.count('.') >= 1 or strs.count(':') >= 1:
                return 1
        elif strs[0].isdigit() and calculate_num_characters(strs):
            return 1
    return 0


def calculate_num_characters(strs):
    numbers = sum(c.isdigit() for c in strs)
    alphas = sum(c.isalpha() for c in strs)
    return 1 if numbers > alphas else 0


def label(r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, y_n=0):
    # if r3 == 1:
    #     if str(r3).count('.') == 1 and len(str(r3)) >= 10:
    #         return 0
    if r1 == 1 or r2 == 1 or r3 == 1 or r4 == 1 or r5 == 1 or r6 == 1 or r7 == 1 or r8 == 1 or r9 == 1 or \
            r10 == 1 or r11 == 1 or r12 == 1 or r13 == 1 or r14 == 1:
        return 1
    else:
        return y_n


def main():
    input = pd.read_csv("/Users/saurabh/PycharmProjects/lnhack/regex_op-2.csv")

    ### enable for regex matcher for test cases
    # input = pd.DataFrame(regex_matcher())
    feature_enrich(input)
    # input['rule_fuzz'] = input["query"].apply(lambda x: rule_box(x))

    input_old = pd.read_csv("/Users/saurabh/PycharmProjects/lnhack/sdr_labeled-4.csv")
    input_old.columns = ["query", "y_n"]
    input_old.fillna(0, inplace=True)
    merge_df = pd.merge(input, input_old, on='query', how='outer')
    merge_df.fillna(0, inplace=True)
    merge_df['y_n'] = merge_df.apply(
        lambda row: label(row["r_1"], row["r_2"], row["r_3"], row["r_4"], row["r_5"], row["r_6"],
                          row["r_7"], row["r_8"], row["r_9"], row["r_10"], row["r_11"], row["r_12"]
                          , row["r_13"], row["r_14"], row["y_n"]), axis=1)
    merge_df["r_1"] = merge_df["r_1"].astype(int)
    merge_df["r_2"] = merge_df["r_2"].astype(int)
    merge_df["r_3"] = merge_df["r_3"].astype(int)
    merge_df["r_4"] = merge_df["r_4"].astype(int)
    merge_df["r_5"] = merge_df["r_5"].astype(int)
    merge_df["r_6"] = merge_df["r_6"].astype(int)
    merge_df["r_7"] = merge_df["r_7"].astype(int)
    merge_df["r_8"] = merge_df["r_8"].astype(int)
    merge_df["r_9"] = merge_df["r_9"].astype(int)
    merge_df["r_10"] = merge_df["r_10"].astype(int)
    merge_df["r_11"] = merge_df["r_11"].astype(int)
    merge_df["r_12"] = merge_df["r_12"].astype(int)
    merge_df["r_13"] = merge_df["r_13"].astype(int)
    merge_df["r_14"] = merge_df["r_14"].astype(int)
    merge_df["r_not"] = merge_df["r_not"].astype(int)
    merge_df["siz"] = merge_df["siz"].astype(int)
    merge_df["is_num"] = merge_df["is_num"].astype(int)
    merge_df["in_kwd"] = merge_df["in_kwd"].astype(int)
    merge_df["only_num"] = merge_df["only_num"].astype(int)
    # merge_df["rule_fuzz"] = merge_df["rule_fuzz"].astype(int)
    merge_df.to_csv('iter4.csv', index=False)

    header = ["query", "y_n"]
    merge_df.to_csv('iter_dl4.csv', index=False, columns=header)

    print("")


def feature_enrich(input):
    input['siz'] = input["query"].apply(lambda x: 1 if len(x) < 50 else 0)
    input['is_num'] = input["query"].apply(lambda x: calculate_num_characters(x))
    input['in_kwd'] = input["query"].apply(lambda x: if_keyword(x))
    input['only_num'] = input["query"].apply(lambda x: if_only_num(x))
    return input


# if __name__ == '__main__':
#     main()
