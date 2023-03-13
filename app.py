from flask import Flask, jsonify, request
import numpy as np
import joblib
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from flask_cors import CORS

# Load the GRU model
file = open('model.pkl', 'rb')
model = joblib.load(file)

# Define the tokenizer
tokenizer = Tokenizer(num_words=1000)
tokenizer.fit_on_texts(['kebakaran', 'penanganan', 'bukan'])

# Define the Flask app
app = Flask(__name__)
CORS(app)

# Define the route for the model deployment information
@app.route('/', methods=['GET'])
def home():
    return "Model GRU untuk memprediksi label teks 0, 1, atau 2 telah berhasil di-deploy menggunakan Flask!"

# Define the route for text prediction
@app.route('/predict', methods=['POST'])
def predict():
    # Get the text from the request
    text = request.json['text']
    
    # Preprocess the text
    text_sequence = tokenizer.texts_to_sequences([text])
    text_sequence_padded = pad_sequences(text_sequence, maxlen=100)
    
    # Predict the label for the text
    label_id = np.argmax(model.predict(text_sequence_padded))
    
    # Manipulate the label
    if label_id == 0:
        label = 'bukan kebakaran'
    elif label_id == 1:
        label = 'kebakaran'
    else:
        label = 'penanganan'
    
    # Return the prediction as a JSON response
    return jsonify({'text': text, 'label': label})

# Run the Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
