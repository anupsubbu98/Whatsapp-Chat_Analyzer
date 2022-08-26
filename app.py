import streamlit as st
from matplotlib import pyplot as plt
import preprocessor
import function
import plotly.express as px

st.sidebar.title('Whatsapp Chat Analyzer')
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    #st.dataframe(df)

    user_list = df['User'].unique().tolist()
    user_list.remove('Group Notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox('Show Analysis wrt', user_list)

    if st.sidebar.button("Show Analysis"):
        no_of_messages, no_of_words, no_of_media_messages, no_of_links = function.fetch_stats(selected_user, df)
        user_msg_df,flag = function.user_msg_df(selected_user, df)
        if flag == 0:
           st.dataframe(user_msg_df)

        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(no_of_messages)

        with col2:
            st.header('Total Words')
            st.title(no_of_words)

        with col3:
            st.header('Media shared')
            st.title(no_of_media_messages)

        with col4:
            st.header('Links shared')
            st.title(no_of_links)
            
        monthly_timeline_df = function.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(monthly_timeline_df['Time'],monthly_timeline_df['Message'],color='green')
        plt.xticks(rotation='vertical')
        plt.grid()
        st.title('Monthly timeline')
        st.pyplot(fig)
        
        daily_timeline_df = function.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline_df['Date_val'],daily_timeline_df['Message'],color='black')
        plt.xticks(rotation='vertical')
        st.title('Daily timeline')
        st.pyplot(fig)
       
        st.title('Activity Map')
        most_busy_day_df   = function.most_busy_day(selected_user,df)
        fig1, ax1 = plt.subplots()
        col1, col2 = st.columns(2)

        with col1:
             st.header('Most busy day')
             ax1.bar(most_busy_day_df['Day_name'],most_busy_day_df['Message'])
             plt.xticks(rotation='vertical')
             st.pyplot(fig1)
            
        most_busy_month_df = function.most_busy_month(selected_user,df)
        fig2, ax2 = plt.subplots()

        with col2:
             st.header('Most busy month')
             ax2.bar(most_busy_month_df['Time'],most_busy_month_df['Message'],color='orange')
             plt.xticks(rotation='vertical')
             st.pyplot(fig2)

        
        if selected_user == 'Overall':
            freq_users, freq_users_df = function.busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            
            with col1:
                st.header('Most frequent users')
                ax.bar(freq_users.index, freq_users.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
	  	
            with col2:
                st.header('Most busy users (%)')
                st.dataframe(freq_users_df)
                
        col1, col2 = st.columns(2)

        freq_used_words_df = function.freq_used_words(selected_user, df)
        with col1:
            st.header('Frequently used words')
            st.dataframe(freq_used_words_df)

        emoji_df = function.freq_used_emojis(selected_user,df)
        with col2:
            st.header('Frequently used emojis')
            st.dataframe(emoji_df)
            
                
        st.title('Word Cloud')
        wc_df = function.wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(wc_df)
        plt.axis("off")
        st.pyplot(fig)
        
        fig, ax = plt.subplots()
        ax.barh(freq_used_words_df[0], freq_used_words_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most Common words')
        st.pyplot(fig)
