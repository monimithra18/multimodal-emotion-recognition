import re
import string
import demoji
import numpy as np
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing import sequence

import pickle

# Loading the tokenizer (for example)
with open('models/text/tokenizer.pickle', 'rb') as handle:
    loaded_tokenizer = pickle.load(handle)

max_words = 30
# Download the demoji library data
demoji.download_codes()

# Define a function to clean the text data
def clean_text(text):
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    
    # Remove retweet tags and mentions
    text = re.sub('(RT|via)((?:\\b\\W*@\\w+)+)', ' ', text)
    text = re.sub(r'@\S+', '', text)
    
    # Remove emojis
    text = demoji.replace(text, '')
    
    # Remove special characters and symbols
    text = re.sub(r'[^\w\s]', '', text)
    
    # Convert all text to lowercase
    text = text.lower()
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word not in stop_words])
    
    # Remove any remaining noise
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    return text


from keras.models import model_from_json

json_file = open(r"models/text/model.json", 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights(r"models/text/model_weights.h5")
 
def preprocess_text(comment):
    # Add the same preprocessing steps you applied to the training data
    clean_comment = clean_text(comment)
    tokenized_comment = loaded_tokenizer.texts_to_sequences([clean_comment])
    padded_comment = sequence.pad_sequences(tokenized_comment, maxlen=max_words)
    return padded_comment

def make_prediction(comment):
    preprocessed_comment = preprocess_text(comment)
    prediction = np.argmax(loaded_model.predict(preprocessed_comment), axis=1)
    if prediction == 0:
        return "Negative"
    elif prediction == 1:
        return "Neutral"
    elif prediction == 2:
        return "Positive"
    else:
        return "Unknown"
