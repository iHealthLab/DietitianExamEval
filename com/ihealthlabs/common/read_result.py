import questions_mysql
import re

# Get the correct answers
qsql = questions_mysql.QuestionsMysql()
question_dict = qsql.get_RD_questions()

# Get the LLM's response from the txt file
with open('claude_3.5_sonnet_cot_exp1.txt', 'r') as file:
        content = file.read()

'''
# Find the missed answer
all_tags_pattern = r"<answer>[^<]*</answer>"

# Specific pattern to match
specific_pattern = r"<answer>([a-dA-D])(?:\.[^<]*)?</answer>"

# Find all answer tags
all_tags = re.findall(all_tags_pattern, content)

# Filter out those that match the specific pattern
non_matching_tags = [tag for tag in all_tags if not re.match(specific_pattern, tag)]

# Print non-matching tags
for tag in non_matching_tags:
    if tag!= "<answer></answer>":
        print(tag)
'''

# Get the answer list and score
answers = qsql.get_answer_xml(content)
score4 = qsql.get_score_xml(content, question_dict)
print(score4)

# Save answer list and score to the txt file
with open('claude_3.5_sonnet_cot_exp1.txt', 'w') as file:
    file.write(content + "Answer List: \n" + answers + "\n" + score4)
