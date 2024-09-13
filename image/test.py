from deepface import DeepFace
import cv2

# Open the camera
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    try:

        # Perform facial emotion recognition
        result = DeepFace.analyze(frame, actions=['emotion'])

        # Get the dominant emotion prediction
        emotion = result[0]['dominant_emotion']

        # Draw the emotion label on the frame
        cv2.putText(frame, f'Emotion: {emotion}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    except:pass
    # Display the frame
    cv2.imshow('Emotion Recognition', frame)

    # Break the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
