# Use the native inference API to send a text message to Anthropic Claude
# and print the response stream.

import boto3
import json

from questions_mysql import QuestionsMysql

class AnthropicBedRockAPI(object):
    def __init__(self):
        # Create a Bedrock Runtime client in the AWS Region of your choice.
        self.client = boto3.client("bedrock-runtime", region_name="us-west-2")

    def ask_claude(self, question, model_id):
        # Format the request payload using the model's native structure.
        native_request = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 512,
            "temperature": 0,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": question}],
                }
            ],
        }

        # Convert the native request to JSON.
        request = json.dumps(native_request)

        # Invoke the model with the request.
        streaming_response = self.client.invoke_model_with_response_stream(
            modelId=model_id, body=request
        )

        res = ""
        # Extract and print the response text in real-time.
        for event in streaming_response["body"]:
            chunk = json.loads(event["chunk"]["bytes"])
            if chunk["type"] == "content_block_delta":
                print(chunk["delta"].get("text", ""), end="")
                res += chunk["delta"].get("text", "")
        return res


if __name__ == '__main__':
    api = AnthropicBedRockAPI()
    qsql = QuestionsMysql()
    question_dict = qsql.get_questions()
    response_claude = ""
    
    for startIndex in range (1, len(question_dict) + 1, 1):
        prompt_str = qsql.get_prompt_string(question_dict, startIndex, 1)
        print(prompt_str)
        response_claude += api.ask_claude(prompt_str, "anthropic.claude-3-opus-20240229-v1:0")
        response_claude += "\n"
        #print(response_claude)
    print(response_claude)
    score_claude = qsql.get_score(response_claude, question_dict)

    print("\n")
    print('Claude 3 Opus: ' + score_claude)
