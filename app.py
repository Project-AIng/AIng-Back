import os
import openai
from flask import Flask, render_template, request,jsonify
import requests
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3001"}})

openai.api_key = "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"
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

if __name__ == '__main__':
    app.run(debug = True)