import os
import tweepy
from tensorflow.keras.models import load_model
from flask import Flask, jsonify
from twitter_scraper import get_tweets

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'model', 'model.h5')
model = load_model(model_path)

# Initialize Flask app
app = Flask(__name__)

label_map = {
    0: 'bukan kebakaran',
    1: 'kebakaran',
    2: 'penanganan'
}

# Endpoint to fetch tweets and predict labels
@app.route('/tweets')
def get_tweets_endpoint():
    # Crawl tweets about forest fires using Twitter-Scraper
    tweets = get_tweets('kebakaran hutan')

    # Process tweets and construct JSON response
    data = []
    for tweet in tweets:
        text = tweet['text']
        # Predict label
        label = model.predict([text])[0]
        # Map label to tex
        label_text = label_map[label]
        data.append({'text': text, 'label': label_text})

    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*') # Allow cross-domain requests

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
