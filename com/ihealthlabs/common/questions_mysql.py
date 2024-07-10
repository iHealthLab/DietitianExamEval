from collections import defaultdict

import sqlalchemy
import re

from conn_mysql import ClientMysql


class QuestionsMysql:

    def __init__(self):
        self.mysql_client = ClientMysql()

    # Get CDCES Questions from the database
    def get_questions(self):
        query = sqlalchemy.text('select * from CDCESQuestions')
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
    
    # Get the 20 test questions from the database
    def get_test_questions(self):
        query = sqlalchemy.text('select * from test')
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
    
    # Get the RD questions from the database
    def get_RD_questions(self):
        query = sqlalchemy.text('select * from RDQuestions')
        data = self.mysql_client.execute(query)
        question_dict = defaultdict()
        rows = data.fetchall()
        for d in rows:
            question_dict[d[0]] = {
                'question_id': d[0],
                'question': d[1],
                'choices': d[2],
                'answer': d[3],
                'explanation': d[4],
                'difficulty_level': d[5],
                'answer_references': d[6]
            }
        return question_dict
    
    # Get the patient cases from the database
    def get_patient_cases(self):
        query = sqlalchemy.text('select * from patientcases')
        data = self.mysql_client.execute(query)
        case_dict = defaultdict()
        rows = data.fetchall()
        for d in rows:
            case_dict[d[0]] = {
                'case_number': d[0],
                'case_id': d[1],
                'patient_info_assessment': d[2],
                'plan': d[3]
            }
        return case_dict

    # Get prompt in a batch of questions
    def get_prompt_string(self, dictionary, startIndex, batch_size):
        #prompt = "Answer the following multiple choice questions using the format of 1.x with no explanation: \n"
        #prompt = "Instructions: Solve the following multiple choice question in a step-by-step fashion. Output a single option from as the final answer and enclosed by xml tags <questionNumber></questionNumber><answer></answer>. \n"
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
    

    # Get no explanation prompt in a batch of questions
    def get_no_explain_prompt_string(self, dictionary, startIndex, batch_size):
        prompt = "Instructions: Solve the following multiple choice question with no explanation. Output a single option as the final answer and enclosed by xml tags <answer></answer> \n"
        for i in range(startIndex, startIndex + batch_size):
            if(i > len(dictionary)):
                return prompt
            question = dictionary[i]
            prompt += str(question['question_id']) + ". " + question['question'] + "\n" + question['choices'] + "\n"
        return prompt
    

    # Get CoT prompt in a batch of questions
    def get_cot_prompt_string(self, dictionary, startIndex, batch_size):
        prompt = "Instructions: Solve the following multiple choice question in a step-by-step fashion, starting by summarizing the available information. Output a single option as the final answer and enclosed by xml tags <answer></answer> \n"
        for i in range(startIndex, startIndex + batch_size):
            if(i > len(dictionary)):
                return prompt
            question = dictionary[i]
            prompt += str(question['question_id']) + ". " + question['question'] + "\n" + question['choices'] + "\n"
        return prompt
    
    # Get CoT prompt in a batch of questions
    def get_pt_case_prompt_string(self, dictionary, startIndex, batch_size):
        prompt = "Imaging you are a registered dietitian who sees patient for nutrition counseling sessions and remotely monitoring the patient's blood glucose management. Your job is to come up with a treatment plan to address the high A1C status for the patient based on the subjective information, objective information, and the assessment provided. \n\nHere are a few examples of the patient cases with subjective information, objective information, assessment and the treatment plan: \nExample 1:"
        prompt += dictionary[1]['patient_info_assessment'] + "\n\n" + dictionary[1]['plan'] + "\n\nExample 2: \n"
        prompt += dictionary[2]['patient_info_assessment'] + "\n\n" + dictionary[2]['plan'] + "\n\nExample 3: \n"
        prompt += dictionary[3]['patient_info_assessment'] + "\n\n" + dictionary[3]['plan'] + "\n\nExample 4: \n"
        prompt += dictionary[4]['patient_info_assessment'] + "\n\n" + dictionary[4]['plan'] + "\n\nExample 5: \n"
        prompt += dictionary[5]['patient_info_assessment'] + "\n\n" + dictionary[5]['plan'] + "\n\nHere is the the patient case you need to work on to generate the treatment plan: \n"
        for i in range(startIndex, startIndex + batch_size):
            if(i > len(dictionary)):
                return prompt
            question = dictionary[i]
            prompt += "Case " + str(question['case_number']) + ": \n" + question['patient_info_assessment'] + "\n"
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
    
    def get_score_xml(self, answer_string, question_dict):
        pattern = r"<answer>([a-dA-D]|NaN)(?:\.[^<]*)?</answer>"
    
        # Find all matches in the text
        matches = re.findall(pattern, answer_string)
        
        # Format the matches as required (question number and answer concatenated with a dot)
        choices = ["{}".format(answer) for answer in matches]
        #print(choices)
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
    
    # Get the answer list from the LLM's response by finding the xml tag pattern
    def get_answer_xml(self, answer_string):
        pattern = r"<answer>([a-dA-D]|NaN)(?:\.[^<]*)?</answer>"
    
        # Find all matches in the text
        matches = re.findall(pattern, answer_string)
        choices = ["{}".format(answer) for answer in matches]
        
        for choice in choices:
            print(choice)
        print(len(choices))
        
        #result = '\n'.join(choices)
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

   