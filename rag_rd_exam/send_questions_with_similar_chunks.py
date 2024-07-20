
import pandas as pd
import sys
sys.path.append('/ai-benchmark/com/ihealthlabs/common')
import openai_api

from questions_mysql import QuestionsMysql

    
qsql = QuestionsMysql()
# Connect to RD Exam Questions
question_dict = qsql.get_RD_questions()

api = openai_api.OpenAIAPI()

# Load knowledge dataframe (chunks)
FILE_PATH = '/ai-benchmark/rag_rd_exam/extracted_string.csv'
df = pd.read_csv(FILE_PATH)
similar_chunks_list = []
for index, row in df.iterrows():
    #question_id = row['question_id']
    similar_chunks_list.append(row['top_10_similar_chunks'])

with open('gpt_4o_rag_testrun_cot.txt', 'w') as file:
    pass

response = "\n"
for startIndex in range (1, len(question_dict) + 1, 1):
    selected_chunk_str = similar_chunks_list[startIndex - 1]

    with open('gpt_4o_rag_testrun_cot.txt', 'r') as file:
        content = file.read()

    prompt_str = qsql.get_rag_cot_prompt_string(question_dict, startIndex, 1, selected_chunk_str)
    print("Prompt: \n" + prompt_str)

    response = api.ask_chatgpt(prompt_str, "gpt-4o", 0)
    response += "\n"

    with open('gpt_4o_rag_testrun_cot.txt', 'w') as file:
        file.write(content + prompt_str + "\n" + response + "\n\n\n")






