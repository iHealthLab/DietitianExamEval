import openai
from openai import OpenAI
import ollama
import asyncio
from anthropic import AsyncAnthropic

from config import env
from questions_mysql import QuestionsMysql



class ChatAPI(object):

    def __init__(self):
        openai.api_key = env.str("OPENAI_API_KEY")
        self.client = AsyncAnthropic(api_key=env.str("ANTHROPIC_API_KEY"),)

    def ask_gpt(self, question, model_str):
        res = ""
        client = OpenAI(api_key = env.str("OPENAI_API_KEY"))
        stream = client.chat.completions.create(
            model=model_str,
            messages=[{"role": "user", "content": question}],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")
                res += chunk.choices[0].delta.content
        return res
    
    
    async def ask_claude(self, question, model_str) :
        async with self.client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": question}],
            model=model_str,
        ) as stream:
            async for text in stream.text_stream:
                print(text, end="", flush=True)
            print()
        res = await stream.get_final_text()
        return res


if __name__ == '__main__':
    qsql = QuestionsMysql()
    question_dict = qsql.get_questions()
    prompt_str = qsql.get_prompt_string(question_dict)
    prompt_str_llama = qsql.get_prompt_string_llama(question_dict)

    api = ChatAPI()
    response_gpt4 = api.ask_gpt(prompt_str, "gpt-4")
    response_claude = asyncio.run(api.ask_claude(prompt_str, "claude-3-opus-20240229"))
    responsellama = ollama.chat(model='llama3', messages=[
      {
        'role': 'user',
        'content': prompt_str_llama,
      },
    ])
    response_llama = responsellama['message']['content']

    print(response_llama)

    score_gpt4 = qsql.get_score(response_gpt4, question_dict)
    score_claude = qsql.get_score(response_claude, question_dict)
    score_llama = qsql.get_score(response_llama, question_dict)

    print("\n")
    print('GPT 4: ' + score_gpt4)
    print('Claude 3 Opus: ' + score_claude)
    print('Llama 3: ' + score_llama)
