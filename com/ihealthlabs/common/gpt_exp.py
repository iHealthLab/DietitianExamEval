import openai_api
import questions_mysql
import time

api = openai_api.OpenAIAPI()
qsql = questions_mysql.QuestionsMysql()
# Connect to RD Exam Questions
question_dict = qsql.get_RD_questions()

for i in range(1, 3):  
    file_name = f'gpt_4o_self_consistency_exp{i}.txt'
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
        # Use the GPT 4o model and set temperature to 0. To use GPT 3.5 ot GPT 4 model, change the "gpt-4o" to "gpt-4 or gpt-3.5"
        response = api.ask_chatgpt(prompt_str, "gpt-4o", 0) 
        response4 += response
        response4 += "\n"

        with open(file_name, 'w') as file:
            file.write(content + prompt_str + "\n" + response + "\n\n\n")
    end = time.time()
    length = end - start
    print("Round", i, "took", length, "seconds.")
'''
# Add the answer list to the txt file
with open('gpt_4o_zero_shot_exp5.txt', 'r') as file:
        content = file.read()

with open('gpt_4o_zero_shot_exp5.txt', 'w') as file:
    file.write(content + "Answer List: \n" + qsql.get_answer_xml(response4) + "\n" + qsql.get_score_xml(response4, question_dict))

# Get the score
score4 = qsql.get_score_xml(response4, question_dict)
print("\n")
print('gpt4o:' + score4)
'''
