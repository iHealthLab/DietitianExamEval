'''
from config import env
from questions_mysql import QuestionsMysql

import asyncio
from anthropic import AsyncAnthropic


qsql = QuestionsMysql()
question_dict = qsql.get_questions()

# Connect to Anthropic Claude API
client = AsyncAnthropic(api_key=env.str("ANTHROPIC_API_KEY"),)

async def main() -> None:
    async with client.messages.stream(
        max_tokens=1024,
        messages=[{"role": "user", "content": qsql.get_prompt_string(question_dict)}],
        # messages=[{"role": "user", "content": "Why sky is blue?"}],
        model="claude-3-opus-20240229",
        # stream=True,
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)
        print()
    # print(message.content)
    res = await stream.get_final_text()

    scoreClaude = qsql.get_score(res, question_dict)
    print("Claude 3 Opus: " + scoreClaude)

asyncio.run(main())
'''


import asyncio
from anthropic import AsyncAnthropic
from anthropic import Anthropic

from config import env
from questions_mysql import QuestionsMysql


class AnthropicAPI(object):

    def __init__(self):
        #self.client = AsyncAnthropic(api_key=env.str("ANTHROPIC_API_KEY"),)
        self.client = Anthropic(api_key=env.str("ANTHROPIC_API_KEY"),)


    def ask_claude(self, question, model_str) :
        res = ""
        with self.client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": question}],
            model=model_str,
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                res += text
        return res
        

    
    '''
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
    '''

if __name__ == '__main__':
    api = AnthropicAPI()
    qsql = QuestionsMysql()
    question_dict = qsql.get_questions()
    response_claude = ""
    #for startIndex in range (1, 160 + 1, 10):
    for startIndex in range (1, len(question_dict) + 1, 10):
        prompt_str = qsql.get_prompt_string(question_dict, startIndex, 10)
        #print(prompt_str)
        #response_claude += asyncio.run(api.ask_claude(prompt_str, "claude-3-opus-20240229"))
        response_claude += api.ask_claude(prompt_str, "claude-3-opus-20240229")
        response_claude += "\n"
        #print(response_claude)

    #prompt_str = qsql.get_prompt_string(question_dict)

    #response_claude = asyncio.run(api.ask_claude(prompt_str, "claude-3-opus-20240229"))

    score_claude = qsql.get_score(response_claude, question_dict)

    print("\n")
    print('Claude 3 Opus: ' + score_claude)
