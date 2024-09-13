import random

def generate_final_result(emotion_data):
    # Extract emotions from the input data
    face_emotion = emotion_data['faceEmotion']
    audio_emotion = emotion_data['audioEmotion']
    text_emotion = emotion_data['textEmotion']

    final_emotions_state = {
        'Positive': 0,
        'Negative': 0
    }

    if face_emotion in ['Happy', 'Surprise', 'Positive', 'Neutral']:
        final_emotions_state['Positive'] += 1
    if audio_emotion in ['Happy', 'Surprise', 'Positive', 'Neutral']:
        final_emotions_state['Positive'] += 1
    if text_emotion in ['Happy', 'Surprise', 'Positive', 'Neutral']:
        final_emotions_state['Positive'] += 1

    if face_emotion in ['Angry', 'Disgusting', 'Fear', 'Negative', 'Sad']:
        final_emotions_state['Negative'] += 1
    if audio_emotion in ['Angry', 'Disgusting', 'Fear', 'Negative', 'Sad']:
        final_emotions_state['Negative'] += 1
    if text_emotion in ['Angry', 'Disgusting', 'Fear', 'Negative', 'Sad']:
        final_emotions_state['Negative'] += 1
        
    emotion_data['finalResult'] = max((k for k, v in final_emotions_state.items() if v != 0), key=lambda k: (final_emotions_state[k], k), default=None)

    # Selecting a random positive or negative quote based on the final emotion
    if emotion_data['finalResult'] == 'Positive':
        emotion_data['recommendedQuote'] = random.choice([
            "Positive vibes fuel your journey, but keep your focus on the road ahead. Safety first, excitement second.",
            "Stay positive, drive safe. Let the joy of the journey be your fuel, not the speed of it.",
            "Positive energy propels you forward, but careful driving ensures a smooth ride. Stay positive, drive responsibly.",
            "Let the positivity in your heart drive you, but let caution steer the wheel. Enjoy the journey responsibly.",
            "Positive thoughts lead to positive journeys. Drive safely, savor the moments, and cherish the road.",
            "In the midst of positivity, stay grounded and drive responsibly. Safety is the ultimate destination.",
            "A positive attitude makes for a smoother ride, but a careful approach ensures you enjoy the journey longer.",
            "Stay positive, drive carefully, and let the road be a canvas for your joyful journey.",
            "Excitement is the spice of life, but safe driving is the recipe for a fulfilling journey. Positive and cautious – the perfect mix.",
            "Positivity in, safety on. Let the joy of the road be your companion, but caution be your guide.",
            "A positive mindset opens the door to adventure, but careful driving ensures you embrace it fully.",
            "Drive with the joy of a positive spirit, but let safety be the melody that accompanies your journey.",
            "Positivity accelerates the journey, but careful driving ensures you enjoy every mile.",
            "Stay positive, drive focused. The road to happiness is best traveled with a clear mind and a careful foot on the pedal.",
            "Positive energy fuels your ride, but let the steering wheel remind you to stay on the right path."
        ])
    elif emotion_data['finalResult'] == 'Negative':
        emotion_data['recommendedQuote'] = random.choice([
            "In challenging times, be cautious with your decisions and confident in your actions.",
            "When the road gets tough, take it slow. Being careful today ensures a smoother journey tomorrow.",
            "Being careful doesn't mean you're afraid; it means you're wise and mindful of the road ahead.",
            "Amidst challenges, being careful is a strength, not a weakness. Drive safely through the storm.",
            "Negativity may surround you, but being careful is your shield. Navigate through with caution.",
            "Every step forward, no matter how small, is a step in the right direction. Be careful but keep moving.",
            "Carefulness is the key to turning obstacles into stepping stones on your journey.",
            "In the face of negativity, tread carefully and let caution guide you to brighter paths.",
            "Being careful is a sign of intelligence, not fear. Take each turn with thoughtfulness and precision.",
            "Amidst the negativity, your caution is your best defense. Drive carefully; you'll reach your destination.",
            "On the road of life, being careful is not a detour; it's a necessary part of the journey.",
            "Negative thoughts are like potholes; navigate carefully to avoid unnecessary bumps.",
            "In the midst of negativity, being careful is a courageous act. Choose each step wisely.",
            "Being careful is not a sign of weakness; it's a commitment to your well-being. Drive with caution.",
            "Negativity may try to distract you, but being careful ensures you stay on the right path."
        ])

    # Selecting a random positive or negative song based on the final emotion
    if emotion_data['finalResult'] == 'Positive':
        emotion_data['recommendedSong'] = random.choice([
            "Ude Dil Befikre",
            "Kar Har Maidaan Fateh",
            "Happy Budday",
            "Zindagi Na Milegi Dobara",
            "Dil Dhadakne Do",
            "Ainvayi Ainvayi",
            "Chak De India",
            "Sooraj Dooba Hai",
            "Gallan Goodiyaan",
            "Badri Ki Dulhania",
            "Dil Chahta Hai",
            "Zara Sa",
            "Ae Watan",
            "London Thumakda",
            "Ae Dil Hai Mushkil",
            "Chak Lein De",
            "Karle Gunaah",
            "Yun Hi Chala Chal",
            "Tera Ban Jaunga",
            "Muskurane Ki Wajah Tum Ho"
        ])
    elif emotion_data['finalResult'] == 'Negative':
        emotion_data['recommendedSong'] = random.choice([
            "Sooraj Dooba Hai",
            "Ilahi",
            "Taake Jhanke",
            "Safarnama",
            "Khul Kabhi Toh",
            "Hawa Hawa",
            "Roke Na Ruke Naina",
            "Challa",
            "Roobaroo",
            "Aaj Ki Raat",
            "Chak De India",
            "Zinda",
            "Kar Har Maidaan Fateh",
            "Aashayein",
            "Ziddi Dil",
            "Koi Kahe Kehta Rahe",
            "Manzar Naya",
            "Jeetenge Hum",
            "Nadaan Parindey",
            "Maula Mere Lele Meri Jaan"
        ])

    return emotion_data