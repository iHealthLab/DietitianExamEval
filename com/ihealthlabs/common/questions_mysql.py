from collections import defaultdict
import re

import sqlalchemy

from conn_mysql import ClientMysql


class QuestionsMysql:

    def __init__(self):
        self.mysql_client = ClientMysql()

    def get_questions(self):
        query = sqlalchemy.text('select * from RDQuestions')
        data = self.mysql_client.execute(query)
        question_dict = defaultdict()
        rows = data.fetchall()
        for d in rows:
            question_dict[d[0]] = {
                'question_id': d[0],
                'question': d[1],
                'choices': d[2],
                'answer': d[3]
            }
        return question_dict

    # Get prompt in a batch of 20 questions
    def get_prompt_string(self, dictionary, startIndex, batch_size):
        #prompt = "Answer the following multiple choice questions using the format of 1.x with no explanation: \n"
        prompt = "Answer the following multiple choice questions using the format of <question_number>.<your choice> with no explanation and your choice will be letter only (for example: 1.a or 2.B, no space between question number and your choice): \n"
        for i in range(startIndex, startIndex + batch_size):
            #if(i > 160):
            if(i > len(dictionary)):
                return prompt
            question = dictionary[i]
            prompt += str(question['question_id']) + ". " + question['question'] + "\n" + question['choices'] + "\n"
        '''
        for key, value in dictionary.items():
            prompt += str(value['question_id']) + ". " + value['question'] + "\n" + value['choices'] + "\n"
        '''
        return prompt
    

    def get_prompt_string_llama(self, dictionary, startIndex, batch_size):
        prompt = "Answer the following multiple choice questions using the format of <question_number>.<your_choice>, where `<your_choice>` is a letter (A, B, C, or D) and nothing else. No space between question number and your choice. Please skip the preamble, go straight to the answers: "
        for i in range(startIndex, startIndex + batch_size):
            if(i > len(dictionary)):
                return prompt
            question = dictionary[i]
            prompt += str(question['question_id']) + ". " + question['question'] + " " + question['choices'] + " "
        #prompt += "Please respond to each question with a single letter (a, b, c, or d) indicating your choice."
        return prompt



    def get_score(self, answer_string, question_dict):
        result_string = "1." + answer_string.split('1.', 1)[-1]

        '''
        # For llama only, to skip the premables
        pattern = r'\d+\.\s*[a-dA-D]'
        matches = re.findall(pattern, result_string)
        formatted_answers = '\n'.join(matches)
        print(formatted_answers)
        choices = self.extract_choices(formatted_answers)
        '''

        choices = self.extract_choices(result_string)
        print(len(choices))
        correct = 0
        wrong_questions = {}
        i = 0
        for key, value in question_dict.items():
            if value['answer'] == choices[i] or value['answer'] == choices[i].upper():
                correct += 1
            else: 
                wrong_questions[i+1] = choices[i]
            i += 1
        size = len(question_dict)
        print("Wrong questions: \n")
        for key, value in wrong_questions.items():
            print("{0}: {1}".format(key, value))
        return str(correct / size * 100) + "%"

   
    def extract_choices(self, choice_string):
        # Extract lines and then the choices
        print("choice_string: " + choice_string)
        lines = choice_string.strip().split('\n')
        print(lines)
        choices = [line.split('.')[1].strip() for line in lines]
        return choices
    

if __name__ == '__main__':
    qsql = QuestionsMysql()
    '''
    question_dict = qsql.get_questions()
    with open('gpt_answer_RD_questions_llama.txt', 'r') as file:
        choice_string = file.readlines()
    print(choice_string)
    correct = 0
    wrong_questions = {}
    i = 0
    for key, value in question_dict.items():
        if value['answer'] == choice_string[i] or value['answer'] == choice_string[i].upper():
            correct += 1
        else: 
            wrong_questions[i+1] = choice_string[i]
        i += 1
    size = len(question_dict)
    print("Wrong questions: \n")
    for key, value in wrong_questions.items():
        print("{0}: {1}".format(key, value))
    print(str(correct / size * 100) + "%")

    #print(qsql.extract_choices(choice_string))
    #print(len(qsql.extract_choices(choice_string)))
    '''

   