import tweepy
from tensorflow.keras.models import load_model

# Load model
model_path = 'model.h5'
model = load_model(model_path)

# Set up Twitter API credentials
consumer_key = 'u9D8IF1iOVWaoRy24598GyRq9'
consumer_secret = 'WYOe2e2Nkb2Q0EIvqK0spsOfdsiNk9lkzTkzvigUTn1PK5wrzm'
access_token = '882952289450774529-NIYPtaMdpiJCbAVSINxORsjS0Ba2GaO'
access_token_secret = 'LWuTR82dsTKdoK6AZ4j9SdDNbJhHDHlyBUDGO2fNLZxKe'

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Initialize Tweepy API client
api = tweepy.API(auth)

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
    
    # Predict label
    label = model.predict([text])[0]
    
    # Map label index to label text
    label_text = label_map[label.argmax()]
    
    return label_text

# Define function to process tweet and predict label
def process_tweet(tweet):
    text = tweet.text
    label = predict_label(text)
    print(f'Tweet: {text}')
    print(f'Label: {label}')
    print()

# Stream tweets with keyword and process them in real time
stream = tweepy.Stream(auth=api.auth, listener=None)
stream.filter(track=[keyword], is_async=True, languages=['id'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
