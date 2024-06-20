# Use the native inference API to send a text message to Anthropic Claude
# and print the response stream.

import boto3
import json

from questions_mysql import QuestionsMysql

class AnthropicBedRockAPI(object):
    """
    This class connects to Amazon BedRock API for Anthropic/Claude AI.
    """
    def __init__(self):
        # Create a Bedrock Runtime client in the AWS Region of your choice.
        self.client = boto3.client("bedrock-runtime", region_name="us-west-2")

    def ask_claude(self, question, model_id, temp):
        # Format the request payload using the model's native structure.
        native_request = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 512,
            "temperature": temp,
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
    # Connect to RD Exam Questions
    question_dict = qsql.get_RD_questions()
    # Connect to CDCES Exam Questions
    # question_dict = qsql.get_questions()

    # Asks the incorrect questions with choices only, allowing explanation and no restriction in answer format
    '''
    prompt_str = ""
    question_list = [32, 39, 43, 55, 60, 65, 83, 94, 111, 114, 127, 130, 133, 135, 148, 157, 177, 188, 192, 193, 211, 216, 218, 225, 233, 258, 259, 270, 273, 275, 291, 292, 299, 300, 303, 311, 312, 313, 324, 331, 354, 357, 368, 374, 375, 378, 379, 383, 387, 389, 392, 394, 400, 401, 408, 412, 415, 423, 429, 442, 446, 447, 457, 460, 477, 523, 528, 537, 540, 548, 560, 571, 607, 622, 632, 643, 644, 649, 657, 659, 661, 668, 678, 680, 689, 705, 708, 716, 720, 723, 728, 735, 737, 759, 767, 790, 813, 815, 840, 851, 864, 874, 877, 914, 916, 930, 977, 991, 1009, 1013, 1033, 1040, 1043, 87, 934, 10, 56, 142, 185, 186, 348, 369, 463, 507, 822, 947, 971, 71, 285, 337, 952, 953, 984]
    for i in question_list:
        question = question_dict[i]
        
        with open('claude_3_answer_incorrect_RD_questions_with_explanation.txt', 'r') as file:
            content = file.read()

        prompt_str = question['question'] + "\n" + question['choices']
        question_str = str(question['question_id']) + ". " + prompt_str + "\n\nDifficulty Level: " + question['difficulty_level'] + "\n\nCorrect Answer: " + question['answer'] + "\n\nExplanation: " + question['explanation'] + "\n\nReferences: " + question['answer_references'] + "\n\nClaude 3 Response: \n"
        response = api.ask_claude(prompt_str, "anthropic.claude-3-opus-20240229-v1:0", 0)
        
        with open('claude_3_answer_incorrect_RD_questions_with_explanation.txt', 'w') as file:
            file.write(content + question_str + "\n" + response + "\n" + "-"*20 + "\n\n\n")
    '''
    
    # Asks all questions from the question set with certain answer format
    response_claude = ""
    # Prompt the questions in a batch of 1, you can adjust the question number in each batch
    for startIndex in range (1, len(question_dict) + 1, 1):
        prompt_str = qsql.get_prompt_string(question_dict, startIndex, 1)
        print(prompt_str)
        # Use the Claude 3 - Opus model and set temperature to 0. 
        # To use Claude 3 Haiku/Sonnet, use "anthropic.claude-3-haiku-20240307-v1:0" or "anthropic.claude-3-sonnet-20240229-v1:0"
        response_claude += api.ask_claude(prompt_str, "anthropic.claude-3-opus-20240229-v1:0", 0)
        response_claude += "\n"
        #print(response_claude)
    print(response_claude)
    
    score_claude = qsql.get_score(response_claude, question_dict)

    print("\n")
    print('Claude 3 Opus: ' + score_claude)
    
