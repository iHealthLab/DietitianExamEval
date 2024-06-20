import time
import openai
from openai import OpenAI

from config import env
from questions_mysql import QuestionsMysql


class OpenAIAPI(object):
    """
    This class connects to OpenAI API.
    """

    def __init__(self):
        openai.api_key = env.str("OPENAI_API_KEY")

    def ask_chatgpt(self, question, model_str, temp):
        res = ""
        client = OpenAI(api_key = env.str("OPENAI_API_KEY"))
        stream = client.chat.completions.create(
            model=model_str,
            messages=[{"role": "user", "content": question}],
            stream=True,
            temperature=temp,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")
                res += chunk.choices[0].delta.content
        return res


if __name__ == '__main__':
    api = OpenAIAPI()
    qsql = QuestionsMysql()
    # Connect to RD Exam Questions
    question_dict = qsql.get_RD_questions()
    # Connect to CDCES Exam Questions
    # question_dict = qsql.get_questions()

    # Asks the incorrect questions with choices only, allowing explanation and no restriction in answer format
    '''
    prompt_str = ""
    question_list = [369, 776, 10, 244, 275, 298, 361, 485, 864, 1006, 324, 162, 249, 291, 299, 379, 474, 720, 822, 976, 1043]
    for i in question_list:
        question = question_dict[i]
        
        with open('gpt_4o_answer_incorrect_RD_questions_with_explanation_inconsistent.txt', 'r') as file:
            content = file.read()

        prompt_str = question['question'] + "\n" + question['choices']
        question_str = str(question['question_id']) + ". " + prompt_str + "\n\nDifficulty Level: " + question['difficulty_level'] + "\n\nCorrect Answer: " + question['answer'] + "\n\nExplanation: " + question['explanation'] + "\n\nReferences: " + question['answer_references'] + "\n\nGPT Response: \n"
        response = api.ask_chatgpt(prompt_str, "gpt-4o", 0)
        with open('gpt_4o_answer_incorrect_RD_questions_with_explanation_inconsistent.txt', 'w') as file:
            file.write(content + question_str + "\n" + response + "\n\n\n")
    '''

    # Asks all questions from the question set with certain answer format
    response4 = "\n"
    # Prompt the questions in a batch of 1, you can adjust the question number in each batch 
    for startIndex in range (1, len(question_dict) + 1, 1):
        prompt_str = qsql.get_prompt_string(question_dict, startIndex, 1)
        print(prompt_str)
        # Use the GPT 4o model and set temperature to 0. To use GPT 3.5 ot GPT 4 model, change the "gpt-4o" to "gpt-4 or gpt-3.5"
        response4 += api.ask_chatgpt(prompt_str, "gpt-4o", 0)
        response4 += "\n"
        #time.sleep(2)

    # Save the LLM response to a txt file
    '''
    with open('gpt_answer_CDCES_questions.txt', 'w') as file:
        file.write(response4 + "\n")
    '''

    score4 = qsql.get_score(response4, question_dict)
    print("\n")
    print('gpt4o:' + score4)
