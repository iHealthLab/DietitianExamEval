import openai
from openai import OpenAI

from ihealthlabs.common.config import env
from ihealthlabs.common.questions_mysql import QuestionsMysql


class OpenAIAPI(object):

    def __init__(self):
        openai.api_key = env.str("OPENAI_API_KEY")

    def ask_chatgpt(self, question):
        res = ""
        client = OpenAI()
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")
                res += chunk.choices[0].delta.content
        return res


if __name__ == '__main__':
    api = OpenAIAPI()
    qsql = QuestionsMysql()
    question_dict = qsql.get_questions()
    prompt_str = qsql.get_prompt_string(question_dict)
    response = api.ask_chatgpt(prompt_str)
    print(response)
    score = qsql.get_score(response, question_dict)
    print(score)
