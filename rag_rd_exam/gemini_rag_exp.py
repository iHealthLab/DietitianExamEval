import pandas as pd
import sys
sys.path.append('/ai-benchmark/com/ihealthlabs/common')
import gemini_api
import time

from questions_mysql import QuestionsMysql

    
qsql = QuestionsMysql()
# Connect to RD Exam Questions
question_dict = qsql.get_RD_questions()

api = gemini_api.GeminiAIAPI()

# Get the extracted similar chunks
FILE_PATH = '/ai-benchmark/rag_rd_exam/extracted_string_10_and_3.csv'
df = pd.read_csv(FILE_PATH)
similar_chunks_list = []
for index, row in df.iterrows():
    #question_id = row['question_id']
    similar_chunks_list.append(row['top_3_similar_chunks'])

for i in range(2, 6):  
    file_name = f'gemini_1.5_pro_rag_top_3_exp{i}.txt'
    with open(file_name, 'w') as file:
        pass

    start = time.time()
    response = "\n"
    for startIndex in range (1, len(question_dict) + 1, 1):
        selected_chunk_str = similar_chunks_list[startIndex - 1]

        with open(file_name, 'r') as file:
            content = file.read()

        prompt_str = qsql.get_rag_prompt_string(question_dict, startIndex, 1, selected_chunk_str)

        response = api.ask_gemini(prompt_str, 'gemini-1.5-pro', 0) 
        response += "\n"

        with open(file_name, 'w') as file:
            file.write(content + prompt_str + "\n" + response + "\n\n\n")
        
    end = time.time()
    length = end - start
    print("Round", i, "took", length, "seconds.")






