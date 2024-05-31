import google.generativeai as genai
import os

from config import env
from questions_mysql import QuestionsMysql


class GeminiAIAPI(object):

    def __init__(self):
        self._client = genai.configure(api_key=env.str("GEMINI_API_KEY"))

    def ask_gemini(self, question, model_str):
        res = ""
        model = genai.GenerativeModel(model_str)
        response = model.generate_content(question)
        print(response.text)
        '''
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")
                res += chunk.choices[0].delta.content
        return res
        '''


if __name__ == '__main__':
    api = GeminiAIAPI()
    qsql = QuestionsMysql()
    question_dict = qsql.get_questions()
    prompt_str = "Write a story about a magic backpack."
    response = api.ask_gemini(prompt_str, 'gemini-1.5-flash')
    '''
    response4 = "\n"
    # Prompt the questions in a batch of 20 
    for startIndex in range (1, len(question_dict) + 1, 20):
        prompt_str = qsql.get_prompt_string(question_dict, startIndex, 20)
        response4 += api.ask_chatgpt(prompt_str, "gpt-4")
        response4 += "\n"
   
    #response35 = api.ask_chatgpt(prompt_str, "gpt-3.5-turbo")
    score4 = qsql.get_score(response4, question_dict)
    #score35 = qsql.get_score(response35, question_dict)
    print("\n")
    print('gpt4 :' + score4)
    #print('gpt3.5 :' + score35)
    '''