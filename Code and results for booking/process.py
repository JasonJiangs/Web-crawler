#-*- coding=utf-8 -*-
#@time : 2021/1/8 下午12:24
#@Author : WuErShan
#@File : read.py
#@Software : PyCharm


import pandas as pd
import numpy as np

# 读取酒店信息，并将酒店id设为索引
df=pd.read_csv('./new_data.csv')
df.set_index(df['Hotel_id'],inplace=True)
# 将关键词与关键词id转制并导出为字典
words=(df.iloc[:,10:]).T
d=words.to_dict()
print(d)

# 将酒店关键字设为索引
a={}
for key,value in d.items():
    a[key]={value:key for key,value in value.items()}
print(a)

# 读取酒店评论，去重，并将酒店id设为索引
df2=(pd.read_csv('./all_reviews.csv'))
df2=df2.drop_duplicates(keep='first')
df2.set_index(df2['Hotel_id'],inplace=True)

# 提取标题和两个内容
content=df2[['Hotel_id','Title','Smile Content','Cry Content']]

content['full']=content.apply(lambda x:str(x['Title'])+str(x['Smile Content']+str(x['Cry Content'])),axis=1)
contents=content[['Hotel_id','full']]


# 遍历内容，提取关键词id、数量、binary数据
data=[]
nums=[]
binary=[]
for c in range(len(contents)):
    ls=[]
    print(c)
    try:
        id=contents['Hotel_id'].iloc[c]
        content=contents['full'].iloc[c]
        key_dict=a[id]
        keys=key_dict.keys()
        for key in keys:
            if key in str(content):
                ls.append(key_dict[key])
    except:
        ls=[]

    num=len(ls)
    if num !=0:
        bi=1

    else:

        bi=0



    data.append(','.join(ls))
    nums.append(num)
    binary.append(bi)

df2['Mentions Binary']=binary
df2['Mentions Number']=nums
df2['Mentions Id']=data
df2.to_csv('./new_all_reviews.csv',index=False)



if __name__ == '__main__':
    pass
