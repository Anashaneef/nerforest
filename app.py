from flask import Flask, jsonify, request
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

app = Flask(__name__)

# Load trained model
model = load_model('model.h5')

# Initialize tokenizer with vocabulary size of 10000
tokenizer = Tokenizer(num_words=10000)

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from request
    data = request.json
    tweet = data['tweet']

    # Tokenize text
    tokenizer.fit_on_texts(tweet)
    sequences = tokenizer.texts_to_sequences(tweet)

    # Pad sequences
    sequences_padded = pad_sequences(sequences, maxlen=100, padding='post', truncating='post')

    # Make predictions
    predictions = model.predict(sequences_padded)

    # Convert predictions to labels
    labels = np.argmax(predictions, axis=1)

    # Return predictions as JSON
    return jsonify({'predictions': labels.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
