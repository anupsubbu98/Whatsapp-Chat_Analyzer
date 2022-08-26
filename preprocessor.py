import regex as re
import pandas as pd
import emoji


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'Message': messages, 'Date': dates})
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y, %H:%M - ')

    users = []
    messages = []
    for message in df['Message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group Notification')
            messages.append(entry[0])

    df['User'] = users
    df['Message'] = messages

    df['Day'] = df['Date'].dt.day
    df['Month'] = df['Date'].dt.month_name()
    df['Year'] = df['Date'].dt.year
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute
    df["emoji"] = df["Message"].apply(split_count)
    
    df['Date_val'] = df['Date'].dt.date
    df['Month_num'] = df['Date'].dt.month
    df['Day_name'] = df['Date'].dt.day_name()
    
  
    return df


def split_count(text):
    emoji_list = []
    data = re.findall(r'\X', text)
    for word in data:
        if any(char in emoji.EMOJI_DATA for char in word):
            emoji_list.append(word)
    return emoji_list

