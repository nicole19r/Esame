#Importazione delle librerie
from flask import Flask, jsonify, request
from flask_cors import CORS
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import pickle

#Vengono importati modello e vectorizer
with open('../Modello.pkl', 'rb') as f:
    classifier = pickle.load(f)

with open('../Vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

#Definizione del server Flask
app = Flask(__name__)
app.config.from_object(__name__)

#Definizione delle regole di accesso alle richieste
CORS(app, resources={r'/*': {'origins': '*'}})

#Scarico e definisco dei componenti per il processamento del testo
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

#Funzione per processare il testo e quindi tokenizzare, lemmatizzatizzare in minuscolo e togliere gli stopwords
def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word.lower()) for word in tokens if word.isalnum()]
    tokens = [word for word in tokens if not word in stop_words]
    return ' '.join(tokens)

#Il testo viene processato e poi viene predetta l'emozione
def emotion_text(text):
    preprocessed_text = preprocess_text(text)
    X_test_text = vectorizer.transform([preprocessed_text])
    emotion_prediction = classifier.predict(X_test_text)
    return emotion_prediction[0]

#Funzione che accetta la richesta per esaminare quale emozione è presente
@app.route('/esamina', methods=['POST'])
def analysis():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        #Si prende il testo passato dal client e lo si passa alla funzione per individuare l'emozione
        result = emotion_text(post_data.get('text'))
        response_object['emotion'] = str(result)
    #La risposta viene inviata al client in formato JSON
    return jsonify(response_object)

#Viene avviato il server
if __name__ == '__main__':
    app.run()