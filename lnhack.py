import regex_match
import create_data
import ingester
import clf
import ModelLoad
import pandas as pd


# file_name = "/Users/saurabh/PycharmProjects/lnhack/SDRsample 2.xlsx"

def mode_of(DL, svm, nb, rgx):
    count_1 = 0
    if DL == 1:
        count_1 += 1
    if svm == 1:
        count_1 += 1
    if nb == 1:
        count_1 += 1
    if rgx == 1:
        count_1 += 2
    return 0 if count_1 < 2 else 1


def get_df_g():
    return pd.read_csv("/Users/saurabh/PycharmProjects/lnhack/glinks.csv")


def get_g_links(df):
    df_g = get_df_g()
    merge_df = pd.merge(df, df_g, on='query', how='outer')
    # merge_df['g_links'].fillna("", inplace=True)
    return merge_df


def get_crnl_links(df):
    df['crnl_links'] = df['query'].apply(lambda x: ingester.query_crnl_urls(x))
    return df


def main(file_name):
    query_rgx_out = regex_match.regex_matcher(file_name)
    print("Done with regex")
    df = pd.DataFrame(query_rgx_out)
    headers = ['query', 'r_1', 'r_2', 'r_3', 'r_4', 'r_5', 'r_6', 'r_7', 'r_8', 'r_9', 'r_10', 'r_11', 'r_12', 'r_13',
               'r_14', 'r_not']
    df.columns = headers
    enriched_df = create_data.feature_enrich(df)
    print("Done with enrichment", enriched_df.shape)
    enriched_df_cols = enriched_df.columns.values[1:]

    clf_out = clf.DL_prediction(enriched_df[['query']])
    print("Done with DL predictions", clf_out.shape)
    clf_out['regex'] = enriched_df.apply(
        lambda row: create_data.label(row["r_1"], row["r_2"], row["r_3"], row["r_4"], row["r_5"], row["r_6"],
                                      row["r_7"], row["r_8"], row["r_9"], row["r_10"], row["r_11"], row["r_12"]
                                      , row["r_13"], row["r_14"]), axis=1)
    clf_out['svm'] = ModelLoad.get_classifier_preds("finalized_model_SVM.sav", enriched_df[enriched_df_cols])
    print("Done with SVM predictions", clf_out.shape)
    clf_out['nb'] = ModelLoad.get_classifier_preds("finalized_model_GaussNB.sav", enriched_df[enriched_df_cols])
    print("Done with NB predictions", clf_out.shape)
    # clf_out['lr'] = ModelLoad.get_classifier_preds("finalized_model_LogisticRegression.sav",
    #                                                enriched_df[enriched_df_cols])

    clf_out['pred'] = clf_out.apply(lambda row: mode_of(row["prob_n"], row["svm"], row["nb"], row["regex"]), axis=1)
    clf_out.to_csv("preds.csv", index=False)
    print("Done with Final predictions", clf_out.shape)
    # semi_final = get_g_links(clf_out)
    # print("Done with getting google links predictions", semi_final.shape)
    final = get_crnl_links(clf_out)
    print("Done with getting cornell links predictions", final.shape)
    header = ["query", "pred", "crnl_links"]
    final.to_csv("final.csv", index=False, columns=header)


if __name__ == '__main__':
    file_name = "/Users/saurabh/PycharmProjects/lnhack/testset.csv"
    main(file_name)
