import os
import tweepy
import pickle
from flask import Flask, jsonify

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'model', 'model_1.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Twitter API credentials
consumer_key = 'u9D8IF1iOVWaoRy24598GyRq9'
consumer_secret = 'WYOe2e2Nkb2Q0EIvqK0spsOfdsiNk9lkzTkzvigUTn1PK5wrzm'
access_token = '882952289450774529-NIYPtaMdpiJCbAVSINxORsjS0Ba2GaO'
access_secret = 'LWuTR82dsTKdoK6AZ4j9SdDNbJhHDHlyBUDGO2fNLZxKe'

# Initialize Tweepy API client
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# Initialize Flask app
app = Flask(__name__)

# Endpoint to fetch tweets and predict labels
@app.route('/tweets')
def get_tweets():
    # Crawl tweets about forest fires
    tweets = api.search(q='kebakaran hutan', count=50)
    
    # Process tweets and predict labels
    data = []
    for tweet in tweets:
        text = tweet.text
        label = model.predict(text)[0]
        data.append({'text': text, 'label': label})
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
