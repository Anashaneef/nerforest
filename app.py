import os
import tweepy
from tensorflow.keras.models import load_model
from flask import Flask, jsonify

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'model', 'model.h5')
model = load_model(model_path)

# Twitter API credentials
consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_token'
access_secret = 'your_access_secret'

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
