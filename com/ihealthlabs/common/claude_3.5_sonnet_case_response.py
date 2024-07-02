import anthropic_bedrock_api
import questions_mysql

api = anthropic_bedrock_api.AnthropicBedRockAPI()
qsql = questions_mysql.QuestionsMysql()
# Connect to patient cases
case_dict = qsql.get_patient_cases()

response4 = "\n"

# Prompt the cases in a batch of 1, you can adjust the number in each batch 
for startIndex in range (6, len(case_dict) + 1, 1):
    with open('claude_3.5_sonnet_pt_cases_response.txt', 'r') as file:
        content = file.read()

    prompt_str = qsql.get_pt_case_prompt_string(case_dict, startIndex, 1)
    print(prompt_str)
    response = api.ask_claude(prompt_str, "anthropic.claude-3-5-sonnet-20240620-v1:0", 0) 
    response4 += response
    response4 += "\n"

    with open('claude_3.5_sonnet_pt_cases_response.txt', 'w') as file:
        file.write(content + prompt_str + "\n\nClaude 3.5 Sonnet Response: \n" + response + "\n" + "==" * 30 + "\n")

