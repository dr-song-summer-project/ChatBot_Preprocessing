from numpy import spacing
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import nltk
import pandas as pd
from openpyxl import Workbook
from pykospacing import Spacing
from hanspell import spell_checker
from tqdm.notebook import tqdm
from soynlp.normalizer import *
import kss
import re
from IPython.display import display
import numpy as np

MAXSIZE = 10

path_sample = 'src/sample_short.xlsx'
path_training = 'src/categories.xlsx'


def spell_text(texts):
    sample_space = spacing(texts)
    # spelled_sent = spell_checker.check(sample_space)
    # sample_space_spell = spelled_sent.checked
    return sample_space


def process_sentence(texts):
    # chars = "<o:p/>"
    tmp = ''
    for sent_ in kss.split_sentences(texts):
        if ('안녕하세요' in sent_) or ('하이닥' in sent_) or ('감사합니다' in sent_) or (len(sent_)) > 500:
            continue
        tmp = tmp + ' ' + (spell_text(sent_))
        # print(spell_text(sent_), end=' ')
    # for i in range(len(chars)):
    #     tmp = tmp.replace(chars[i], "")
    tmp = tmp.replace("<br>", "")
    tmp = tmp.replace("<o:p>", "")
    tmp = tmp.replace("</o:p>", "")
    if tmp == "" or tmp == "  ":
        return "아직 작성되지 않았습니다."
    return tmp


def read_file(file_paths):  # ==파일 읽어오기
    df_ = pd.read_excel(file_paths)
    numpy = pd.DataFrame.to_numpy(df_)
    return df_, numpy


def classify(list_, text):
    i = 1
    correct = True
    print(text)
    ant = input("요약문을 입력하세요 : ")
    while correct:
        select = (input('0~%d중 분류를 입력하세요 : ' % (len(list_) - 1)).split())
        for j in range(len(select)):
            if int(select[j]) < len(list_) and select[j] != '':
                correct = False
            else:
                correct = True

    for k in range(len(select)):
        while category3[int(select[k])][i] != 0:
            i = i + 1
        category3[int(select[k])][i] = (text, ant)
    # print(category3[select])


# =============================================================

text_df, text_df_np = read_file(path_sample)  # 학습할 데이터
ct_df, ct_df_np = read_file(path_training)  # 데이터를 나눌 카테고리

# sentence_question = []
# sentence_answer = []
#
# for i in tqdm(range(0, len(text_df))):
#     sentence_question.append(process_sentence(text_df_np[i][1]))
#     sentence_answer.append(process_sentence(text_df_np[i][2]))

# =============================================================

data = pd.DataFrame()
standard = pd.DataFrame()
data['querys'] = text_df['질문']
standard['category3'] = ct_df['Category3']
# display(standard['category3'])

standard = standard[standard['category3'].notna()]
data = data[data['querys'].notna()]
category3 = [[0 for j in range(MAXSIZE)] for i in range(len(standard))]
tmp = standard['category3'].values.tolist()
Qst = data['querys'].values.tolist()

for i in range(len(standard['category3'])):
    category3[i][0] = tmp[i]
    print(i, '번 : ', category3[i][0], end=' ')

# =============================================================

annotation = []

for i in range(len(data['querys'])):
    classify(standard, Qst[i])

df = pd.DataFrame(category3)
df.to_excel('src/sample_classified.xlsx')