import pandas as pd
import xlsxwriter
import os

if os.path.exists('en_f')==False:
    os.mkdir('en_f')

data=pd.read_csv('new_e_reviews.csv',low_memory=None)
columns=data.columns
lenth=(len(data)//60000)+1
i=0
while True:
    try:
        print(i)
        df=data.iloc[i:i+60000]
        filename='./en_f/{}_{}.xlsx'.format(str(i+1),str(i+60000))
        df.to_excel(filename,index=None,columns=columns,engine='xlsxwriter')
    except:
        print('即将结束')
        df = data.iloc[i:]
        filename = './en_f/{}_{}.xlsx'.format(str(i + 1), str(len(data)))
        df.to_excel(filename, index=None, columns=columns,engine='xlsxwriter')
    i+=60000
    if i>len(data):
        break
