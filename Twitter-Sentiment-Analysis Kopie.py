#library for accessing tweeters api
import tweepy
#sentiment analysis library
from textblob import TextBlob
import csv
from urlextract import URLExtract


# Step 1 - Authenticate
# consumer at twitter
consumer_key= 'CONSUMER_KEY'
consumer_secret= 'CONSUMER_SECRET'

# gives us access to twitters api
access_token='ACCESS_TOKEN'
access_token_secret='ACCESS_TOKEN_SECRET'
# this is for authentication by using OAuthHandler and set_access_token method
# from tweepy with a bunch of codes hidden to us
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


# main variables where we'll do all the twitter magic
# storing twitter api class in var 'api' for easy usage
api = tweepy.API(auth)

# now, we want to search for tweets

# create a public var to store a list of tweets
# .search method will retrieve a bunch of tweets with the designated word (Trump)
public_tweets = api.search('Trump')

# to export to .csv
# 'with open' helps close your file automatically
with open('twitter_sentiment_analysis.csv', 'w', newline = '') as output:
    
    # create var
    fileOut = csv.writer(output)
    data = ['Tweets', 'Polarity', 'Subjectivity', 'URL']
    
    fileOut.writerow(data)
    
    for tweet in public_tweets:
        analysis = TextBlob(tweet.text)
        polarityInt = analysis.sentiment.polarity
        subjectivityInt = analysis.sentiment.subjectivity
        
        # [-1.0, 1.0]
        if polarityInt >= 0.0:
            polarityStr = "Positiv"
        else: polarityStr = "Negativ"
        
        # [0.0, 1.0]
        if subjectivityInt >= 0.5:
            subjectivityStr = "Subjective"
        else: subjectivityStr = "Objective"
        
        # default value for url
        # if url = None, perform operations on tweet.text to cut off existing url
        url = None
        
        # to start a separate column for URL
        # split texts into chunks
        words = tweet.text.split()
        
        # to extract link...
        link = URLExtract()
        
        # find links within a tweet
        urls = link.find_urls(tweet.text)
        
        # identify link - http / https (http is common denominator for both)
        for word in words:
            if 'http' in word:
                url = word
    
        fileOut.writerow([tweet.text, polarityStr, subjectivityStr, url])
        
        # print to terminal
        print (tweet.text)
        print ('Polarity: ', polarityInt)
        print ('Subjectivity:', subjectivityInt)


