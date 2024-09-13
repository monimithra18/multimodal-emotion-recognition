import librosa
import librosa.display
import numpy as np
import sys
import warnings
if not sys.warnoptions:
    warnings.simplefilter('ignore')
warnings.filterwarnings('ignore', category=DeprecationWarning) 


header = 'chroma_stft rms spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
for i in range(1, 21):
    header += f' mfcc{i}'
header += ' label'
header = header.split()

def process_audio(taalfile):
    
    print('Processing ',taalfile)
    y, sr = librosa.load(taalfile, mono=True, duration=30)
    rms = librosa.feature.rms(y=y)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    to_append = f' {np.mean(chroma_stft)} {np.mean(rms)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)} '    
    for e in mfcc:
        to_append += f' {np.mean(e)}'
        
    return to_append


from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, BatchNormalization

# Define the sequential model
audio_model = Sequential()

# Adding LSTM layers for audio analysis
audio_model.add(LSTM(128, input_shape=(26, 1), return_sequences=True))
audio_model.add(Dropout(0.2))
audio_model.add(LSTM(64))
audio_model.add(Dropout(0.2))

# Adding Dense layers with BatchNormalization and Dropout
audio_model.add(Dense(256, activation='relu'))
audio_model.add(BatchNormalization())
audio_model.add(Dropout(0.4))
audio_model.add(Dense(128, activation='relu'))
audio_model.add(BatchNormalization())
audio_model.add(Dropout(0.4))

# Final output layer
audio_model.add(Dense(14, activation='softmax'))

# Load the weights
audio_model.load_weights(r"models/audio/model_weights.h5")

outputs = ['male_neutral', 'male_sad', 'male_fear', 'male_happy', 'male_disgust', 'male_angry', 'male_surprise', 'female_surprise', 'female_neutral', 'female_disgust', 'female_fear', 'female_sad', 'female_happy', 'female_angry']
# outputs = ['Neutral', 'Sad', 'Fear', 'Happy', 'Disgust', 'Angry', 'Surprise', 'Surprise', 'Neutral', 'Disgust', 'Fear', 'Sad', 'Happy', 'Angry']

d = dict(zip(outputs, range(0, len(outputs))))

def return_key(val):
    for key, value in d.items():
        if value == val:
            return key
    return 'Key Not Found'

def detect_audio_emotion(file_path):

    live_data = process_audio(file_path)

    live_data_list = []
    for i in live_data.split():
        live_data_list.append(float(i))


    # Assuming live_data_list is a NumPy array
    live_data_list = np.array(live_data_list)

    # Reshape the input to match the expected shape (batch_size, sequence_length, input_features)
    live_data_list = live_data_list.reshape((1, live_data_list.shape[0], 1))

    # Make predictions
    rs = audio_model.predict(live_data_list)

    # Get the index with the highest probability
    predicted_index = np.argmax(rs)

    # Map the index to the corresponding class label
    predicted_class = return_key(predicted_index)

    print("Predicted Class:", predicted_class)

    return predicted_class.replace("female_","").replace("male_","").capitalize()

 