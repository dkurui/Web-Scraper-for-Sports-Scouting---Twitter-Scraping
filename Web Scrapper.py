#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tweepy 
import pandas as pd
import datetime
import pytz
import re
import requests
import sys
from pytz import timezone
import time


# In[2]:


handles = pd.read_excel('twitter_handles.xlsx')
handles_list = list(handles['Twitter Handles'])


# In[3]:


# In[4]:


# consumer_key = "xxxxxxxxxxxxxxxxxxx"
# consumer_secret = "xxxxxxxxxxxxxxxxxxx"
# access_token = "xxxxxxxxxxxxxxxxxxx"
# access_token_secret = "xxxxxxxxxxxxxxxxxxx"


# In[5]:


#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
API = tweepy.API(auth,wait_on_rate_limit=True,retry_count = 5, retry_delay = 5)


# In[6]:


def authenticate_tokens(api):
    counter = 1
    while True:
        try:
            print("\nAuthenticating your API......")
            API.verify_credentials()
            print('\nSuccessfully Authenticated')
            return True
        except:
            print('\nAuthentication Failed.......retrying to check again')
            if counter <3:
                counter = counter+1
                for x in range(10):   
                    print(('\rRetrying in {} sec').format(-(x-10)), end = '')
                    time.sleep(1)
                continue
            else:
                print('\nAuthentication Has Failed, check your authentication tokens and try again')
                return False
                break
        else:
            return False


# In[7]:


def check_internet_connection():
    url = "http://www.google.com"
    timeout = 5
    counter = 1    
    while True:
        try:
            request = requests.get(url, timeout=timeout)
            if (request.status_code == 200):
                return True
        except:
            print("\nSeems there is no internet connection..........retrying")
            continue
        else:  
            print('\nThere is no internet connection, check and try again')
            return False


# In[8]:


def check_if_user_exist(screen_name, api):
    "'This function checks if a twiter screen name given exists on twitter'"   
    
    counter = 1
    while True:
        try:
            user = (api.get_user(screen_name = screen_name)).name 
            return True
        except:
            print('seems',screen_name,'is not on twitter, the system is retrying again to find the user...')
            if counter <5:
                counter = counter+1
                continue                
            else:
                return False
                break
        else:
            return False


# In[9]:


def retrieve_university(tweet_text):
    "This fucntion retrieves the name of the university from a given tweet"
    clean_tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet_text)    
    target = "university"
    words = clean_tweet.split()
    for i,w in enumerate(words):
        try:
            if (target in w):
                if words[i+1] == 'of':
                    uni = words[i]+' '+words[i+1]+' '+words[i+2]+' '+words[i+3]
                    return uni
                else:
                    uni = words[i-2]+' '+words[i-1]+' '+words[i-0]
                    return uni
        except:
            return None
            
def retrieve_college(tweet_text):
    "This fucntion retrieves the name of the college from a given tweet"
    clean_tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet_text)    
    target = "college"
    words = clean_tweet.split()
    for i,w in enumerate(words):
        try:
            if (target in w) :
                if words[i+1] == 'of':
                    uni = words[i]+' '+words[i+1]+' '+words[i+2]
                    return uni
                else:
                    uni = words[i-1]+' '+words[i]
                    return uni
        except:
            return None
            
def retrieve_academy(tweet_text):
    "This fucntion retrieves the name of the academy from a given tweet"
    clean_tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet_text)    
    target = "academy"
    words = clean_tweet.split()
    for i,w in enumerate(words):
        try:
            if(target in w):
                if words[i+1] == 'of':
                    uni = words[i]+' '+words[i+1]+' '+words[i+2]
                    return uni
                else:
                    uni = words[i-2]+' '+words[i-1]+' '+words[i-0]
                    return uni
        except:
            return None
            
def retrieve_others(tweet_text,api):
    "This function retrieves the institutions which are not specificaly a university or academy"
    clean_tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet_text) 
    target = "offer"
    words = clean_tweet.split()
    for i in range(len(words)):
        try:
            if (words[i] == 'offer' and words[i+1] == 'from' and '@' in words[i+2]) : 
                if '@' in words[i+2]:           
                    uni = words[i+2]
                    print(uni)
                    if uni.count('@')>1:                        
                        k= uni.split('@')
                        uni = k[1]
                        uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                        print(uni)
                        uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+2]+')'
                    uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                    uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+2]+')'
                else:
                    uni_name = words[i+2]+' '+words[i+3]+' '+words[i+4]
                break
            elif (words[i] == 'offer' and words[i+1] == 'from') : 
                if '@' in words[i+2]:           
                    uni = words[i+2]
                    if uni.count('@')>1:                        
                        k= uni.split('@')
                        uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                        uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+2]+')'
                    uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                    uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+2]+')'
                else:
                    uni_name = words[i+2]+' '+words[i+3]
                break
            elif (words[i] == 'from' and '@' in words[i+1]) : 
                if '@' in words[i+1]:           
                    uni = words[i+1]
                    if uni.count('@')>1:                        
                        k= uni.split('@')
                        uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                        uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+1]+')'
                    uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                    uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+1]+')'
                else:
                    uni_name = words[i+2]+' '+words[i+3]+' '+words[i+4]
                break
            elif (words[i] == 'offer' and words[i+1] == 'to' and words[i+2] == 'play' and words[i+3] == 'at') : 
                if '@' in words[i+4]:           
                    uni = words[i+4]
                    if uni.count('@')>1:                        
                        k= uni.split('@')
                        uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                        uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+4]+')'
                    uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                    uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+4]+')'
                else:
                    uni_name = words[i+4]+' '+words[i+5]+' '+ words[i+6]+' '+words[i+7]+' '+words[i+8]
                break
            elif (words[i] == 'play' and words[i+1] == 'football' and words[i+2] == 'at' ) : 
                if '@' in words[i+3]:           
                    uni = words[i+3]
                    if uni.count('@')>1:                        
                        k= uni.split('@')
                        uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                        uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+3]+')'
                    uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                    uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+3]+')'
                else:
                    uni_name = words[i+3]+' '+words[i+4]
                break
            elif (words[i] == 'play' and words[i+1] == 'football') : 
                if '@' in words[i+2]:           
                    uni = words[i+2]
                    if uni.count('@')>1:                        
                        k= uni.split('@')
                        uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                        uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+2]+')'
                    uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                    uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+2]+')'
                else:
                    uni_name = words[i+2]+' '+words[i+3]
                break
            elif (words[i] == 'scholarship' and words[i+1] == 'from') : 
                if '@' in words[i+2]:           
                    uni = words[i+2]
                    if uni.count('@')>1:                        
                        k= uni.split('@')
                        uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                        uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+2]+')'
                    uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                    uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+2]+')'
                else:
                    uni_name = words[i+2]+ ' '+words[i+3]
                break
            elif (words[i] == 'scholarship' and words[i+1] == 'to') : 
                if '@' in words[i+2]:           
                    uni = words[i+2]
                    if uni.count('@')>1:                        
                        k= uni.split('@')
                        uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                        uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+2]+')'
                    uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                    uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+2]+')'
                else:
                    uni_name = words[i+2]+ ' '+words[i+3]
                break
            elif (words[i] == 'offer' and words[i+1] == 'to') : 
                if '@' in words[i+2]:           
                    uni = words[i+2]
                    if uni.count('@')>1:                        
                        k= uni.split('@')
                        uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                        uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+2]+')'
                    uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                    uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+2]+')'
                else:
                    uni_name = words[i+2]+' '+words[i+3]
                break
            elif (words[i] == 'offered' and words[i+1] == 'to' and words[i+2] == 'play' and words[i+3] == 'at') : 
                if '@' in words[i+4]:           
                    uni = words[i+4]
                    if uni.count('@')>1:                        
                        k= uni.split('@')
                        uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                        uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+4]+')'
                    uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                    uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+4]+')'
                else:
                    uni_name = words[i+4]+' '+words[i+5]
                break
            elif (words[i] == 'my' and words[i+1] == 'offer' and words[i+2] == 'to' and words[i+3] == 'play' and words[i+4] == 'football') : 
                if '@' in words[i+5]:           
                    uni = words[i+5]
                    if uni.count('@')>1:                        
                        k= uni.split('@')
                        uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                        uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+5]+')'
                    uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                    uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+5]+')'
                else:
                    uni_name = words[i+5]+' '+words[i+6]
                break
            elif (words[i] == 'my' and words[i+1] == 'offer' and words[i+2] == 'to' and words[i+3] == 'play' and words[i+4] == 'football') : 
                if '@' in words[i+5]:           
                    uni = words[i+5]
                    if uni.count('@')>1:                        
                        k= uni.split('@')
                        uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                        uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+5]+')'
                    uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                    uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+5]+')'
                else:
                    uni_name = words[i+5]+' '+words[i+6]
                break
            elif (words[i] == 'offered' and words[i+1] == 'to' and words[i+2] == 'play' and words[i+3] == 'football' and words[i+4] == 'at') : 
                if '@' in words[i+5]:           
                    uni = words[i+5]
                    if uni.count('@')>1:                        
                        k= uni.split('@')
                        uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                        uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+5]+')'
                    uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                    uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+5]+')'
                else:
                    uni_name = words[i+5]+' '+words[i+6]
                break
            elif (words[i] == 'offer' and words[i+1] == 'at') : 
                if '@' in words[i+2]:           
                    uni = words[i+2]
                    if uni.count('@')>1:                        
                        k= uni.split('@')
                        uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                        uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+2]+')'
                    uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                    uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+2]+')'
                else:
                    uni_name = words[i+2]+' '+words[i+3]
                break
            elif (words[i] == 'offer!') : 
                if '@' in words[i+1]:           
                    uni = words[i+1]
                    if uni.count('@')>1:                        
                        k= uni.split('@')
                        uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                        uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+1]+')'
                    uni = re.sub(r'[^_a-zA-Z0-9]','', uni)
                    uni_name = str((API.get_user(screen_name = uni)).name)+' ('+words[i+1]+')'
                else:
                    uni_name = words[i+1]+' '+words[i+2]+' '+words[i+3]
                break
            else:
                uni_name = 'None'
        except:
            uni_name = 'None'
    return uni_name
        


# In[10]:


def date_setter(start_date,stop_date):
    "This function seeks to convert the dates entered from string to type datetime"
    split_start_date = start_date.split("-")
    start_Y = int(split_start_date[0])
    start_M = int(split_start_date[1])
    start_D = int(split_start_date[2])
    
    split_stop_date = stop_date.split("-")
    stop_Y = int(split_stop_date[0])
    stop_M = int(split_stop_date[1])
    stop_D = int(split_stop_date[2])
    
    start = datetime.datetime(start_Y, start_M, start_D)
    stop = datetime.datetime(stop_Y, stop_M, stop_D)
    
    utc=pytz.UTC
    begin = utc.localize(start)
    end = utc.localize(stop)
    
    return begin, end


# In[11]:


start_date = input("Enter the start date: Use the format YYYY-MM-DD ")
stop_date = input("Enter the start date: Use the format YYYY-MM-DD ")

from_date, to_date = date_setter(start_date,stop_date)


# In[12]:


tweets_df = pd.DataFrame(columns = ['TWITTER HANDLE', 'PLAYER NAME','DATE OF TWEET', 'TWEET'])


# In[13]:


def retrive_tweets(screen_name, api,df):
    "This function retrieves tweets for a given user and save them in a txt file"
    while True:
        try:
            if check_internet_connection():        
                if check_if_user_exist(screen_name, api):
                    while True:
                        try:
                            counter = 0
                            tweeter_user = (api.get_user(screen_name = screen_name)).name
                            for status in tweepy.Cursor(api.user_timeline,screen_name =screen_name ,tweet_mode="extended", include_rts = False, count = 3200).items():
                                lower_case_tweet = (status.full_text).lower() 
                                if (('offer from' in lower_case_tweet) or ('offer to' in lower_case_tweet) or  ('offers' in lower_case_tweet) 
                                or ('offer' in lower_case_tweet) or ('offered' in lower_case_tweet) or ('scholarship' in lower_case_tweet)
                                or (('college' in lower_case_tweet) and ('offer' in lower_case_tweet) )or (('academy' in lower_case_tweet) and ('offer' in lower_case_tweet) )
                                or (('tech' in lower_case_tweet) and ('offer' in lower_case_tweet) )or ('scholarships' in lower_case_tweet)):
                                    record_to_append = [screen_name,tweeter_user,status.created_at,status.full_text]
                                    df_length = len(df)
                                    df.loc[df_length] = record_to_append 
                                    counter = counter+1
                            print(f"\n{counter} tweets retrieved for the selected period")
                            print("Retrieved and saved successfully\n")
                            break
                        except Exception as e:
                            print(e)
                            print('Due to twitter retrieval rate limits, please be patient as the system retries....')
                            for x in range(60):   
                                print(('\rRetrying in {} sec').format(-(x-60)), end = '')
                                time.sleep(1)
                            continue
                else:
                    print('The user',screen_name,'does not exist, please check the name again')
            break
        except:
            print('Seems there is no internet connection, retrying........\n')  
            for x in range(5):   
                print(('\rRetrying in {} sec').format(-(x-5)), end = '')
                time.sleep(1)
            continue
            
    


# In[14]:


count = 1 
if (check_internet_connection()):
    if(authenticate_tokens(API)):
        for item in handles_list: 
            print(count,' out of ',len(handles_list),'handles')
            print("Retrieving tweets from ",item)
            retrive_tweets(item, API,tweets_df)
            count +=1


# In[ ]:





# In[ ]:





# In[16]:


tweets_df['DATE OF TWEET'] = tweets_df['DATE OF TWEET'].dt.tz_localize(None)
writer = pd.ExcelWriter('Raw_Tweets.xlsx')
tweets_df.to_excel(writer,'Raw_tweets')
writer.save()
print('All retrived tweets have been written successfully to Excel Sheet.')


# In[17]:


raw_tweets_df = pd.read_excel('Raw_Tweets.xlsx')
final_tweets_df = pd.DataFrame(columns = ['TWITTER HANDLE', 'INSTITUTION','DATE OF TWEET', 'TWEET'])
offers_df = pd.DataFrame(columns = ['TWITTER HANDLE', 'NUMBER OF OFFERS','PERIOD'])


# In[18]:


def retrieve_institution_from_tweets(handle, api, fin_df,off_df, raw_tweets_df):
    "This function runs to retriev the institutions names fom the retirved tweets"
    while True:
        try:
            print('Retrieveing institutions for',handle)
            handles_present = list(set(raw_tweets_df['TWITTER HANDLE']))
            num_offers = 0
            if handle in handles_present: 
                tweeter_user = (API.get_user(screen_name = handle)).name  
                sub_df = raw_tweets_df.loc[(raw_tweets_df['TWITTER HANDLE'] == handle)]
                for i in range(len(sub_df)):
                    tot = (' '+str(len(sub_df)))
                    print(('\rProcessing {} of').format(i+1)+tot, end=' tweets')
                    if((pytz.utc.localize(sub_df['DATE OF TWEET'].iloc[i])>=(from_date)) and (pytz.utc.localize(sub_df['DATE OF TWEET'].iloc[i])<=(to_date)) ):
                        lower_case_tweet = (sub_df['TWEET'].iloc[i]).lower() 
                        if ('university' in lower_case_tweet):
                            institute = retrieve_university(lower_case_tweet)
                        elif('academy' in lower_case_tweet ):
                            institute = retrieve_academy(lower_case_tweet)
                        elif('college' in lower_case_tweet ):
                            institute = retrieve_college(lower_case_tweet)
                        else:
                            institute = retrieve_others(lower_case_tweet,API)
                        record_to_save = [handle,institute,str(sub_df['DATE OF TWEET'].iloc[i]),str(sub_df['TWEET'].iloc[i])]
                        df_len = len(fin_df)
                        fin_df.loc[df_len] = record_to_save 
                        if(institute!='None'):
                            num_offers +=1
                    
            period = 'between '+str(from_date.date())+' and '+str(to_date.date())  
            offers_to_append = [handle,num_offers,period]
            off_df_len = len(off_df)            
            off_df.loc[off_df_len] = offers_to_append
            print(handle, 'received',num_offers, 'offer(s) within the selected period')  
            print("------------------------------------------------------------------------------------")
            return fin_df, off_df        
        except Exception as e:
            print(e)
            print('Please be patient as the system retries.......')
            for x in range(60):   
                print(('\rRetrying in {} sec').format(-(x-60)), end = '')
                time.sleep(1)
            continue


# In[19]:


counter = 1
for h in handles_list:
    print(counter,'out of',len(handles_list))
    retrieve_institution_from_tweets(h, API, final_tweets_df,offers_df, raw_tweets_df)
    counter = counter + 1


# In[21]:


doc_name = str(from_date.date()) +' to '+str(to_date.date())
writer = pd.ExcelWriter(doc_name+'.xlsx')
# write dataframe to excel sheet named 'marks'
final_tweets_df.to_excel(writer,str(from_date.date()) +' to '+str(to_date.date()))
offers_df.to_excel(writer, 'OFFERS '+str(from_date.date()) +' to '+str(to_date.date()))
# save the excel file
writer.save()
print('Data written successfully to Excel Sheet.')


# In[ ]:




