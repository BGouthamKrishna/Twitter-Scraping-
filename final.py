import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import datetime
import pymongo

# program to not display a warning message
import warnings

# displaying the warning message
warnings.warn('Warning Message: 4')

# Page config settings
st.set_page_config(layout="wide", page_title='Twitter scraper')

st.subheader("**:blue[:man-raising-hand: Welcome to Twitter Scraping]**")

# Project introduction
st.write(""" 
This website helps you to Scrape Tweets using a **keyword or hashtag**. You can also specify the date range 
and total number of tweets needed. Dataframes containing the tweets can be downloaded in either CSV or Json formats.
Dataframes can also be uploaded to the Mongodb server directly.""")

# Creating list to append tweet data to
tweets_list = []

# Gathering inputs such as keyword to be searched, Date range & Tweet limit
Keyword = st.text_input('Keyword or Hashtag')
date = st.date_input("Enter start date")
date2 = st.date_input("Enter end date")
number = st.number_input('Enter number of tweets', step=1)

if Keyword == '':
    st.write(" Please enter the keyword ")
else:
    run = st.button('Run')      # This enables Run button to extract data and Display it

    if "load_state" not in st.session_state:
        st.session_state.load_state = False
    if run or st.session_state.load_state:
        st.session_state.load_state = True

        # Using TwitterSearchScraper to scrape data and append tweets to list
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(Keyword + ' since:' + str(date) +
                                                                 ' until:' + str(date2)).get_items()):
            if i > number:
                break
            tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.replyCount,
                                tweet.retweetCount, tweet.lang, tweet.source, tweet.likeCount])

        # Creating a dataframe from the tweets list above
        tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username', 'reply count',
                                                       'retweet count', 'language', 'source', 'like count'])

        # Displaying the above data dataframe
        st.dataframe(tweets_df)

        # Convert the dataframe into csv file
        def con_csv(tweets_df):
            return tweets_df.to_csv()

        # Convert the dataframe into json file
        def con_json(tweets_df):
            return tweets_df.to_json()

        # Button to download the dataframe into csv file
        st.download_button(
            label="Download data as CSV",
            data=con_csv(tweets_df),
            file_name='tweets.csv',
            mime='text/csv', )

        # Button to download the dataframe into json file
        st.download_button(
            label="Download data as Json",
            data=con_json(tweets_df),
            file_name='tweets.json',
            mime='text/csv',)

        # Using MongoDB Atlas as a new database to store date(scraped tweets) in collections(scraped_tweets)
        client = pymongo.MongoClient("mongodb+srv://gouthamkrishna:Ihirmjbp@twitterscraping.0gezcyr.mongodb.net/?retryWrites=true&w=majority")
        db = client.Twitter_data
        col = db.Twitter_collection
        scr_data = {"Scraped_word": Keyword, "Scraped_date": str(datetime.date.today()),
                    "Scraped_tweets": tweets_df.to_dict('records')}

        # Button to Upload the data into MongoDB file
        if st.button("Upload to MongoDB"):
            col.delete_many({})
            col.insert_one(scr_data)
            st.success('Upload to MongoDB Successfully:thumbsup:')
