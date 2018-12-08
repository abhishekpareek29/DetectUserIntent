import numpy as np
import pandas as pd
from keras.models import load_model

maxlen = 30
labels = 2

model = load_model('/Users/saurabh/PycharmProjects/lnhack/origin_model4')
char_index = {'2': 0, '#': 1, '3': 2, 'I': 3, '-': 4, ';': 5, 'm': 6, 't': 7, 'F': 8, "'": 9, 'W': 10, 'B': 11, '4': 12,
              'x': 13, '`': 14, 'Q': 15, 'c': 16, 'END': 17, 'V': 18, 'T': 19, '[': 20, 'N': 21, '\\': 22, 'r': 23,
              'n': 24, 'l': 25, '&': 26, 'D': 27, 'p': 28, '1': 29, 'K': 30, 'a': 31, 'C': 32, '6': 33, '7': 34,
              'O': 35, 'E': 36, '*': 37, 'y': 38, '!': 39, ' ': 40, 'd': 41, 'R': 42, '§': 43, 'j': 44, 'w': 45,
              'i': 46, 'L': 47, 'z': 48, '"': 49, 'q': 50, 'h': 51, 'A': 52, '9': 53, '?': 54, 'g': 55, '5': 56,
              'k': 57, 's': 58, ')': 59, 'e': 60, 'X': 61, ']': 62, 'J': 63, '(': 64, '$': 65, ',': 66, 'P': 67,
              'S': 68, 'o': 69, 'f': 70, '+': 71, 'H': 72, 'Y': 73, 'u': 74, 'M': 75, 'U': 76, 'Z': 77, '0': 78,
              '.': 79, 'b': 80, '_': 81, '8': 82, 'v': 83, 'G': 84, ':': 85, '%': 86, '@': 87}


def DL_prediction_str(strs):
    df = pd.DataFrame([strs])
    return DL_prediction(df)


def DL_prediction(input):
    model = load_model('/Users/saurabh/PycharmProjects/lnhack/origin_model44')
    char_index = {'2': 0, '#': 1, '3': 2, 'I': 3, '-': 4, ';': 5, 'm': 6, 't': 7, 'F': 8, "'": 9, 'W': 10, 'B': 11,
                  '4': 12,
                  'x': 13, '`': 14, 'Q': 15, 'c': 16, 'END': 17, 'V': 18, 'T': 19, '[': 20, 'N': 21, '\\': 22, 'r': 23,
                  'n': 24, 'l': 25, '&': 26, 'D': 27, 'p': 28, '1': 29, 'K': 30, 'a': 31, 'C': 32, '6': 33, '7': 34,
                  'O': 35, 'E': 36, '*': 37, 'y': 38, '!': 39, ' ': 40, 'd': 41, 'R': 42, '§': 43, 'j': 44, 'w': 45,
                  'i': 46, 'L': 47, 'z': 48, '"': 49, 'q': 50, 'h': 51, 'A': 52, '9': 53, '?': 54, 'g': 55, '5': 56,
                  'k': 57, 's': 58, ')': 59, 'e': 60, 'X': 61, ']': 62, 'J': 63, '(': 64, '$': 65, ',': 66, 'P': 67,
                  'S': 68, 'o': 69, 'f': 70, '+': 71, 'H': 72, 'Y': 73, 'u': 74, 'M': 75, 'U': 76, 'Z': 77, '0': 78,
                  '.': 79, 'b': 80, '_': 81, '8': 82, 'v': 83, 'G': 84, ':': 85, '%': 86, '@': 87}
    cha_ind_len = len(char_index)
    # input = pd.read_csv("origin_in.csv", header=None)
    # input = pd.read_csv("/Users/saurabh/Downloads/Bad_Citation_Searches.csv")

    input.columns = ['name']
    trunc_test_name = [str(i)[0:maxlen] for i in input.name]
    test = np.asarray(name_matrix(trunc_test_name, char_index, maxlen, cha_ind_len))

    # predcition
    evals = model.predict(test)
    prob_m = [1 if i[0] > 0.5 else 0 for i in evals]

    out = pd.DataFrame(prob_m)
    out['query'] = input.name.reset_index()['name']
    out.columns = ['prob_n', 'query']

    return out


def get_name_mat(char_index, name):
    trunc_name = [i[0:maxlen] for i in name]
    X = name_matrix(trunc_name, char_index, maxlen)
    return X


def tag_origin(n_or_f):
    result = []
    for elem in n_or_f:
        if elem == 'n':
            result.append([1, 0])
        else:
            result.append([0, 1])
    return result


def name_matrix(trunc_name_input, char_index_input, maxlen_input, cha_ind_len):
    result = []
    for i in trunc_name_input:
        tmp = [set_flag(char_index_input[j], cha_ind_len) for j in str(i)]
        for k in range(0, maxlen_input - len(str(i))):
            tmp.append(set_flag(char_index_input["END"], cha_ind_len))
        result.append(tmp)
    return result


def set_flag(i, cha_ind_len):
    tmp = np.zeros(cha_ind_len)
    tmp[i] = 1
    return tmp

#
# if __name__ == '__main__':
#     DL_prediction(pd.DataFrame(["22 nycrr"]))
