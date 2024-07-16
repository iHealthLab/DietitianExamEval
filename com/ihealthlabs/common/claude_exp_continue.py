import anthropic_bedrock_api
import questions_mysql

api = anthropic_bedrock_api.AnthropicBedRockAPI()
qsql = questions_mysql.QuestionsMysql()
# Connect to RD Exam Questions
question_dict = qsql.get_RD_questions()

response4 = "\n"


# Prompt the questions in a batch of 1, you can adjust the question number in each batch 
for startIndex in range (961, len(question_dict) + 1, 1):
    
    with open('claude_3.5_sonnet_sc_cot_exp7.txt', 'r') as file:
        content = file.read()

    prompt_str = qsql.get_cot_prompt_string(question_dict, startIndex, 1)
    print(prompt_str)
    response = api.ask_claude(prompt_str, "anthropic.claude-3-5-sonnet-20240620-v1:0", 0) 
    response4 += response
    response4 += "\n"

    with open('claude_3.5_sonnet_sc_cot_exp7.txt', 'w') as file:
        file.write(content + prompt_str + "\n" + response + "\n\n\n")



