import os
import boto3
from botocore.exceptions import ClientError
import json
from dotenv import load_dotenv
import argparse


# Amazon Bedrock Runtime clientの作成
try:
    bedrock = boto3.client(
        service_name='bedrock-runtime',
        region_name='ap-northeast-1'
    )
except Exception as e:
    print(f"Failed to create Bedrock client: {e}")
    bedrock = None

# モデルIDの設定
model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
accept = "application/json"
contentType = "application/json"

def generate_content(prompt, conversation_history=[]):
    if not bedrock:
        print("Bedrock client is not initialized")
        return None

    try:
        messages = []
        for i, message in enumerate(conversation_history):
            role = "user" if i % 2 == 0 else "assistant"
            messages.append({"role": role, "content": message})

        messages.append({
            "role": "user",
            "content": f"Generate HTML content based on the following prompt: {prompt}"
        })

        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "temperature": 0.7,
            "top_p": 0.9,
            "messages": messages
        }

        response = bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
            accept=accept,
            contentType=contentType
        )
        
        response_body = json.loads(response.get('body').read())
        return response_body['content'][0]['text']

    except ClientError as e:
        print(f"Bedrock ClientError: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in generate_content: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Generate content using Amazon Bedrock")
    parser.add_argument("prompt", help="The prompt for content generation")
    parser.add_argument("--history", help="Conversation history, separated by ||", default="")
    args = parser.parse_args()

    conversation_history = args.history.split('||') if args.history else []
    response = generate_content(args.prompt, conversation_history)

    if response:
        print("Generated content:")
        print(response)
        
        conversation_history.append(f"Human: {args.prompt}")
        conversation_history.append(f"Assistant: {response}")
        print("\nUpdated conversation history:")
        print('||'.join(conversation_history))
    else:
        print("Failed to generate content")

if __name__ == '__main__':
    main()