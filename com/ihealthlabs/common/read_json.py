import json
import re

from conn_mysql import ClientMysql

class question:

    def __init__(self, question_content, choices, answer):
        self.question_content = question_content
        self.choices = choices
        self.answer = answer

    def toString(self):
        string = ""
        string += self.question_content
        string += self.choices
        string += self.answer
        return string

class Json_to_question:

    def __init__(self):
        self.mysql_client = ClientMysql()
    
    def parseJson(self, questions):
        question_list = []

        for ques in questions:
            if ques["type"] == "multiple_choice":
                for key in ques:
                    if key == "content":
                        question_content = re.search(r'<p>(.*?)<\/p>', ques[key]).group(1)
                        escaped_content = ""
                        for char in question_content:
                            if char == "'":
                                escaped_content += '\\'
                            escaped_content += char
                    elif key == "options":
                        options = ""
                        options += "a. " + ques[key][0] + " "
                        options += "b. " + ques[key][1] + " "
                        options += "c. " + ques[key][2] + " "
                        options += "d. " + ques[key][3] + " "
                        escaped_options = ""
                        for char in options:
                            if char == "'":
                                escaped_options += '\\'
                            escaped_options += char
                    elif key == "correctAnswers":
                        if ques[key] == "1":
                            answer = "a"
                        elif ques[key] == "2":
                            answer = "b"
                        elif ques[key]== "3":
                            answer = "c"
                        elif ques[key] == "4":
                            answer = "d"
                question_obj = question(escaped_content, escaped_options, answer)
                question_list.append(question_obj)
                #print(question_obj.toString())
        return question_list
               


if __name__ == '__main__':
    with open('/Users/mohanqi/Desktop/Questions/Toolkit2.json') as json_file:
        data = json.load(json_file)
    questions = data['questions']

    question_json = Json_to_question()
    question_json.parseJson(questions)




    