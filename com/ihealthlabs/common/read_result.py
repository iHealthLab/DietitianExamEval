import questions_mysql
import re

# Get the correct answers
qsql = questions_mysql.QuestionsMysql()
question_dict = qsql.get_RD_questions()

# Get the LLM's response from the txt file
with open('gpt_4o_rag_test_run1.txt', 'r') as file:
        content = file.read()

# Get the answer list and score
choices = qsql.get_answer_xml(content)
if len(choices) == 1050:
    answers = '\n'.join(choices)
    score4 = qsql.get_score_xml(content, question_dict)
    print(score4)

    # Save answer list and score to the txt file
    with open('gpt_4o_rag_test_run1.txt', 'w') as file:
        file.write(content + "Answer List: \n" + answers + "\n" + score4)
else:
    # Find the missed answer
    all_tags_pattern = r"<answer>[^<]*</answer>"
    '''
    all_tags_pattern = r"[^<]*</answer>Instruction"
    
    all_tags = re.findall(all_tags_pattern, content)
    for tag in all_tags:
        print(tag)
    '''
    # Specific pattern to match
    specific_pattern = r"<answer>([a-dA-D]|NaN)(?:\.[^<]*)?</answer>"

    # Find all answer tags
    all_tags = re.findall(all_tags_pattern, content)

    # Filter out those that match the specific pattern
    non_matching_tags = [tag for tag in all_tags if not re.match(specific_pattern, tag)]

    # Print non-matching tags
    for tag in non_matching_tags:
        if tag!= "<answer></answer>":
            print(tag)