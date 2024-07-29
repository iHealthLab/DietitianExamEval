"""
Gets questions from the database and combines with different prompt instructions
to form the final prompt.
"""
from collections import defaultdict

import re
import sqlalchemy

from conn_mysql import ClientMysql


class QuestionsMysql:
    """
    This class can connect to the database to get the questions and
    add different prompt instructions to form different prompt for LLMs.
    """
    def __init__(self):
        """
        Initializes the QuestionsMysql class and sets up the MySQL client.
        """
        self.mysql_client = ClientMysql()

    # Get the RD questions from the database
    def get_rd_questions(self):
        """
        Retrieves RD questions from the database and returns them in a dictionary format.

        Returns:
            dict: A dictionary where each key is a question ID and the value is another dictionary
            containing question details including the question, choices, answer, explanation, 
            difficulty level, and answer references.
        """
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

    def get_no_explain_prompt_string(self, dictionary, start_index, batch_size):
        """
        Generates a prompt string for multiple choice questions with zero-shot prompt.

        Parameters:
            dictionary (dict): A dictionary containing the questions.
            startIndex (int): The index to start from in the dictionary.
            batch_size (int): The number of questions to include in the batch.

        Returns:
            str: A prompt string for the specified batch of questions.
        """
        prompt = "Instructions: Solve the following multiple choice question with no explanation. " \
                 "Output a single option as the final answer and enclosed " \
                 "by xml tags <answer></answer> \n"
        for i in range(start_index, start_index + batch_size):
            if i > len(dictionary):
                return prompt
            question = dictionary[i]
            prompt += str(question['question_id']) + ". " + question['question'] + "\n" + question['choices'] + "\n"
        return prompt


    def get_cot_prompt_string(self, dictionary, start_index, batch_size):
        """
        Generates a prompt string for multiple choice questions with a chain-of-thoughts prompt.

        Parameters:
            dictionary (dict): A dictionary containing the questions.
            startIndex (int): The index to start from in the dictionary.
            batch_size (int): The number of questions to include in the batch.

        Returns:
            str: A prompt string for the specified batch of questions.
        """
        prompt = "Instructions: Solve the following multiple choice question in a step-by-step fashion, " \
                 "starting by summarizing the available information. " \
                 "Output a single option as the final answer and enclosed by xml tags <answer></answer> \n"
        for i in range(start_index, start_index + batch_size):
            if i > len(dictionary):
                return prompt
            question = dictionary[i]
            prompt += str(question['question_id']) + ". " + question['question'] + "\n" + question['choices'] + "\n"
        return prompt


    def get_rag_prompt_string(self, dictionary, start_index, batch_size, selected_chunk_str):
        """
        Generates a prompt string for a batch of multiple choice questions based on the provided information (RAG).

        Parameters:
            dictionary (dict): A dictionary containing the questions.
            startIndex (int): The index to start from in the dictionary.
            batch_size (int): The number of questions to include in the batch.
            selected_chunk_str (str): Additional information provided for the questions.

        Returns:
            str: A prompt string for the specified batch of questions.
        """
        prompt = "Instructions: Solve the following multiple choice question based on the information provided below. " \
                 "Output a single option as the final answer and enclosed by xml tags <answer></answer> \n"
        for i in range(start_index, start_index + batch_size):
            if i > len(dictionary):
                return prompt
            question = dictionary[i]
            prompt += str(question['question_id']) + ". " + question['question'] + "\n" + question['choices'] + "\n" + selected_chunk_str
        return prompt


    def get_score_xml(self, answer_string, question_dict):
        """
    Calculates the score based on the provided answers in XML format and the correct answers in the question dictionary.

        Parameters:
            answer_string (str): The answers provided by the model in XML format.
            question_dict (dict): A dictionary containing the correct answers for the questions.

        Returns:
            str: The percentage of correct answers.
        """
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


    def get_answer_xml(self, answer_string):
        """
        Extracts the answers from the LLM's response using XML tags.

        Parameters:
            answer_string (str): The LLM's response containing answers in XML format.

        Returns:
            list: A list of extracted answers.
        """
        pattern = r"<answer>([a-dA-D]|NaN)(?:\.[^<]*)?</answer>"

        # Find all matches in the text
        matches = re.findall(pattern, answer_string)
        choices = ["{}".format(answer) for answer in matches]

        for choice in choices:
            print(choice)
        print(len(choices))

        #result = '\n'.join(choices)
        return choices
