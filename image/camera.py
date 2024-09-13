import cv2
import numpy as np
import skimage.transform
from keras.models import model_from_json
import face_recognition

# Load the emotion prediction model
json_file = open("model.json", 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("model_weights.h5")

def predict_emotion(frame, trained_model, categories_list):
    # Find face locations using face_recognition library
    face_locations = face_recognition.face_locations(frame)

    for face_location in face_locations:
        # Extract the face region
        top, right, bottom, left = face_location
        face_roi = frame[top:bottom, left:right]

        # Resize the face image to match the input size of the emotion prediction model
        resized_face = skimage.transform.resize(face_roi, (64, 64, 3))
        x_input = np.asarray(resized_face)
        x_input = np.expand_dims(x_input, axis=0)

        # Make a prediction
        predictions = trained_model.predict(x_input, batch_size=None, verbose=1)
        predicted_label = np.argmax(predictions, axis=-1)[0]
        emotion_label = categories_list[predicted_label]

        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Display the predicted emotion
        cv2.putText(frame, emotion_label, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Emotion Recognition', frame)
categories_list = ['fearful', 'disgusted', 'angry', 'neutral', 'sad', 'surprised', 'happy']

# Open the camera
cap = cv2.VideoCapture(0)

# Counter for skipping frames
frame_count = 0

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Skip frames if the counter is not divisible by 4
    if frame_count % 4 != 0:
        frame_count += 1
        continue

    # Call the predict_emotion function on the frame
    predict_emotion(frame, loaded_model, categories_list)

    # Break the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Increment the frame counter
    frame_count += 1

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
