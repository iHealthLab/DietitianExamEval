import json
import re

from conn_mysql import ClientMysql

class question:

    def __init__(self, question_content, choices, answer):
        self.question_content = question_content
        self.choices = choices
        self.answer = answer

    def __init__(self, question_content, choices, answer, explanation, difficulty_level, references):
        self.question_content = question_content
        self.choices = choices
        self.answer = answer
        self.explanation = explanation
        self.difficulty_level = difficulty_level
        self.references = references


    def toString(self):
        string = ""
        string += self.question_content
        string += "\n"
        string += self.choices
        string += "\n"
        string += self.answer
        string += "\n"
        string += self.explanation
        string += "\n"
        string += self.difficulty_level
        string += "\n"
        string += self.references
        string += "\n"
        string += "\n"
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
    


    def parseRdJson(self, questions):
        question_list = []

        for ques in questions:
            for key in ques:
                if key == "question":
                    question_content = ques[key]
                    escaped_content = ""
                    for char in question_content:
                        if char == "'" or char == "(" or char ==")":
                            escaped_content += '\\'
                        escaped_content += char
                elif key == "choices":
                    options = ""
                    options += "A. " + ques[key][0] + " "
                    options += "B. " + ques[key][1] + " "
                    options += "C. " + ques[key][2] + " "
                    options += "D. " + ques[key][3] + " "
                    escaped_options = ""
                    for char in options:
                        if char == "'":
                            escaped_options += '\\'
                        escaped_options += char
                elif key == "correct_answer":
                    answer = ques[key]
                elif key == "explanation":
                    explanation = ques[key][0]
                    escaped_exp = ""
                    for char in explanation:
                        if char == "'":
                            escaped_exp += '\\'
                        escaped_exp += char
                elif key == "difficulty_level":
                    difficulty_level = ques[key][0]
                elif key == "references":
                    references = ""
                    for value in ques[key]:
                        references += value
                        references += " "
                    escaped_references = ""
                    for char in references:
                        if char == "'" or char == "(" or char ==")":
                            escaped_references += '\\'
                        elif char == ":":
                            escaped_references += ':'
                        escaped_references += char
            question_obj = question(escaped_content, escaped_options, answer, escaped_exp, difficulty_level, escaped_references)
            question_list.append(question_obj)
            #print(question_obj.toString())
        return question_list


if __name__ == '__main__':
    with open('/Users/mohanqi/Desktop/Questions/questions_rd_test_2.json') as json_file:
        data = json.load(json_file)
    #questions = data['questions']

    question_json = Json_to_question()
    question_json.parseRdJson(data)




    