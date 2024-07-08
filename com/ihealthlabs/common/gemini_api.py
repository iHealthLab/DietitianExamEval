import google.generativeai as genai

from config import env
from questions_mysql import QuestionsMysql
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type


class GeminiAIAPI(object):
    """
    This class connects to Gemini API directly.
    """

    def __init__(self):
        self._client = genai.configure(api_key=env.str("GEMINI_API_KEY"))
    
    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=10),
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type(ValueError)
    )
    def ask_gemini(self, question, model_str, temp):
        res = ""
        model = genai.GenerativeModel(model_str)
        safety_settings = [
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
        ]
        response = model.generate_content(question, generation_config=genai.types.GenerationConfig(temperature=temp), safety_settings=safety_settings)
        #print(response.text)

        for chunk in response:
            print(chunk.text)
            res += chunk.text
        return res

if __name__ == '__main__':
    api = GeminiAIAPI()
    qsql = QuestionsMysql()
    # Connect to RD Exam Questions
    question_dict = qsql.get_RD_questions()
    # Connect to CDCES Exam Questions
    # question_dict = qsql.get_questions()

    # Asks the incorrect questions with choices only, allowing explanation and no restriction in answer format
    '''
    prompt_str = ""
    question_list = [139, 245, 930, 447]
    for i in question_list:
        question = question_dict[i]
        
        with open('gemini_1.5Pro_answer_incorrect_RD_questions_with_explanation.txt', 'r') as file:
            content = file.read()

        prompt_str = question['question'] + "\n" + question['choices']
        question_str = str(question['question_id']) + ". " + prompt_str + "\n\nDifficulty Level: " + question['difficulty_level'] + "\n\nCorrect Answer: " + question['answer'] + "\n\nExplanation: " + question['explanation'] + "\n\nReferences: " + question['answer_references'] + "\n\nGemini 1.5 Pro Response: \n"
        response = api.ask_gemini(prompt_str, 'gemini-1.5-pro', 0)
        with open('gemini_1.5Pro_answer_incorrect_RD_questions_with_explanation.txt', 'w') as file:
            file.write(content + question_str + "\n" + response + "\n" + "-"*100 + "\n\n\n")

    '''

    # Asks all questions from the question set with certain answer format
    response = "\n"
    # Prompt the questions in a batch of 1, you can adjust the question number in each batch 
    for startIndex in range (1, len(question_dict) + 1, 1):
        prompt_str = qsql.get_prompt_string(question_dict, startIndex,  1)
        # Use the Gemini 1.5 Pro model and set temperature to 0.
        response += api.ask_gemini(prompt_str, 'gemini-1.5-pro', 0)

   
    score = qsql.get_score(response, question_dict)
    print("\n")
    print('Gemini 1.5 Pro :' + score)
    
