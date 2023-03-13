from flask import Flask, jsonify, request
import numpy as np
from keras.models import load_model

# Load the GRU model
model = load_model('model.h5')

# Define the Flask app
app = Flask(__name__)

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
    # ...
    
    # Predict the label for the text
    label_id = np.argmax(model.predict(text))
    
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
    app.run()
