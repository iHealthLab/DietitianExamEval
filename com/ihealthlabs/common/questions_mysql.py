from collections import defaultdict

import sqlalchemy

from conn_mysql import ClientMysql


class QuestionsMysql:

    def __init__(self):
        self.mysql_client = ClientMysql()

    def get_questions(self):
        query = sqlalchemy.text('select * from question')
        data = self.mysql_client.execute(query)
        question_dict = defaultdict()
        rows = data.fetchall()
        for d in rows:
            question_dict[d[0]] = {
                'question_id': d[0],
                'question_number': d[1],
                'question': d[2],
                'choices': d[3],
                'answer': d[4],
                'test_id': d[5]
            }
        return question_dict

    def get_prompt_string(self, dictionary):
        prompt = "Answer the following multiple choice questions using the format of 1.x with no explanation: \n"
        count = 1
        for key, value in dictionary.items():
            prompt += str(count) + ". " + value['question'] + "\n" + value['choices'] + "\n"
            count += 1
        # print(prompt)
        return prompt

    def get_prompt_string_llama(self, dictionary):
        prompt = "Answer the following multiple choice questions using the format of <question_number>.<your choice> (for the choice you made, please include the letter only and no need to add space between question number and your choice) with no explanation, please only choose one answer for each question: \n"
        #count = 1
        for key, value in dictionary.items():
            prompt += str(value['question_number']) + ". " + value['question'] + "\n" + value['choices'] + "\n"
            #count += 1
        # print(prompt)
        return prompt

    def get_score(self, answer_string, question_dict):
        result_string = "1." + answer_string.split('1.', 1)[-1]
        choices = self.extract_choices(result_string)
        correct = 0
        wrong_questions = []
        i = 0
        for key, value in question_dict.items():
            if value['answer'] == choices[i]:
                correct += 1
            else: 
                wrong_questions.append(i+1)
            i += 1
        size = len(question_dict)
        print(wrong_questions)
        return str(correct / size * 100) + "%"

    def extract_choices(self, choice_string):
        # Split the string into parts on spaces
        parts = choice_string.split()
        choices = [part[-1] for part in parts]
        return choices


if __name__ == '__main__':
    qsql = QuestionsMysql()
