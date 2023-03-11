import os
import streamlit as st
import tweepy
import joblib
import re

# Load the model
model_path = os.path.join(os.path.dirname(__file__), 'model_1.pkl')
model = joblib.load(model_path)

# Authenticate with Twitter API
consumer_key = 'u9D8IF1iOVWaoRy24598GyRq9'
consumer_secret = 'WYOe2e2Nkb2Q0EIvqK0spsOfdsiNk9lkzTkzvigUTn1PK5wrzm'
access_token = '882952289450774529-5Yj0dlLI6iir8ZxuyzKhL6W67SE976k'
access_token_secret = 'PaNKscNA383Yd4lQCYyHTomRACMZijPvLk1viy9egFyOu'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define function to clean tweet text
def clean_tweet_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.lower()
    return text

# Define Streamlit app
st.title("Real-time Forest Fire Detection")
st.write("This app detects tweets about forest fires in real-time.")

# Define keyword for searching tweets
keyword = "forest fire OR kebakaran hutan OR kebakaran hutan"

# Create streamlit loop for real-time data streaming
while True:
    try:
        # Get tweets
        tweets = tweepy.Cursor(api.search_tweets, q=keyword, lang='id').items(50)
        
        # Process tweets and classify with the loaded model
        for tweet in tweets:
            text = tweet.text
            cleaned_text = clean_tweet_text(text)
            label = model.predict([cleaned_text])[0]
            if label == 1:
                label = 'Kebakaran'
            elif label == 2:
                label = 'Penanganan'
            else:
                label = 'Bukan Kebakaran'
            st.write(f"{label}: {text}")
        
    except Exception as e:
        st.write("Error:", e)
