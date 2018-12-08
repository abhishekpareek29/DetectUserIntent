import re
import openpyxl
import csv
import pandas as pd

# file_name = "SDRsample 2.xlsx"


def load_queries(file_name="/Users/saurabh/PycharmProjects/lnhack/testset.csv"):

    inp = pd.read_csv("/Users/saurabh/PycharmProjects/lnhack/testset.csv")
    queries = inp.iloc[:, 0].values.tolist()

    # wb = openpyxl.load_workbook(filename=file_name, read_only=True)
    #
    # column_index = 0
    # sheet_name = "SDRs"
    # sheet = wb[sheet_name]
    # query = []
    # for r in sheet.rows:
    #     try:
    #         q = str(r[column_index].value).replace(u'\xa7', 'section').replace("\"", "")
    #     except:
    #         q = r[column_index].value
    #     query.append(q)

    return queries

# df = pd.read_excel('Bad_Citation_Searches.xlsx', sheet_name = "YES SDR", dtype={'query':str})

rule_evi = 'rule[s]*\s*[\d\.\:\(\)a-z\-]+$|evidence code\s*[\d\.]+|business and professions code\s*[\d\.]+'
pen_Code_regex = 'penal code\s*[\d\.]+|pc\s*[\d\.]+|penal\s*[\d\.]+|pen code\s*[\d\.]+|pen[al]* code[\,]* section\s*[\(\)0-9\.a-z]$|penal law\s*[\d\.]+|pl\s*[\d\.]+'
ccp_reg = '^[cpralfe]+[rule]*\s*[section]*\s*[\(\)\da-z\.]+$'
number_reg = '^[0-9\.]+$|^[0-9\.]+\([a-z0-9]\)*$|^[0-9\.\-]+\([a-z0-9]+\)\([a-z0-9]+\)$|^[0-9\.\-]+\([a-z0-9]+\)\([a-z0-9]+\)\([a-z0-9]+\)$'
chap_art_fam = '^chapter\s*[0-9]+|^article\s*[0-9]+|^family code\s*[0-9]+|^civil code\s*[0-9]+|^labor code\s*[section]*\s*[0-9\.]+|^law\s*[0-9]+|^labor law\s*[0-9]+'
dash_separated = '^[0-9\.\-\:]+\-[0-9\.\(\)a-z]+\-*[0-9\.\(\)a-z]*$|^[a-z]+\-[0-9]+\-*[0-9]+$|^[a-z]+[0-9]+\-[0-9]+\-*[0-9]*$'
colon_dash_regex = '^[0-9a-z]+\:[0-9a-z]{0,4}\-*[0-9\:\.]{0,3}$'
alphanumeric_2_4_regex = '^[0-9a-z]{1,5}$'
ranking_regex = '^[0-9]+th$|^[0-9]+rd$|^[0-9]+nd$|^[0-9]+st$'
section_regex = '^section\s*.*'
vtl_regex = '^vtl\s*[0-9]{1,4}\.*'
title_regex = '^title\s*[0-9a-z]{1,4}'
probate_regex = 'prob[ate\.]*\s*[code]*\s*[\-\,]*[section]*\s*[0-9\.]{2,7}'
usc_sec_regex = '^[0-9]{1,3}\s*[uscp\.]*\s*[section\.]*\s*[0-9\-\.]+[\(0-9a-z\)]*'


# evi_reg = 'evidence code\s*[\d.]+'

# Take all the queries in a list
# query = list(df['query'])

def regex_matcher(file_name=None):
    que = []
    queries = load_queries(file_name)
    for q in queries:

        try:
            q = q.replace(u'\xa7', 'section').replace("\"", "").replace(":00", "")
        except:
            pass
        if str(q) == 'None':
            break
        # 1
        if re.findall(rule_evi, str(q), re.IGNORECASE):
            que.append(
                [str(re.findall(rule_evi, str(q), re.IGNORECASE)[0]), 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        # 2
        elif re.findall(ccp_reg, str(q), re.IGNORECASE):
            que.append(
                [str(re.findall(ccp_reg, str(q), re.IGNORECASE)[0]), 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        # 3
        elif re.findall(number_reg, str(q), re.IGNORECASE):
            que.append(
                [str(re.findall(number_reg, str(q), re.IGNORECASE)[0]), 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        # 4
        elif re.findall(chap_art_fam, str(q), re.IGNORECASE):
            que.append(
                [str(re.findall(chap_art_fam, str(q), re.IGNORECASE)[0]), 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        # 5
        elif re.findall(dash_separated, str(q), re.IGNORECASE):
            que.append(
                [str(re.findall(dash_separated, str(q), re.IGNORECASE)[0]), 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0])
        # 6
        elif re.findall(ranking_regex, str(q), re.IGNORECASE):
            que.append(
                [str(re.findall(ranking_regex, str(q), re.IGNORECASE)[0]), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        # 7
        elif re.findall(colon_dash_regex, str(q), re.IGNORECASE):
            que.append(
                [str(re.findall(colon_dash_regex, str(q), re.IGNORECASE)[0]), 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
                 0])
        # 8
        elif re.findall(alphanumeric_2_4_regex, str(q), re.IGNORECASE):
            que.append(
                [str(re.findall(alphanumeric_2_4_regex, str(q), re.IGNORECASE)[0]), 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
                 0,
                 0, 0])
        # 9
        elif re.findall(section_regex, str(q), re.IGNORECASE):
            que.append(
                [str(re.findall(section_regex, str(q), re.IGNORECASE)[0]), 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0])
        # 10
        elif re.findall(pen_Code_regex, str(q), re.IGNORECASE):
            que.append(
                [str(re.findall(pen_Code_regex, str(q), re.IGNORECASE)[0]), 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
                 0])
        # 11
        elif re.findall(vtl_regex, str(q), re.IGNORECASE):
            que.append(
                [str(re.findall(vtl_regex, str(q), re.IGNORECASE)[0]), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0])
        # 12
        elif re.findall(title_regex, str(q), re.IGNORECASE):
            que.append(
                [str(re.findall(title_regex, str(q), re.IGNORECASE)[0]), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0])
        # 13
        elif re.findall(probate_regex, str(q), re.IGNORECASE):
            que.append(
                [str(re.findall(probate_regex, str(q), re.IGNORECASE)[0]), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0])
        # 14
        elif re.findall(usc_sec_regex, str(q), re.IGNORECASE):
            que.append(
                [str(re.findall(usc_sec_regex, str(q), re.IGNORECASE)[0]), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0])
        # not
        else:
            que.append([str(q), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
    return que


if __name__ == '__main__':
    load_queries("")

# with open("regex_op.csv", "wb") as csv_file:
#     writer = csv.writer(csv_file, delimiter=',')
#     writer.writerow(
#         ['query', 'r_1', 'r_2', 'r_3', 'r_4', 'r_5', 'r_6', 'r_7', 'r_8', 'r_9', 'r_10', 'r_11', 'r_12', 'r_13', 'r_14',
#          'r_not'])
#     for line in que:
#         writer.writerow(line)
