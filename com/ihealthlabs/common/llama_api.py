from config import env
from questions_mysql import QuestionsMysql

import ollama

qsql = QuestionsMysql()
question_dict = qsql.get_questions()

response = ollama.chat(model='llama3', messages=[
  {
    'role': 'user',
    'content': qsql.get_prompt_string_llama(question_dict),
  },
])
responsellama = response['message']['content']
print(responsellama)
scorellama = qsql.get_score(responsellama, question_dict)
print("llama3: " + scorellama)

