# Registered Dietitian (RD) Exam Evaluation
This repository contains the codes to evaluate the accuracy and consistency of LLMs in addressing nutrition-related inquiries.  Our experiments include the GPT 4o, Claude 3.5 - Sonnet, and Gemini 1.5 Pro models along with Zero Shot (ZS), Chain of Thought (CoT), Chain of Thought with Self Consistency (CoT-SC), and Retrieval Augmented Prompting (RAP) techniques.

To achieve this, we use the Registered Dietitian (RD) exam, a standard certification examination that serves to assess if dietitians meet the qualifications required to practice in the dietetics and nutrition field. Our experiments include the [GPT 4o](https://openai.com/index/hello-gpt-4o/), [Claude 3.5 - Sonnet](https://www.anthropic.com/news/claude-3-5-sonnet), and [Gemini 1.5 Pro](https://blog.google/technology/ai/google-gemini-next-generation-model-february-2024/) models along with Zero Shot (ZS), Chain of Thought (CoT), Chain of Thought with Self Consistency (CoT-SC), and Retrieval Augmented Prompting (RAP) techniques. This evaluation includes 1050 multiple-choice questions with different proficiency levels, covering four nutrition domains: i.e., principles of dietetics, nutrition care, food service systems, and food and nutrition management.

We compare the responses with the ground truth answers, enabling an objective assessment of the models' performance. To examine the consistency of the responses, we conduct repeated measurements by presenting each model with the same set of questions five times using each prompting technique. The responses for each technique and model are compared within and across groups.


## Step 1: Prepare the Dataset & Set up
This repository doesn't contain any original exam questions we used for the experiements. You will need to have your own multiple choice questions ready in MySQL Workbench database with at least question_id, question, choices and answer columns for each question. Other setup instructions are listed in LLMs_multiple_choice_eval.ipynb under Set Up section. 

## Step 2: Connect to the Database and Get the Question
Once you have your dataset ready, you can connect to your database by using the codes in conn_mysql.py and save your database info to the .env file. Detailed steps and .env file template can be found in LLMs_multiple_choice_eval.ipynb. 

## Extra Step for RAP
This repository doesn't contain any original reference content we used for the experiements. You will need to have your own referenece contents ready in pdfs. You can use pdf_to_chunks.py to divide the pdf contents into chunks. Then use embedding.py to get the embeddings using Amazon Titan Embeddings V2 service. After that, you will use the codes in LLMs_multiple_choice_eval.ipynb to get the top 10 similar chunks and send them together with the RAP instructions later.

## Step 3: Choose the Prompts
Once you have the questions ready, you can select the prompt you want to use. In questions_mysql.py, you can find the prompt functions for ZS, CoT, and RAP. For CoT-SC, we used the same prompt for CoT.

## Step 4: Connect to LLMs
The LLM-connecting modules are under com/ihealthlabs/common: openai_api.py connects to GPT, gemini_api.py connects to Gemini, anthropic_bedrock_api.py connects to Claude via Amazon Bedrock. You can switch to different models if you wish. Detailed codes can be found in LLMs_multiple_choice_eval.ipynb. The responses got from each LLMs will be saved to a txt file for each round of experiment. 

## Extract the Answers and Find the Missing Ones
Once you have the txt file containing the LLM's response to the questions, you can use the codes in LLMs_multiple_choice_eval.ipynb to extract the answer in xml tags. Please note sometimes the LLMs may not give an answer, give an answer in other formath or give an irrelavant answer to some questions. The code in LLMs_multiple_choice_eval.ipynb also deals with those situations by listing them out. Please look into those questions and modify them to the xml format. The final list of LLM's choices to the question will be saved to the original txt file at the end as well as the wrong answers and the final score. 


## Evaluate the LLM responses in terms of accuracy and consistency
[LLM Response Analysis](LLM_response_analysis_pub.ipynb) includes code to assess the responses and perform statistical analysis. The evaluation of responses is based on two key metrics: accuracy and consistency. Accuracy assess how closely a set of responses aligns with the ground truth answers. To this end, the responses are initially imported and compared with the ground truth answers. Consistency measures the extent to which responses produce the same results. Our analysis is divided into four different parts.

1) **Overall Accuracy:** We calculate the percentage scores by determining the ratio of correct responses to total responses and multiplying by 100. The percentage score reflects the ability of the LLMs to identify the correct option. Each measurement is repeated five times. The five repeated measurements in each test are grouped, and the mean and standard deviation of the scores are calculated.

2) **Subcategory analysis:** The responses are categorized according to the questions’ proficiency levels and nutrition topics. The average error rates for these subcategories are then computed.

3) **Inter-rater analysis:** [Cohen's Kappa](https://journals.sagepub.com/doi/abs/10.1177/001316446002000104) is used to measure the degree of agreement between two sets of responses. For example, the agreement between responses obtained from GPT-4o with Zero Shot prompting and with Chain of Thought prompting are calculated. 

4) **Intra-rater analysis:** [Fleiss Kappa test](https://psycnet.apa.org/record/1972-05083-001) is used to measure the degree of overall agreement between the repeated measurements under fixed conditions. For instance, we assess whether GPT-4o with Zero Shot prompting provides the same choices in repeated measurements.
 


