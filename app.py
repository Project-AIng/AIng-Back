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


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# 환경 변수 설정 (다운로드한 JSON 키 파일의 경로를 지정)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "제가 드린 파일의 경로를 쓰시면 됩니다 예-> C:/mslee/capstone/jsonkey/civil-orb-383914-4db936f7a15d.json"

openai.api_key = "gpt api key를 넣으세요"

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
    #top_p=1,
    messages=result
    )
    print(result)
    print(completion2)
   
    
    # JSON 형식으로 클라이언트 측에 보내주기 위해 딕셔너리에 저장
    response_dict = {
        "text":  json.dumps(completion.choices[0].message["content"]).replace('"', ''), # 채팅 메세지
        "other_results": json.dumps(completion2.choices[0].message["content"]).replace('"', '') # 나머지 결과 값
        }
    print(completion["usage"])
    return jsonify(response_dict)

def index():
    return render_template('index.html')


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


if __name__ == '__main__':
    app.run(debug = True)
