from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
import regex

def user_msg_df(selected_user,df):
 
    if selected_user != 'Overall':
        user_msg_df = df[df['User'] == selected_user]
        user_msg_df = user_msg_df.drop(columns={'Month_num','Date_val','Date'})
        flag = 0

    else:
        user_msg_df = df[df['User'] == 'Overall'].drop(columns={'Month_num','Date_val','Date'})
        flag = 1
        
    return user_msg_df,flag
    
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    no_of_messages = df.shape[0]

    words = []
    for message in df['Message']:
        words.extend(message.split())

    no_of_media_messages = df[df['Message'] == '<Media omitted>\n'].shape[0]

    extractor = URLExtract()

    links = []
    for message in df['Message']:
        links.extend(extractor.find_urls(message))

    return no_of_messages, len(words), no_of_media_messages, len(links)
    
def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
        
    monthly_timeline_df = pd.DataFrame(df.groupby(['Year','Month_num','Month']).count()['Message']).reset_index()
    time = []
    for i in range(monthly_timeline_df.shape[0]):
        time.append(monthly_timeline_df['Month'][i]+'-'+str(monthly_timeline_df['Year'][i]))

    monthly_timeline_df['Time'] = time
    
    return monthly_timeline_df
    
 
def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
        
    daily_timeline_df = pd.DataFrame(df.groupby('Date_val').count()['Message']).reset_index()
       
    return daily_timeline_df
    
def most_busy_day(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
        
    most_busy_day_df = pd.DataFrame(df.groupby('Day_name').count()['Message']).reset_index()
    most_busy_day_df.sort_values(by=['Message'],ascending=False,inplace=True)
       
    return most_busy_day_df
    
def most_busy_month(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
        
    most_busy_month_df = pd.DataFrame(df.groupby(['Month','Year']).count()['Message']).reset_index().head(15)
    time = []	
    for i in range(most_busy_month_df.shape[0]):
        time.append(most_busy_month_df['Month'][i]+'-'+str(most_busy_month_df['Year'][i]))

    most_busy_month_df['Time'] = time 
    most_busy_month_df.sort_values(by=['Message'],ascending=False,inplace=True)
       
    return most_busy_month_df


def busy_users(df):
    freq_users = df['User'].value_counts().head(10)
    freq_users_df = round(df['User'].value_counts() / df.shape[0] * 100,2).reset_index().rename(
        columns={'index': 'Frequent User', 'User': 'Percent'})
    return freq_users, freq_users_df
    
def freq_used_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df[df['User'] != 'Group Notification']
    temp = temp[temp['Message'] != '<Media omitted>\n']

    words = []
    for message in temp['Message']:
        words.extend(message.split())

    freq_used_words_df = pd.DataFrame(Counter(words).most_common(20))
    return freq_used_words_df


def freq_used_emojis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    total_emojis_list = list([a for b in df.emoji for a in b])
    emoji_dict = dict(Counter(total_emojis_list))
    emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
    emoji_df = pd.DataFrame(emoji_dict, columns=['emoji', 'count'])

    return emoji_df


def wordcloud(selected_user, df):
    temp = df[df['User'] != 'Group Notification']
    temp = temp[temp['Message'] != '<Media omitted>\n']

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    wc = WordCloud(width=400, height=400, min_font_size=6, background_color='black')
    wc_df = wc.generate(temp['Message'].str.cat(sep=" "))
    return wc_df

def emoji_freq(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    total_emojis_list = list([a for b in df.emoji for a in b])
    emoji_dict = dict(Counter(total_emojis_list))
    emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
    emoji_df = pd.DataFrame(emoji_dict, columns=['emoji', 'count'])

    return emoji_df







