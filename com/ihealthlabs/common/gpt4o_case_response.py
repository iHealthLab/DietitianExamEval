import openai_api
import questions_mysql

api = openai_api.OpenAIAPI()
qsql = questions_mysql.QuestionsMysql()
# Connect to patient cases
case_dict = qsql.get_patient_cases()

response4 = "\n"

# Prompt the cases in a batch of 1, you can adjust the number in each batch 
for startIndex in range (6, len(case_dict) + 1, 1):

    with open('gpt_4o_pt_cases_response.txt', 'r') as file:
        content = file.read()

    prompt_str = qsql.get_pt_case_prompt_string(case_dict, startIndex, 1)
    print(prompt_str)
    # Use the GPT 4o model and set temperature to 0. To use GPT 3.5 ot GPT 4 model, change the "gpt-4o" to "gpt-4 or gpt-3.5"
    response = api.ask_chatgpt(prompt_str, "gpt-4o", 0) 
    response4 += response
    response4 += "\n"

    with open('gpt_4o_pt_cases_response.txt', 'w') as file:
        file.write(content + prompt_str + "\n\nGPT4o Response: \n" + response + "\n" + "==" * 30 + "\n")


