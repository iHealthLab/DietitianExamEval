# Send a prompt to Meta Llama 3 and print the response stream in real-time.

import boto3
import json

from questions_mysql import QuestionsMysql

class LlamaBedRockAPI(object):
    def __init__(self):
        # Create a Bedrock Runtime client in the AWS Region of your choice.
        self.client = boto3.client("bedrock-runtime", region_name="us-west-2")
    
    def ask_llama(self, question, model_id):
        # Embed the message in Llama 3's prompt format.
        prompt = f"""
        <|begin_of_text|>
        <|start_header_id|>user<|end_header_id|>
        {question}
        <|eot_id|>
        <|start_header_id|>assistant<|end_header_id|>
        """

        # Format the request payload using the model's native structure.
        request = {
            "prompt": prompt,
            # Optional inference parameters:
            "max_gen_len": 512,
            "temperature": 0.5,
            "top_p": 0.9,
        }

        # Encode and send the request.
        response_stream = self.client.invoke_model_with_response_stream(
            body=json.dumps(request),
            modelId=model_id,
        )

        res = ""
        # Extract and print the response text in real-time.
        for event in response_stream["body"]:
            chunk = json.loads(event["chunk"]["bytes"])
            if "generation" in chunk:
                print(chunk["generation"], end="")
                res += chunk["generation"]
        return res

if __name__ == '__main__':
    api = LlamaBedRockAPI()

    qsql = QuestionsMysql()
    question_dict = qsql.get_questions()
    response_llama = ""
    
    for startIndex in range (1, len(question_dict) + 1, 20):
        prompt_str = qsql.get_prompt_string_llama(question_dict, startIndex, 20)
        #print(prompt_str)
        response_llama += api.ask_llama(prompt_str, "meta.llama3-8b-instruct-v1:0")
        response_llama += "\n"
        #print(response_llama)
    
    with open('gpt_answer_RD_questions_llama.txt', 'w') as file:
        file.write(response_llama + "\n")

    score_claude = qsql.get_score(response_llama, question_dict)

    print("\n")
    print('Llama 3 8B: ' + score_claude)

