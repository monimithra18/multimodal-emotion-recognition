# Multimodal Emotion Recognition

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=keras&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

A real-time emotion recognition system that combines **text**, **image**, and **audio** analysis into a unified multi-modal pipeline. Unlike traditional single-modality approaches, this system captures the full complexity of human emotions by processing all three data types simultaneously.

---

## 🧠 Overview

Traditional emotion recognition models rely on a single modality (e.g. only facial expressions or only speech), which limits accuracy in real-world scenarios. This project overcomes that limitation by fusing three complementary modalities:

- 📝 **Text** — Sentiment and emotion from written language
- 🖼️ **Image** — Facial expression analysis using CNNs
- 🔊 **Audio** — Emotional speech recognition using MFCC + LSTM

---

## 🗂 Project Structure

```
multimodal-emotion-recognition/
├── text/          # Text-based emotion model (LSTM + NLP pipeline)
├── audio/         # Audio-based emotion model (MFCC + LSTM)
├── image/         # Image-based emotion model (CNN + FER dataset)
├── web/           # Real-time web interface for all three modalities
└── README.md
```

---

## 📊 Datasets

| Modality | Dataset | Description |
|---|---|---|
| Text | bitcointweets.csv | Tweet sentiment analysis |
| Audio | RAVDESS + TESS | Emotional speech recordings |
| Image | emotion-detection-fer | Facial expression recognition dataset |

---

## 🛠 Models & Techniques

**Text:**
- Tokenization, lemmatization, and stop word removal
- LSTM networks for sequential text classification
- Accuracy: **96%**

**Audio:**
- MFCC (Mel-Frequency Cepstral Coefficients) for feature extraction
- LSTM for temporal audio pattern classification
- Accuracy: **89%**

**Image:**
- Convolutional Neural Networks (CNNs) for facial expression detection
- Real-time inference from webcam or image input
- Accuracy: **91%**

---

## ⚙️ How It Works

1. Input is received via text, audio, or image (or all three simultaneously)
2. Each modality is processed by its dedicated model
3. Predictions from each model are combined for cross-modal analysis
4. Final emotion output is returned with confidence scores

---

## 🚀 Getting Started

```bash
# Clone the repo
git clone https://github.com/monimithra18/multimodal-emotion-recognition.git
cd multimodal-emotion-recognition

# Install dependencies
pip install tensorflow keras scikit-learn librosa pandas numpy opencv-python

# Run individual modality notebooks or the web interface
cd web && python app.py
```

---

## 📈 Results

| Modality | Accuracy |
|---|---|
| Text Model | 96% |
| Audio Model | 89% |
| Image Model | 91% |

Cross-modal fusion consistently outperforms any single modality by capturing complementary emotional signals.

---

## 🔭 Future Work

- Cross-modal integration with unified fusion layer
- Support for multiple languages
- Edge computing implementation for low-latency inference
- Collaboration with psychology and cognitive science for improved labelling

---

*Built by [Monish Mithra Kadiyala](https://linkedin.com/in/monishmithra) · MS Data Science @ University at Buffalo*
