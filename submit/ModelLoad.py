import pandas as pd
from matplotlib import style

style.use("ggplot")

import pickle

# # Code to unload model
# loaded_model = pickle.load(open('finalized_model_SVM.sav', 'rb'))
# # result = loaded_model.score(X_test, Y_test)
# # print(result)
#
# # New data to predict
# pr = pd.read_csv('convertcsv.csv')
# pred_cols = list(pr.columns.values)[:-1]
#
# # apply the whole pipeline to data
# pred = pd.Series(loaded_model.predict(pr[pred_cols]))
# print(pred)


def get_classifier_preds(model_path, test):
    loaded_model = pickle.load(open(model_path, 'rb'))
    out_df = loaded_model.predict(test)
    return out_df
