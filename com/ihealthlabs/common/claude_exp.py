import anthropic_bedrock_api
import questions_mysql

api = anthropic_bedrock_api.AnthropicBedRockAPI()
qsql = questions_mysql.QuestionsMysql()
# Connect to RD Exam Questions
question_dict = qsql.get_RD_questions()

response4 = "\n"

# Prompt the questions in a batch of 1, you can adjust the question number in each batch 
for startIndex in range (280, len(question_dict) + 1, 1):
     
    with open('claude_3.5_sonnet_cot_exp2.txt', 'r') as file:
        content = file.read()

    prompt_str = qsql.get_cot_prompt_string(question_dict, startIndex, 1)
    print(prompt_str)
    # Use the GPT 4o model and set temperature to 0. To use GPT 3.5 ot GPT 4 model, change the "gpt-4o" to "gpt-4 or gpt-3.5"
    response = api.ask_claude(prompt_str, "anthropic.claude-3-5-sonnet-20240620-v1:0", 0) 
    response4 += response
    response4 += "\n"

    with open('claude_3.5_sonnet_cot_exp2.txt', 'w') as file:
        file.write(content + prompt_str + "\n" + response + "\n\n\n")
'''
with open('claude_3.5_sonnet_zero_shot_exp5.txt', 'r') as file:
        content = file.read()

with open('claude_3.5_sonnet_zero_shot_exp5.txt', 'w') as file:
    file.write(content + "Answer List: \n" + qsql.get_answer_xml(response4) + "\n" + qsql.get_score_xml(response4, question_dict))
'''

score4 = qsql.get_score_xml(response4, question_dict)
print("\n")
print('claude 3.5 sonnet:' + score4)