from flask import Flask, render_template, request, jsonify
import os
import boto3
from botocore.exceptions import ClientError
import json
from dotenv import load_dotenv

app = Flask(__name__)

# 環境変数の読み込み
load_dotenv()

# Amazon Bedrock Runtime clientの作成
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name=os.getenv('AWS_DEFAULT_REGION')
)

# モデルIDの設定
model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"  # 作成したモデルのIDを指定
accept = "application/json"
contentType = "application/json"


def generate_content(prompt, conversation_history=[]):
    try:
        body = {
            "anthropic_verson" : "bedrock-2023-05-31",
            "max_tokens": 500,
            "temperature": 0.7,
            "top_p": 0.9,
            "messages":[
                {
                    "role": "user",
                    "content": f"\n\nHuman: Generate HTML content based on the following prompt: {prompt}\n\nAssistant: Here's the HTML content based on your prompt:\n\n",
                }
            ],
        }

        if conversation_history:
            body["prompt"] = "\n\n".join(conversation_history) + body["prompt"]

        response = bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
            accept=accept,
            contentType=contentType
        )
        
        response_body = json.loads(response.get('body').read())
        return response_body.get('content')[0].get("text")

    except ClientError as e:
        print(f"An error occurred: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        conversation_history = request.form.get('conversation_history', '').split('||')
        response = generate_content(prompt, conversation_history)
        
        if response:
            conversation_history.append(f"Human: {prompt}")
            conversation_history.append(f"Assistant: {response}")
            return jsonify({
                'response': response,
                'conversation_history': '||'.join(conversation_history)
            })
        else:
            return jsonify({'error': 'Failed to generate content'}), 500

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)