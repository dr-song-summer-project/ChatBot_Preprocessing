import requests
import pandas as pd


proxies = {
    'http': 'http://220.149.25.33:80', #free proxy
    'https': 'http://220.149.25.33:80',
}

start = 1500
end = 1600

def get_excel(path):
    df_ = pd.read_excel(path)
    data = pd.DataFrame()
    querys = df_['질문 요약'].values.tolist()
    answers = df_['답변 요약'].values.tolist()
    Index = []
    result_Q = []
    result_A = []
    for i in range(start, end):
        if (len(querys[i]) < 30) and (("누락" not in querys[i]) and ("누락" not in answers[i])):
            # print(querys[i])
            Index.append(i)
            result_Q.append((querys[i]))
            result_A.append(answers[i])
    return Index, result_Q, df_


def get_translate(text):
    client_id = "client_id" # <-- client_id 기입
    client_secret = "client_secret" # <-- client_secret 기입

    data = {'text' : text,
            'source' : 'ko',
            'target': 'ja'}



    url = "https://openapi.naver.com/v1/papago/n2mt"

    header = {"X-Naver-Client-Id":client_id,
              "X-Naver-Client-Secret":client_secret}

    # response = requests.post(url, headers=header, data=data, proxies=proxies)
    response = requests.post(url, headers=header, data=data)
    rescode = response.status_code

    trans_data = "알 수 없는 오류"

    if(rescode==200):
        send_data = response.json()
        trans_data = (send_data['message']['result']['translatedText'])
        # return trans_data
    else:
        print("Error Code:" , rescode)

    data_reuslt = {'text': trans_data,
                   'source': 'ja',
                   'target': 'ko'}
    response = requests.post(url, headers=header, data=data_reuslt, proxies=proxies)
    rescode = response.status_code

    if (rescode == 200):
        send_data = response.json()
        trans_data_ = (send_data['message']['result']['translatedText'])
        return trans_data_
    else:
        print("Error Code:", rescode)

Index, Question, Df = get_excel('src/요약본_4000개_원본_파파고.xlsx')

# result_Df  = pd.Series(index=['질문', '질문 요약', '답변', '답변 요약'])
result_Df = pd.DataFrame()

trans = []
for i in range (0, len(Index)):
    trans.append(get_translate(Question[i]))
    #trans.append(i)
    print(trans[i])


for i in range (0, len(Index)):
    result_Df = result_Df.append(Df.loc[Index[i], ['질문', '질문 요약', '답변', '답변 요약']])

result_Df['질문 요약'] = trans
result_Df.to_excel(f'src/translated{start}to{end}.xlsx')
