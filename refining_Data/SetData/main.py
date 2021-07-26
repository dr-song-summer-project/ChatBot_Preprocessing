import numpy as np
import pandas as pd
import sys
from openpyxl import Workbook

file_path = 'src/clustered_질문요약_800_n20.xlsx'
path_save = 'src/QueryData/'

df = pd.read_excel(file_path)
data = pd.DataFrame()
annotation_Q = df['질문 요약'].tolist()
# annotation_A = df['답변 요약'].tolist()
Index = df['Index'].tolist()
label = df['labels'].tolist()

def write_file(index, path):
    f = open(path+str(Index[i])+'QueryData.txt','w')
    f.write(annotation_Q[index])
    f.close()
    print(index)


for i in range(len(annotation_Q)):
    write_file(i,path_save+(str(label[i]))+'\\')