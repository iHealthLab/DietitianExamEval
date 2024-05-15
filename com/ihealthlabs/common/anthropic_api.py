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