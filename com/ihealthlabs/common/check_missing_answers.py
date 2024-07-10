def check_missing_answers(filename):
    with open(filename, 'r') as file:
        content = file.read()
    
    questions = content.split('Instructions:')
    missing_answers = []
    
    for i, question in enumerate(questions[1:], start=1):  # start=1 to skip the first empty split
        if '<answer>' not in question or '</answer>' not in question:
            missing_answers.append(i)
    
    return missing_answers

# Usage
filename = 'gemini_1.5_pro_cot_exp1 copy 2.txt'  # Replace with your file name
missing_answers = check_missing_answers(filename)

if missing_answers:
    print(f'The following questions are missing answers: {missing_answers}')
else:
    print('All questions have answers.')
