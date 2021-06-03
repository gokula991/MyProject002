#!/usr/bin/env python
# coding: utf-8

# <h1> IMDB :Web Scraping  <h1>

# <h2> By K. Gokula Chandra <h2>
# <h3> Date : 03-06-21<h3>
# <p> In this notebook ,am gonna perform Data Scraping from web(IMDB,It's an website of movie reviews and information.)</p>

# <p> Here, we use BeautifulSoup library(in-built) for structuring data and also we can acheive the former action with help of json library through API(Application Programming Interface</p>
# <p>First things First, lets import required packages/libraries</p>

# In[3]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sns
import json
from datetime import date
import matplotlib.pyplot as plt
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


# <p>The following function helps us to:<br>
#     *) It takes parmeters year and count,the number of movies and year for the process of extraction.<br>
#     *)If the given year is the current year then it will process upto present day else the entire year(Limitation)<br>
#     *) This function gets the data from web and converts into html file with BeautifulSoup library and the data is transformed into an dataframe using pandas library and the dataframe is returned<br>
#     </p>

# In[15]:


def myfunction(year,count):
    movies=[]
    genre=[]
    ids=[]
    rating=[]
    runtime=[]
    certify=[]
    review=[]
    current=date.today().strftime("%Y-%m-%d")
    start="{}-01-01".format(year)
    y=int(str(current).split('-')[0])
    if year==y:
        end=current
    else:
        end='{}-12-31'.format(year)
    url = 'https://www.imdb.com/search/title/?title_type=feature&release_date={s},{e}&languages=en&adult=include&count={c}'.format(s=start,e=end,c=count)
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    res=session.get(url)
    res=requests.get(url)
    data=BeautifulSoup(res.text,'html')
    for i in data.find("body").find_all("div",{"class":"lister-item-content"}):
        for j in i.find_all("h3"):
            m_temp=j.find("a").text
        for j in i.find_all("strong"):
            r_temp=float(j.text)
        for j in i.find_all("span",{"class":"genre"}):
            t=[]
            for k in str(j.text).split(','):
                t.append(k.strip())
            g_temp=t
        for j in i.find_all("h3"):
            i_temp=str(j.find("a")).split('/')[2]
        for j in i.find_all("span",attrs={"class":"runtime"}):
            ru_temp=str(j.text).split(' ')[0]
        for j in i.find_all("span",{"class":"certificate"}):
            c_temp=str(j.text)
        for j in i.find_all("meta",{"itemprop":"ratingCount"}):
            re_temp=int(str(j).split("\"")[1])
        if m_temp and r_temp and g_temp and i_temp and ru_temp and c_temp and re_temp:
            movies.append(m_temp)
            genre.append(g_temp)
            rating.append(r_temp)
            ids.append(i_temp)
            runtime.append(int(ru_temp))
            certify.append(c_temp)
            review.append(re_temp)
    df=pd.DataFrame({'Id':ids,'Movie Title':movies,'Genre':genre,'Rating':rating,'Runtime(in min)':runtime,'Certificate':certify,'Reviews':review})
    return df


# <b> Now, Lemme call myfunction on year 2021 With count As 20</b>

# In[16]:


k=myfunction(2021,20)
k


# <b> Kudos, We got the data cleaned and arranged i nform of dataframe successfuly through the website <br> Now lets have some visualizations on movie ratings , genre , etc.,</b>

# In[17]:


sns.set(rc={"font.style":"normal",
            "axes.facecolor":'white',
            "figure.facecolor":'white',
            "text.color":"black",
            "xtick.color":"black",
            "ytick.color":"black",
            "axes.labelcolor":"black",
            "axes.grid":False,
            'axes.labelsize':30,
            'figure.figsize':(20.0, 10.0),
            'xtick.labelsize':25,
            'font.size':20,
            'ytick.labelsize':20})


# In[18]:


sns.barplot(y='Movie Title',x='Rating',data=k,saturation=1)


# <p>It shows that Zack Snyders Justice League has the highest rating. Well, We all know why,Its a better version of the same movie From 2017 which was directed first by Zack Snyder and then later by another directer which led to a disaster In 2017.</p>

# <b>Okay, now lets add score attribute to the dataframe by taking rating and revies into the account</b>

# In[19]:


df=myfunction(2021,250)
d=pd.DataFrame(columns=['Name','Genre','Rating','Score'])
for i in range(df.shape[0]):
    for j in df.iloc[i]['Genre']:
        d=d.append({'Name':df.iloc[i]['Movie Title'],'Genre':j,'Rating':df.iloc[i]['Rating'],'Score':df.iloc[i]['Rating']/df.iloc[i]['Reviews']},ignore_index=True)
d


# In[22]:


temp=d.groupby('Genre').count()
temp['Score']


# In[259]:


temp.columns=['Count','Score']


# <b>Let's visualize no of movies in all Genres for the year.</b>

# In[261]:


temp.plot(kind='bar',y='Count')


# <b>Let's visualize rating of all Genres for the given year.</b>

# In[262]:


temp=d.groupby('Genre')['Rating'].mean()
plt.rcParams['figure.figsize']=(10,5)
temp.plot(kind='bar',y='Rating')


# <b> Now will try to get hte top rated genre based on the score for the given year </b>

# In[275]:


temp=d.groupby('Genre')['Score'].max()
temp=pd.DataFrame(temp)
temp.reset_index(inplace=True)
temp=temp.sort_values(by='Score',ascending=False)
temp.iloc[0].Genre


# <p> Lets go bit further and create an fuction that return the scored genre when the year is passed as parmetre </p>

# In[278]:


def getgenre(year):
    df=myfunction(year,250)
    d=pd.DataFrame(columns=['Name','Genre','Rating','Score'])
    for i in range(df.shape[0]):
        for j in df.iloc[i]['Genre']:
            d=d.append({'Name':df.iloc[i]['Movie Title'],'Genre':j,'Rating':df.iloc[i]['Rating'],'Score':df.iloc[i]['Rating']/df.iloc[i]['Reviews']},ignore_index=True)
    temp=d.groupby('Genre')['Score'].max()
    temp=pd.DataFrame(temp)
    temp.reset_index(inplace=True)
    temp=temp.sort_values(by='Score',ascending=False)
    return temp.iloc[0].Genre
for i in range(1970,2022):
    print(i,getgenre(i))


# <b> Now , Lets create an other dataframe that will store top scored genre as per the specified year </b>

# In[281]:


import time
gen_dict=dict()
for i in range(1970,2022):
    gen_dict[i]=getgenre(i)
    time.sleep(3)


# In[287]:


gdf=pd.DataFrame.from_dict(gen_dict, orient='index')


# In[299]:


gdf.columns=['Famous Genre']


# In[292]:


gdf.tail(10)


# <h2>Great! We have made this far using the first method for Web Scraping .Now Let's do this using API.</h2>

# <p> API stands for Application Programming Interface. An API is a software intermediary that allows applications to interact with each other. In other words, an API is the messenger that delivers your request to the provider that you're requesting it from and then delivers the response back to you.</p>

# In[3]:


url1='http://www.imdb.com/title/{a}'.format(a='tt0993840')
res=requests.get(url1)


# In[10]:


data=BeautifulSoup(res.text,'html')
f=str(data.find("script",attrs={'type':"application/ld+json"}))
f=f[f.index('{'):-9]
f=json.loads(f)
f


# <p>Let's write a piece of code that generates a dataframe with the details of all the movies.<br>
# Remember,We have got the ids of movies from the first method .We can use them or we can get the 'ids' by searching on google.
# However,It's good to get the ids from the first method</p>

# In[16]:


idds=['tt0993840','tt3228774','tt11083552']
import time
df=pd.DataFrame(columns=['Name','ContentType','Genre','Rating','No of Reviews','SCore'])
for i in idds:
    url1='http://www.imdb.com/title/{a}'.format(a=i)
    time.sleep(5)
    res=requests.get(url1)
    data=BeautifulSoup(res.text,'html')
    f=str(data.find("script",attrs={'type':"application/ld+json"}))
    f=f[f.index('{'):-9]
    f=json.loads(f)
    df=df.append(({'Name':f['name'],'ContentType':f['contentRating'],'Genre':f['genre'],'Director':f['director'][0]['name'],'Rating':f['aggregateRating']['ratingValue'],'No of reviews':f['aggregateRating']['ratingCount'],'Score':f['aggregateRating']['ratingValue']/f['aggregateRating']['ratingCount']}),ignore_index=True)
df


# <b>Since 2013, Drama has never been recorded has top genre.I think thats because of change in Cultural practices and Technology.<br>
# But let's not jump into the conclusions about the reasons before having the data.</b>

# <b>Okay,that's how We made to end of the project and can perform Web Scraping using python libraries and get to play with the data.</b>
