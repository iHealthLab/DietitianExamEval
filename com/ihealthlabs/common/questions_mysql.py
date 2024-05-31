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

    def get_prompt_string_llama(self, dictionary):
        prompt = "Answer the following multiple choice questions using the format of <question_number>.<your choice> (for the choice you made, please include the letter only and no need to add space between question number and your choice) with no explanation, please only choose one answer for each question: \n"
        #count = 1
        for key, value in dictionary.items():
            prompt += str(value['question_id']) + ". " + value['question'] + "\n" + value['choices'] + "\n"
            #count += 1
        # print(prompt)
        return prompt

    def get_score(self, answer_string, question_dict):
        result_string = "1." + answer_string.split('1.', 1)[-1]
        print(result_string)
        choices = self.extract_choices(result_string)
        print(len(choices))
        correct = 0
        wrong_questions = {}
        i = 0
        for key, value in question_dict.items():
            if value['answer'] == choices[i]:
                correct += 1
            else: 
                wrong_questions[i+1] = choices[i]
            i += 1
        size = len(question_dict)
        print("Wrong questions: \n")
        for key, value in wrong_questions.items():
            print("{0}: {1}".format(key, value))
        return str(correct / size * 100) + "%"

    '''
    def extract_choices(self, choice_string):
        choices = []
        lines = choice_string.split('\n')
        for line in lines:
            line = line.strip()
            match = re.search(r'^\d+\.\s*([A-D])', line)
            if match:
                choices.append(match.group(1).lower())  # Convert to lowercase for consistency
        return choices
    '''

    def extract_choices(self, choice_string):
        # Extract lines and then the choices
        lines = choice_string.strip().split('\n')
        choices = [line.split('.')[1].strip() for line in lines]
        return choices
    
    '''
    def extract_choices(self, choice_string):
        # Split the string into parts on spaces
        parts = choice_string.split()
        choices = [part[-1] for part in parts]
        return choices
    '''

if __name__ == '__main__':
    qsql = QuestionsMysql()
    '''
    with open('gpt_answer_RD_questions.txt', 'r') as file:
        choice_string = file.readlines()
    print(choice_string)
    print(qsql.extract_choices(choice_string))
    print(len(qsql.extract_choices(choice_string)))
    '''
   