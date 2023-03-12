import os
import twitter
from tensorflow.keras.models import load_model
from flask import Flask, jsonify

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'model', 'model.h5')
model = load_model(model_path)

# Twitter API credentials
consumer_key = 'u9D8IF1iOVWaoRy24598GyRq9'
consumer_secret = 'WYOe2e2Nkb2Q0EIvqK0spsOfdsiNk9lkzTkzvigUTn1PK5wrzm'
access_token = '882952289450774529-NIYPtaMdpiJCbAVSINxORsjS0Ba2GaO'
access_secret = 'LWuTR82dsTKdoK6AZ4j9SdDNbJhHDHlyBUDGO2fNLZxKe'

# Initialize Twitter API client
api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token,
                  access_token_secret=access_secret)

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
    tweets = api.GetSearch(term='kebakaran hutan', count=50)

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
