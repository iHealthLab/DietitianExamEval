import gemini_api
import questions_mysql

api = gemini_api.GeminiAIAPI()
qsql = questions_mysql.QuestionsMysql()
# Connect to patient cases
case_dict = qsql.get_patient_cases()

response4 = "\n"

# Prompt the cases in a batch of 1, you can adjust the number in each batch 
for startIndex in range (8, len(case_dict) + 1, 1):
    with open('gemini_1.5_pro_pt_cases_response.txt', 'r') as file:
        content = file.read()

    prompt_str = qsql.get_pt_case_prompt_string(case_dict, startIndex, 1)
    print(prompt_str)
    response = api.ask_gemini(prompt_str, "gemini-1.5-pro", 0) 
    response4 += response
    response4 += "\n"

    with open('gemini_1.5_pro_pt_cases_response.txt', 'w') as file:
        file.write(content + prompt_str + "\n\nGemini 1.5 Pro Response: \n" + response + "\n" + "==" * 30 + "\n")

