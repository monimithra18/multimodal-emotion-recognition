import cv2
import time
import random
import numpy as np
from PIL import Image
from io import BytesIO
from flask import jsonify
from app.main import main_bp
from base64 import b64encode
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from flask_wtf.file import FileAllowed
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from app.main.camera import Camera, VideoFile
from source.text_emotion_detector import make_prediction
from source.audio_emotion_detector import detect_audio_emotion
from source.face_emotion_detector import EmotionRecognitionModel
from source.recommendation_model import generate_final_result
from flask import render_template, Response, flash, request

emotion_model = EmotionRecognitionModel((64, 64, 1))

@main_bp.route("/")
def login():
    return render_template("login.html")

@main_bp.route("/login")
def login1():
    return render_template("login.html")

@main_bp.route("/index")
def login2():
    return render_template("login.html")

@main_bp.route("/home")
def home_page():
    return render_template("home_page.html")


def gen(camera):
    global emotion_data

    while True:
        frame = camera.get_frame()

        if frame is not None:
            image_output = emotion_model.detect_emotion_in_frame(frame)
            # print("Image Emotion : " + image_output[1])

            if image_output[1] !="":
                emotion_data['faceEmotion'] = image_output[1]

            frame_processed = image_output[0]
            frame_processed = cv2.imencode('.jpg', frame_processed)[1].tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_processed + b'\r\n')
        else:
            print("No frame available")

@main_bp.route('/video_feed')
def video_feed():
    return Response(gen(
        Camera()
    ),
        mimetype='multipart/x-mixed-replace; boundary=frame')



@main_bp.route('/video_file_feed')
def video_file_feed():
    return Response(gen(
        VideoFile()
    ),
        mimetype='multipart/x-mixed-replace; boundary=frame')


def allowed_file(filename):
    ext = filename.split(".")[-1]
    is_good = ext in ["jpg", "jpeg", "png","wav"]
    return is_good


# form
class PhotoMaskForm(FlaskForm):
    image = FileField('Choose image:',
                      validators=[
                          FileAllowed(['jpg', 'jpeg', 'png'], 'The allowed extensions are: .jpg, .jpeg and .png')])

    submit = SubmitField('Detect Emotion')


 


@main_bp.route('/process_audio', methods=['POST'])
def process_audio():

    try:
        audio_file = request.files.get('audio')

        if audio_file and allowed_file(audio_file.filename):
            filename = secure_filename(audio_file.filename)
            audio_path = "uploaded_files/" + filename
            audio_file.save(audio_path)


            print("file saved"+audio_path)

            # Convert the audio file to WAV format using pydub
            audio = AudioSegment.from_file(audio_path, format='webm')
            audio.export(audio_path, format='wav')


            print("file saved"+audio_path)

            # Use SpeechRecognition to convert audio to text
            recognizer = sr.Recognizer()
            print("file Recognizer")

            with sr.AudioFile(audio_path) as source:
                audio_data = recognizer.record(source)

            print("file AudioFile")

            try:

                print("file recognizer")
                # Perform speech-to-text conversion
                text_result = recognizer.recognize_google(audio_data)
                
                print(text_result)
                result = {'text_result': text_result, 'sentiment': 'happy', 'audio_path': audio_path}
                
                return jsonify(result)

            except sr.UnknownValueError:
                # Speech Recognition could not understand the audio
                return jsonify({'error': 'Speech Recognition could not understand the audio'}), 400

            except sr.RequestError as e:
                # Could not request results from Google Speech Recognition service
                return jsonify({'error': f'Could not request results from Google Speech Recognition service: {e}'}), 500
            
            except Exception as e:
                print(e)
                import traceback
                traceback.print_exc()
    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()

    return jsonify({'error': 'Invalid file'}), 400


@main_bp.route('/process_audio_and_transcript', methods=['POST'])
def process_audio_and_transcript():
    global emotion_data
    try:
        # Get the audio file and transcript from the request
        audio_file = request.files['audio']
        transcript = request.form['transcript']

        print('Transcript:', transcript)

        if transcript !='':
            text_emotion = make_prediction(transcript)
            emotion_data['textEmotion'] = text_emotion
            print("Text Emotion L "+text_emotion)
            audio_path = "uploaded_files/" + audio_file.filename
            # Save the audio file
            audio_file.save(audio_path)
            time.sleep(1)
            emotion_data['audioEmotion'] = text_emotion

            print("Audio Emotion : "+detect_audio_emotion(audio_path))


        # Return a JSON response (you can customize this based on your needs)
        return jsonify({'status': 'success', 'message': 'Audio and transcript processed successfully'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


# Dummy data for testing
emotion_data = {
    'faceEmotion': ' ',
    'audioEmotion': ' ',
    'textEmotion': ' ',
    'finalResult': '  ',
    'recommendedQuote': ' ',
    'recommendedSong': ' ',
}


@main_bp.route('/get_emotion_info')
def get_emotion_info():
    global emotion_data
    emotion_data = generate_final_result(emotion_data)

    return jsonify(emotion_data)




@main_bp.route('/audio_test')
def audio_test():
    return render_template('audio_test.html')

@main_bp.route('/upload', methods=['POST'])
def upload_audio():
    audio_file = request.files['audio_data']
    audio_file.save('uploaded_files/recording.wav')

    return {'message': 'Audio file received successfully'}
