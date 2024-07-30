# RD Exam Eval
This repository contains the codes and steps to sending RD Exam questions to GPT 4o, Claude 3.5 - Sonnet, and Gemini 1.5 Pro with Zero Shot (ZS), Chain of Thought (CoT), Chain of Thought with Self Consistency (CoT-SC), and Retrieval Augmented Prompting (RAP), and getting responses for analysis and comparison. 


## Step 1: Prepare the Dataset & Set up
This repository doesn't contain any original exam questions we used for the experiements. You will need to have your own multiple choice questions ready in MySQL Workbench database with at least question_id, question, choices and answer columns for each question. Other setup instructions are listed in LLMs_multiple_choice_eval.ipynb under Set Up section. 

## Step 2: Connect to the Database and Get the Question One-by-One
Once you have your dataset ready, you can connect to your database by using the codes in conn_mysql.py and save your database info to the .env file. Detailed steps and .env file template can be found in LLMs_multiple_choice_eval.ipynb. 

## Extra Step for RAP
This repository doesn't contain any original reference content we used for the experiements. You will need to have your own referenece contents ready in pdfs. You can use pdf_to_chunks.py to divide the pdf contents into chunks. Then use embedding.py to get the embeddings using Amazon Titan Embeddings V2 service. After that, you will use the codes in LLMs_multiple_choice_eval.ipynb to get the top 10 similar chunks and send them together with the RAP instructions later.

## Step 3: Choose the Prompts
Once you have the questions ready, you can select the prompt you want to use. In questions_mysql.py, you can find the prompt functions for ZS, CoT, and RAP. For CoT-SC, we used the same prompt for CoT.

## Step 4: Connect to LLMs
The LLM-connecting modules are under com/ihealthlabs/common: openai_api.py connects to GPT, gemini_api.py connects to Gemini, anthropic_bedrock_api.py connects to Claude via Amazon Bedrock. You can switch to different models if you wish. Detailed codes can be found in LLMs_multiple_choice_eval.ipynb. The responses got from each LLMs will be saved to a txt file for each round of experiment. 

## Step 5: Extract the Answers and Find the Missing Ones
Once you have the txt file containing the LLM's response to the questions, you can use the codes in LLMs_multiple_choice_eval.ipynb to extract the answer in xml tags. Please note sometimes the LLMs may not give an answer, give an answer in other formath or give an irrelavant answer to some questions. The code in LLMs_multiple_choice_eval.ipynb also deals with those situations by listing them out. Please look into those questions and modify them to the xml format. The final list of LLM's choices to the question will be saved to the original txt file at the end as well as the wrong answers and the final score. 



 


