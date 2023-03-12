import os
import re
from flask import Flask, jsonify, request
from twitter_scraper import get_tweets

app = Flask(__name__)

# Define keyword to search for
keyword = 'kebakaran hutan'

# Define function to process text and predict label
def predict_label(text):
    # Map label indices to label text
    label_map = {
        0: 'bukan kebakaran',
        1: 'kebakaran',
        2: 'penanganan'
    }

    # Preprocess text
    text = text.lower()
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation

    # Predict label
    # Replace the following line with your model prediction code
    label = 0

    # Map label index to label text
    label_text = label_map[label]

    return label_text

# Define function to process tweet and predict label
def process_tweet(tweet):
    text = tweet['text']
    label = predict_label(text)
    print(f'Tweet: {text}')
    print(f'Label: {label}')
    print()

# Define endpoint for processing new tweets
@app.route('/process-tweets', methods=['POST'])
def process_tweets():
    tweets = request.get_json()['tweets']

    for tweet in tweets:
        process_tweet(tweet)

    return jsonify({'message': 'Tweets processed successfully.'})

# Stream tweets with keyword and process them in real time
for tweet in get_tweets(keyword, pages=1):
    process_tweet(tweet)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
