import anthropic_bedrock_api
import questions_mysql
import time
from datetime import datetime

api = anthropic_bedrock_api.AnthropicBedRockAPI()
qsql = questions_mysql.QuestionsMysql()
# Connect to RD Exam Questions
question_dict = qsql.get_RD_questions()

prefix = str(datetime.now())

for i in range(8, 16):  
    file_name = f'{prefix}_claude_3.5_sonnet_sc_cot_exp{i}.txt'
    with open(file_name, 'w') as file:
        pass

    response4 = "\n"

    start = time.time()
    # Prompt the questions in a batch of 1, you can adjust the question number in each batch 
    for startIndex in range (1, len(question_dict) + 1, 1):
        
        with open(file_name, 'r') as file:
            content = file.read()

        prompt_str = qsql.get_cot_prompt_string(question_dict, startIndex, 1)
        print(prompt_str)
        response = api.ask_claude(prompt_str, "anthropic.claude-3-5-sonnet-20240620-v1:0", 0) 
        response4 += response
        response4 += "\n"

        with open(file_name, 'w') as file:
            file.write(content + prompt_str + "\n" + response + "\n\n\n")
    
    end = time.time()
    length = end - start
    print("Round", i, "took", length, "seconds.")


'''
score4 = qsql.get_score_xml(response4, question_dict)
print("\n")
print('claude 3.5 sonnet:' + score4)
'''