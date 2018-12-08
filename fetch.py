import numpy as np
import pandas as pd
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.core import Activation, Dropout
from keras.models import Sequential

maxlen = 30
labels = 2
# cha_ind_len = 89


def main():
    # input = pd.read_csv("origin_in.csv", header=None)
    input = pd.read_csv("/Users/saurabh/PycharmProjects/lnhack/iter_dl4.csv")

    input.columns = ['name', 'n_or_f']

    print(input.groupby('n_or_f')['name'].count())

    names = input['name']
    # origin = input['n_or_f']
    vocab = set(' '.join([str(i) for i in names]))
    vocab.add('END')
    len_vocab = len(vocab)

    char_index = dict((c, i) for i, c in enumerate(vocab))
    cha_ind_len = len(char_index)
    print(char_index)
    # dummy_false = input[input['n_or_f'] == 0]
    # dummy_true = input[input['n_or_f'] == 1]
    # input_sample = dummy_false.append(dummy_true[:500])
    input_sample = input
    print(input_sample.groupby('n_or_f')['name'].count())

    # change these lines to remove sample
    msk = np.random.rand(len(input_sample)) < 0.8
    train = input_sample[msk]
    test = input_sample[~msk]

    print(test.groupby('n_or_f')['name'].count())
    print(train.groupby('n_or_f')['name'].count())

    trunc_train_name = [str(i)[0:maxlen] for i in train.name]
    train_X = np.asarray(name_matrix(trunc_train_name, char_index, maxlen, cha_ind_len))
    train_Y = np.asarray(tag_origin(train.n_or_f))

    trunc_test_name = [str(i)[0:maxlen] for i in test.name]
    test_X = np.asarray(name_matrix(trunc_test_name, char_index, maxlen, cha_ind_len))
    test_Y = np.asarray(tag_origin(test.n_or_f))

    # keras Sequential model
    model = Sequential()
    model.add(LSTM(124, return_sequences=True, input_shape=(maxlen, len_vocab)))
    model.add(Dropout(0.2))
    model.add(LSTM(124, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(2, activation='sigmoid'))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    batch_size = 500
    model.fit(train_X, train_Y, batch_size=batch_size, nb_epoch=15, validation_split=0.2)
    model.save('origin_model44', overwrite=True, include_optimizer=True)

    score, acc = model.evaluate(test_X, test_Y)
    print('Test score:', score)
    print('Test accuracy:', acc)

    # predcition
    name = ["26(b)(4)(D)", "atl3(\"securities\")",
            "§ 303.131 Proceedings for Temporary Restraining Order and Order to Show Cause re Preliminary Injunction [Code Civ. Proc. § 527]%2014Ex Parte Application, Supporting Declaration and Declaration re Notice [Cal. Rules of Ct., Rule 3.1200 et seq.]",
            "danger to community bail reform act 924(c)", "\"Rule 11\"", "2984.4",
            "What are the elements of title vii of civil rights act of 1944"]
    trunc_name = [i[0:maxlen] for i in name]
    X = name_matrix(trunc_name, char_index, maxlen, cha_ind_len)

    pred = model.predict(np.asarray(X))
    print(pred.tolist())

    # save our model and data
    train.to_csv("train_split.csv")
    test.to_csv("test_split.csv")

    evals = model.predict(test_X)
    prob_m = [i[0] for i in evals]

    out = pd.DataFrame(prob_m)
    out['name'] = test.name.reset_index()['name']
    out['n_or_f'] = test.n_or_f.reset_index()['n_or_f']

    out.head(10)
    out.columns = ['prob_n', 'name', 'actual']
    out.head(10)
    out.to_csv("origin_pred_out.csv")


def tag_origin(n_or_f):
    result = []
    for elem in n_or_f:
        if elem == 1:
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


if __name__ == '__main__':
    main()
