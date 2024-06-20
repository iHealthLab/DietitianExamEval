import json

import sqlalchemy
from read_json import Json_to_question
from conn_mysql import ClientMysql


class DBUtils:

    def __init__(self):
        self.mysql_client = ClientMysql()

    def create_non_cover_patients(self, table_name):
        table = table_name
        self.mysql_client.execute('''DROP TABLE IF EXISTS {}'''.format(table))
        self.mysql_client.execute(
            '''
               CREATE TABLE IF NOT EXISTS `{}` (
                `id`                        int AUTO_INCREMENT,
                `memberId`                  varchar(24) NOT NULL,
                `firstName`                 varchar(50) NOT NULL,
                `lastName`                  varchar(50) NOT NULL,
                `birthday`                  datetime,
                `teamId`                    varchar(24),
                `organizationId`            varchar(24),
                PRIMARY KEY `id` (`id`)
            ) 
        '''.format(table))

    def create_multiplp_choices(self, table_name):
        table = table_name
        self.mysql_client.execute(
            '''
               CREATE TABLE IF NOT EXISTS `{}` (
                `question_id`               int AUTO_INCREMENT,
                `question_number`           int AUTO_INCREMENT,
                `question_content`          text NOT NULL,
                `choices`                   text,
                `answer`                    text,
                `category`                  text NULL,
                PRIMARY KEY `question_id` (`question_id`)
            ) 
        '''.format(table))

    # Add data to CDCESQuestion table
    def add_cdces_data(self, table_name, question_list):
        table = table_name
        for question in question_list:
            query = "INSERT INTO " + table + " (question, choices, answer) VALUES ('" + question.question_content + "', '" + question.choices + "', '" + question.answer + "')"
            sql_query = sqlalchemy.text(query)
            self.mysql_client.execute(sql_query)
    
    # Add data to RDQuestions table
    def add_rd_data(self, table_name, question_list):
        table = table_name
        for question in question_list:
            query = "INSERT INTO " + table + " (question, choices, answer, explanation, difficulty_level, answer_references) VALUES ('" + question.question_content + "', '" + question.choices + "', '" + question.answer + "', '" + question.explanation + "', '" + question.difficulty_level + "', '" + question.references + "')"
            sql_query = sqlalchemy.text(query)
            self.mysql_client.execute(sql_query)
    
    # Add ADCES data to CDCESQuestions table
    def add_rd_data(self, table_name, question_list):
        table = table_name
        for question in question_list:
            query = "INSERT INTO " + table + " (question, choices, answer, explanation) VALUES ('" + question.question_content + "', '" + question.choices + "', '" + question.answer + "', '" + question.explanation + "')"
            sql_query = sqlalchemy.text(query)
            self.mysql_client.execute(sql_query)

if __name__ == '__main__':
    
    # Add CDCES Questions
    '''
    db = DBUtils()
    question_json = Json_to_question()
    with open('/Users/mohanqi/Desktop/Questions/Toolkit4.json') as json_file:
        data = json.load(json_file)
    questions = data['questions']
    db.add_cdces_data('CDCESQuestions', question_json.parseJson(questions))
    '''

    # Add RD Questions
    db = DBUtils()
    question_json = Json_to_question()
    with open('/Users/mohanqi/Desktop/Questions/ADCES_practice_exam_2.json') as json_file:
        data = json.load(json_file)
    db.add_rd_data('CDCESQuestions', question_json.parseADCESJson(data))