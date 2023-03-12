import os
import tweepy
from tensorflow.keras.models import load_model
from flask import Flask, jsonify

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'model', 'model.h5')
model = load_model(model_path)

# Twitter API credentials
bearer_token = 'AAAAAAAAAAAAAAAAAAAAALa8dgEAAAAAeBV0JiJMVZ9925dYnd%2BZcrkh0cM%3DDpJjkv1LBp0Dla1SDuhgpzCdeZvoYY80HLXW52Tn1JqP93JU2c'

# Initialize Twitter API client
auth = tweepy.AppAuthHandler(bearer_token=bearer_token)
api = tweepy.API(auth)

# Initialize Flask app
app = Flask(__name__)

label_map = {
    0: 'bukan kebakaran',
    1: 'kebakaran',
    2: 'penanganan'
}

# Endpoint to fetch tweets and predict labels
@app.route('/tweets')
def get_tweets():
    # Crawl tweets about forest fires
    tweets = api.search_tweets(q='kebakaran hutan', count=50)

    # Process tweets and construct JSON response
    data = []
    for tweet in tweets:
        text = tweet.text
        # Predict label
        label = model.predict([text])[0]
        # Map label to text
        label_text = label_map[label]
        data.append({'text': text, 'label': label_text})

    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*') # Allow cross-domain requests

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
