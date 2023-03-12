from flask import Flask, request, jsonify
import twint
import tensorflow as tf
import numpy as np

# Load model
model = tf.keras.models.load_model('model.h5')

# Define label mapping
label_mapping = {
    0: 'Bukan kebakaran',
    1: 'Kebakaran',
    2: 'Penanganan'
}

# Initialize Twint config
c = twint.Config()

# Set Twint search query
c.Search = 'kebakaran hutan'

# Set Twint callback function
def on_tweet_callback(tweet):
    # Get tweet text
    tweet_text = tweet.tweet

    # Preprocess tweet text
    tweet_text = preprocess_text(tweet_text)

    # Convert tweet text to vector
    tweet_vector = text_to_vector(tweet_text)

    # Make prediction using model
    prediction = model.predict(tweet_vector)

    # Get predicted label
    predicted_label = np.argmax(prediction)

    # Get label name from mapping
    label_name = label_mapping[predicted_label]

    # Construct response JSON
    response = {
        'post': tweet_text,
        'label': label_name
    }

    # Send response JSON
    send_response(response)

# Set Twint callback
c.Callback = on_tweet_callback

# Set Twint limit
c.Limit = 10

# Set Twint hide output
c.Hide_output = True

# Start Twint search
twint.run.Search(c)

# Initialize Flask app
app = Flask(__name__)

# Define prediction function
def predict_label(tweet_text):
    # Preprocess tweet text
    tweet_text = preprocess_text(tweet_text)

    # Convert tweet text to vector
    tweet_vector = text_to_vector(tweet_text)

    # Make prediction using model
    prediction = model.predict(tweet_vector)

    # Get predicted label
    predicted_label = np.argmax(prediction)

    # Get label name from mapping
    label_name = label_mapping[predicted_label]

    return label_name

# Define preprocessing function
def preprocess_text(text):
    # Implement your text preprocessing logic here
    # ...
    return text

# Define text to vector function
def text_to_vector(text):
    # Implement your text to vector conversion logic here
    # ...
    return vector

# Define send response function
def send_response(response):
    # Implement your response sending logic here
    # ...
    print(response)

# Define endpoint for predicting label
@app.route('/predict', methods=['POST'])
def predict():
    # Get request data
    data = request.json

    # Get tweet text from request data
    tweet_text = data['tweet']

    # Predict label using model
    predicted_label = predict_label(tweet_text)

    # Construct response JSON
    response = {
        'post': tweet_text,
        'label': predicted_label
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
