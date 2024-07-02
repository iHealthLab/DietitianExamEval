from anthropic import Anthropic

from config import env
from questions_mysql import QuestionsMysql

class AnthropicAPI(object):
    """
    This class connects to Anthropic API directly.
    """

    def __init__(self):
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
        

if __name__ == '__main__':
    api = AnthropicAPI()
    qsql = QuestionsMysql()
    question_dict = qsql.get_questions()
    response_claude = ""

    # Prompt the questions in a batch of 10 
    for startIndex in range (1, len(question_dict) + 1, 10):
        prompt_str = qsql.get_prompt_string(question_dict, startIndex, 10)
        #print(prompt_str)
        response_claude += api.ask_claude(prompt_str, "claude-3-opus-20240229")
        response_claude += "\n"
        #print(response_claude)

    score_claude = qsql.get_score(response_claude, question_dict)

    print("\n")
    print('Claude 3 Opus: ' + score_claude)
