import os
import openai
from flask import Flask, render_template, request,jsonify
import requests
import json
from flask_cors import CORS
from flask import Flask, request, jsonify
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from flask import render_template
import jwt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# 환경 변수 설정 (다운로드한 JSON 키 파일의 경로를 지정)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "제가 드린 파일의 경로를 쓰시면 됩니다 예-> C:/mslee/capstone/jsonkey/civil-orb-383914-4db936f7a15d.json"

openai.api_key = "gpt api key를 넣으세요"

# 주의 주의 root -> mysql id / csedbadmin -> mysql password
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:csedbadmin@localhost/test'
db = SQLAlchemy(app)

@app.route('/grammar_correction', methods=['POST'])
def grammar_correction():
    data = request.get_json()
    message = data.get('message')

    # Call OpenAI API for grammar correction
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please correct the following sentence: '{message}'",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )

    corrected_message = response.choices[0].text.strip()

    return jsonify(corrected_message)

message = []
@app.route('/set_topic',methods = ['POST'])
def set_topic():
    getTopic = request.get_json()
    topic = "You are a friendly friend of the user. you have to talk about "
    topic += getTopic['topic']
    message.append({"role":"system","content":f"{topic}"})
    return 'OK'

@app.route('/generate', methods = ['POST'])
def answer():
    data = request.get_json()
    
    # Get the token from request
    token = request.json.get('token')
    user_email = get_email_from_token(token)
    user = User.query.filter_by(email=user_email).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # 유저 채팅할때마다 count+1(평균을 구하기 위함)
    if user:
        user.count += 1
    else:
        user.count = user.count

    db.session.add(user)
    db.session.commit()
    ############################
    
    input_text = data['input_text']
    result = []
    result.append({"role":"system","content":"Divide the sentences I said into GRAMMAR, CLARITY, COHERENCE, VOCABULARY, STRUCTURE and give them a score. I can give you a score from 0 to 100 and I hope you give me a score like the example I'm talking about in the future. GRAMMAR: 100 CLARITY: 100 COHERENCE: 80 VOCABULARY: 100 STRUCTURE: 60 You have to give it like an example. You can't write anything more. Just give me a score. Give me an average of the cumulative values of continuously generated score"})
    result.append({"role":"assistant","content":"GRAMMAR: 100 CLARITY: 100 COHERENCE: 100 VOCABULARY: 80 STRUCTURE: 80"})
    result.append({"role":"user","content":f"{input_text}"})
    message.append({"role":"user","content":f"{input_text}"})
    
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0.7,
    top_p=1,
    max_tokens=256,
    messages=message
    )
    
    completion2 = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0.7,
    messages=result
    )

    #점수 추출
    result_text = json.dumps(completion2.choices[0].message["content"]).replace('"', '') 
    scores = re.findall(r'\d+', result_text)  

    #점수 db에 넣기(누적해서)
    if len(scores) == 5: 
        user.gra_score += float(scores[0])
        user.cla_score += float(scores[1])
        user.coh_score += float(scores[2])
        user.voc_score += float(scores[3])
        user.str_score += float(scores[4])
        db.session.commit() 
    ########################################
    print(result)
    print(completion2)

    response_dict = {
        "text":  json.dumps(completion.choices[0].message["content"]).replace('"', ''), # 채팅 메세지
        "other_results": json.dumps(completion2.choices[0].message["content"]).replace('"', '') # 나머지 결과 값
        }
    print(completion["usage"])

    return jsonify(response_dict)   

def transcribe_speech(audio_data):
    client = speech.SpeechClient()
    audio = types.RecognitionAudio(content=audio_data)

    config = types.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=48000,
        language_code='en-US',
        enable_automatic_punctuation=True
    )

    response = client.recognize(config=config, audio=audio)

    if not response.results:
        return "", "No transcription found. Response: " + str(response)

    transcript = response.results[0].alternatives[0].transcript
    return transcript, ""

@app.route('/transcribe', methods=['POST'])
def transcribe():
    audio_file = request.files['audio_file']
    audio_data = audio_file.read()
    transcript, error_message = transcribe_speech(audio_data)

    if error_message:
        print("Error:", error_message)
        return jsonify({'error': error_message})

    print("Transcript:", transcript)
    return jsonify({'transcript': transcript, 'input_text': transcript})

# 토큰을 이용해서 사용자 email 얻기
@app.route('/get_email', methods=['POST'])
def get_email():
    token = request.json.get('token')
    if not token:
        return jsonify({'error': 'Token not provided'}), 400

    user_email = get_email_from_token(token)

    if 'expired' in user_email or 'Invalid' in user_email:
        return jsonify({'error': user_email}), 401

    print("Email extracted from token: ", user_email)

    return jsonify({'email': user_email})
def get_email_from_token(token):
    try:
        # Verify JWT token
        decoded = jwt.decode(token, '78s97df4g75fg68hfsd987fhsdf879hsd786fh4s', algorithms=['HS256'])
        # Extract user email and return
        return decoded.get('sub')  # 'sub' is where we stored the user email in the token
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
#db user table
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    gra_score = db.Column(db.Float)
    cla_score = db.Column(db.Float)
    coh_score = db.Column(db.Float)
    voc_score = db.Column(db.Float)
    str_score = db.Column(db.Float)
    count = db.Column(db.Integer, default=0)
    #chat_text = db.Column(db.String(5000))
    reco_sub1 = db.Column(db.String(255))
    reco_sub2 = db.Column(db.String(255))
    reco_sub3 = db.Column(db.String(255))
    role = db.Column(db.String(255), nullable=False, default="ROLE_USER")


if __name__ == '__main__':
    app.run(debug = True)