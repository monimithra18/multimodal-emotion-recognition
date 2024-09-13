
import numpy as np
from keras.layers import Conv2D, Input, BatchNormalization, MaxPooling2D, Activation, Flatten, Dense, Dropout
from keras.models import Model
from keras.preprocessing import image
import cv2

class EmotionRecognitionModel:
    def __init__(self, input_shape):
        self.model = self._build_model(input_shape)
        self.model.load_weights('models/image/model_weights.hdf5')
        self.face_cascade = cv2.CascadeClassifier('models/image//haarcascade_frontalface_default.xml')
        self.label_dict = {0: 'Angry', 1: 'Disgusting', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}

    def _build_model(self, input_shape):
        X_input = Input((48,48,1))

        X = Conv2D(32, kernel_size=(3,3), strides=(1,1), padding='valid')(X_input)
        X = BatchNormalization(axis=3)(X)
        X = Activation('relu')(X)


        X = Conv2D(64, (3,3), strides=(1,1), padding = 'same')(X)
        X = BatchNormalization(axis=3)(X)
        X = Activation('relu')(X)

        X = MaxPooling2D((2,2))(X)

        X = Conv2D(64, (3,3), strides=(1,1), padding = 'valid')(X)
        X = BatchNormalization(axis=3)(X)
        X = Activation('relu')(X)

        X = Conv2D(128, (3,3), strides=(1,1), padding = 'same')(X)
        X = BatchNormalization(axis=3)(X)
        X = Activation('relu')(X)


        X = MaxPooling2D((2,2))(X)

        X = Conv2D(128, (3,3), strides=(1,1), padding = 'valid')(X)
        X = BatchNormalization(axis=3)(X)
        X = Activation('relu')(X)

        

        X = MaxPooling2D((2,2))(X)
        X = Flatten()(X)
        X = Dense(200, activation='relu')(X)
        X = Dropout(0.6)(X)
        X = Dense(7, activation = 'softmax')(X)

        model = Model(inputs=X_input, outputs=X)
        return model

    def detect_emotion_in_frame(self, cap_image):
        cap_img_gray = cv2.cvtColor(cap_image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(cap_img_gray, 1.3, 5)
        emotion_predictions = []

        if len(faces) == 0:
            return cap_image, ""
            # roi_gray = cap_img_gray
            # roi_gray = cv2.resize(roi_gray, (48, 48))
            # img_pixels = image.img_to_array(roi_gray)
            # img_pixels = np.expand_dims(img_pixels, axis=0)

            # predictions = self.model.predict(img_pixels)
            # emotion_label = np.argmax(predictions)
            # emotion_prediction = self.label_dict[emotion_label]
            # emotion_predictions.append(emotion_prediction)

            # return cap_image, emotion_prediction

        for (x, y, w, h) in faces:
            cv2.rectangle(cap_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = cap_img_gray[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48))
            img_pixels = image.img_to_array(roi_gray)
            img_pixels = np.expand_dims(img_pixels, axis=0)

            predictions = self.model.predict(img_pixels)
            emotion_label = np.argmax(predictions)
            emotion_prediction = self.label_dict[emotion_label]
            emotion_predictions.append(emotion_prediction)

            cv2.putText(cap_image, emotion_prediction, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        return cap_image, emotion_prediction
    



