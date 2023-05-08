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
prompt = ["remember the previous conversation and chat basend on the conversation you received",'show english score from 0 to 100 about grammar, expression, vocabulary, context.', 'only show me why you scored this english sentence each other grammar,expression, vocabulary, context.','only show you change my sentence better.']




messages = []
messages.append({"role":"system","content":"we will talk about love"})
@app.route('/generate', methods = ['POST'])
def answer():
    data = request.get_json()
    input_text = data['input_text']
    result = []
    result.append({"role":"system","content":"only show english score from 0 to 100 about grammar, expression, vocabulary, context. and show you change my sentence better"})
    result.append({"role":"user","content":f"{input_text}"})
    messages.append({"role":"user","content":f"{input_text}"})
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0.7,
    top_p=1,
    messages=messages
    )
    completion2 = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0.7,
    top_p=1,
    messages=result
    )
   
    
    # JSON 형식으로 클라이언트 측에 보내주기 위해 딕셔너리에 저장
    response_dict = {
        "text":  json.dumps(completion.choices[0].message["content"]).replace('"', ''), # 채팅 메세지
        "other_results": json.dumps(completion2.choices[0].message["content"]).replace('\n', ' ') # 나머지 결과 값
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