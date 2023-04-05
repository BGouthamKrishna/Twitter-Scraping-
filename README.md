# Twitter Scraping

Data is scattered everywhere in the world. We can find all sorts of data in various soccial media websites like Facebook and Twitter. Inorder to get tweets from twitter pertaining to a keyword or hastag, we need to scrape data from twitter. 

Using a library such as snscrape we can obtain  data like (date, id, url, tweet content, user,reply count, retweet count,language, source, like count etc) from twitter.

Streamlit helps us create web app for the project. Streamlit is an open source app framework in Python language. It creates a GUI that allows us to enter the keyword, daterange and number of tweets to be scraped. Scraped data can be downloaded as Csv or Json files and also be uploaded to the mongodb server directly using the buttons on the interface.




## Requirements

Python3

Pymongo

MongoDB Atlas

Streamlit

Snscrape



## Installation

Install Snscrape, Streamlit and Mongodb

```bash
  pip install snscrape
  pip install streamlit
  pip install pymongo
```

   
## Workflow

### Create a  list to append tweet data to
```bash
  tweets_list = []
```

### Gathering inputs such as keyword to be searched, Date range & Tweet limit from user using streamlit interface
```bash
Keyword = st.text_input('Keyword or Hashtag')
date = st.date_input("Enter start date")
date2 = st.date_input("Enter end date")
number = st.number_input('Enter number of tweets', step=1)
```

###  Using TwitterSearchScraper to scrape data and append tweets to list
```bash
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(Keyword + ' since:' + str(date) + ' until:' + str(date2)).get_items()):
            if i > number:
                break
            tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.replyCount, tweet.retweetCount, tweet.lang,
             tweet.source, tweet.likeCount])
```

### Create a dataframe from the tweets list above and display using streamlit
```bash
tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username', 'reply counnt', 'retweet count',
                                      'language', 'source', 'like count'])
st.dataframe(tweets_df)
```

### Define a function to convert the dataframe to csv and json formats
```bash
        def con_csv(tweets_df):
            return tweets_df.to_csv()

        def con_json(tweets_df):
            return tweets_df.to_json()
```

### Using MongoDB Atlas as a new database to store date(scraped tweets) in collections(scraped_tweets)
```bash
client = pymongo.MongoClient("mongodb+srv://gouthamkrishna:Ihirmjbp@twitterscraping.0gezcyr.mongodb.net/?retryWrites=true&w=majority")
db = client.Twitter_data
col = db.Twitter_collection
scr_data = {"Scraped_word": Keyword,
            "Scraped_date": str(datetime.date.today()),
            "Scraped_tweets": tweets_df.to_dict('records')}
```

### Create GUI buttons using streamlit in order to upload or download the files
```bash
st.download_button(
        label="Download data as CSV",
        data=con_csv(tweets_df),
        file_name='tweets.csv',
        mime='text/csv', )

st.download_button(
        label="Download data as Json",
        data=con_json(tweets_df),
        file_name='tweets.json',
        mime='text/csv',)

st.button("Upload to MongoDB"):
        col.delete_many({})
        col.insert_one(scr_data)
        st.success('Upload to MongoDB Successfully:thumbsup:')
```
## Create a MongoDB server using MondoDB Atlas

### Create an account and login to MongoDB Atlas. Click on "Create" to create a new shared cluster. 

![App Screenshot](https://snipboard.io/hn1CRe.jpg)

### New Cluster has been created. Click on "Connect" to connect to the cluster.

![App Screenshot](https://snipboard.io/RhAGPT.jpg)

### Click on "Connect your application"

![App Screenshot](https://snipboard.io/BS5nbE.jpg)

### Connection string has been generated. Same can be used in the code inorder to connect to the MongoDB server.

![App Screenshot](https://snipboard.io/OFRZ3w.jpg)

### Uploaded Data can be found under "collections" section. 

![App Screenshot](https://snipboard.io/QTx4V9.jpg)






## Authors

- [@BGouthamkrishna](https://github.com/BGouthamKrishna)


## 🔗 Links

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/bgouthamkrishna/)
