#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import collections
from collections import defaultdict


# In[2]:


df=pd.read_excel('complete_data.xlsx')  


# In[3]:


import xlsxwriter
workbook = xlsxwriter.Workbook('myfile.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write(0, 0,"states_name")
worksheet.write(0, 1,"positive")
worksheet.write(0, 2,"negative")
worksheet.write(0, 3,"neutral")


# In[4]:


def count_labels(df,total=0,i=1):
    all_states=set(df["Location"])
    for state in all_states:
        pos=0
        neg=0
        nut=0
        worksheet.write(i, 0,state)
        rows=df.index[df['Location'] == state].tolist()
        for row in rows:    
            if df.at[row,"Label"]== 1:   
                pos=pos+1
            if df.at[row,"Label"]== -1:    
                neg=neg+1
            if df.at[row,"Label"]==0:
                nut=nut+1
        total=pos+nut+neg
        state_dict[state]["positive"]=pos/total*100
        worksheet.write(i, 1,pos/total*100)
        state_dict[state]["negative"]=neg/total*100
        worksheet.write(i, 2,neg/total*100)
        state_dict[state]["neutral"]=nut/total*100
        worksheet.write(i, 3,nut/total*100)
        i=i+1
    workbook.close()
    return state_dict


# In[5]:


state_dict=defaultdict(lambda: defaultdict(int))
state_dict=count_labels(df)


# In[6]:


response=pd.read_excel('Data_for_map.xlsx',dtype={'sates_name': str, 'positive': float,'negative': float,"neutral":float})  


# In[7]:


response.head(5)


# In[ ]:




