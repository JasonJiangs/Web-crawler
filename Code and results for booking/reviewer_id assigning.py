import pandas as pd
import numpy as np


df=pd.read_csv('./new_all_reviews.csv')
pd.set_option('display.width',1000)
pd.set_option('display.max_columns',None)
reviewers=df['Reviewer']
reviewers=reviewers.drop_duplicates(keep='first')
reviewers=pd.DataFrame({'Reviewer Id':np.arange(1,len(reviewers)+1),'Reviewer':reviewers})
reviewers.set_index(reviewers['Reviewer'],inplace=True)
item=reviewers['Reviewer Id'].to_dict()
print(item)
df['Reviewer Id']=df['Reviewer'].apply(lambda x:item[x])
reviewer_id=df['Reviewer Id']
df=df.drop(columns=['Reviewer Id'])
df.insert(1,'Reviewer Id',reviewer_id)
df.to_csv('alll_reviews.csv',index=False)



df2=pd.read_csv('./new_e_reviews.csv')
reviewers2=df2['Reviewer']
reviewers2=reviewers2.drop_duplicates(keep='first')
reviewers2=pd.DataFrame({'Reviewer Id':np.arange(1,len(reviewers2)+1),'Reviewer':reviewers2})
reviewers2.set_index(reviewers2['Reviewer'],inplace=True)
item2=reviewers2['Reviewer Id'].to_dict()

keys=list(item2.keys())
k_ls=list(item.keys())
n=len(k_ls)
for i in range(len(keys)):
    if keys[i] not in k_ls:
        n+=1
        print(n)
        item[keys[i]]=str(n)




df2['Reviewer Id']=df2['Reviewer'].apply(lambda x:item[x])
reviewer2_id=df2['Reviewer Id']
df2=df2.drop(columns=['Reviewer Id'])
df2.insert(1,'Reviewer Id',reviewer2_id)
df2.to_csv('en_reviews.csv',index=False)
