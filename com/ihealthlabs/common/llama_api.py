from config import env
from questions_mysql import QuestionsMysql

import ollama

qsql = QuestionsMysql()
question_dict = qsql.get_questions()

# Connect to ollama
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

'''
# calling llama api
import json
from llamaapi import LlamaAPI

# Initialize the SDK
llama = LlamaAPI(env.str("LLAMA_API_KEY"))

# Build the API request
api_request_json = {
    "messages": [
        {"role": "user", "content": qsql.get_prompt_string_llama(question_dict)},
    ],
    "stream": False,
}

# Execute the Request
response = llama.run(api_request_json)
print(json.dumps(response.json(), indent=2))
'''
