# Registered Dietitian (RD) Exam Evaluation
This repository contains the codes to evaluate the accuracy and consistency of LLMs in addressing nutrition-related inquiries.  Our experiments include the GPT 4o, Claude 3.5 - Sonnet, and Gemini 1.5 Pro models along with Zero Shot (ZS), Chain of Thought (CoT), Chain of Thought with Self Consistency (CoT-SC), and Retrieval Augmented Prompting (RAP) techniques.

To achieve this, we use the Registered Dietitian (RD) exam, a standard certification examination that serves to assess if dietitians meet the qualifications required to practice in the dietetics and nutrition field. Our experiments include the [GPT 4o](https://openai.com/index/hello-gpt-4o/), [Claude 3.5 - Sonnet](https://www.anthropic.com/news/claude-3-5-sonnet), and [Gemini 1.5 Pro](https://blog.google/technology/ai/google-gemini-next-generation-model-february-2024/) models along with Zero Shot (ZS), Chain of Thought (CoT), Chain of Thought with Self Consistency (CoT-SC), and Retrieval Augmented Prompting (RAP) techniques. This evaluation includes 1050 multiple-choice questions with different proficiency levels, covering four nutrition domains: i.e., principles of dietetics, nutrition care, food service systems, and food and nutrition management.

We compare the responses with the ground truth answers, enabling an objective assessment of the models' performance. To examine the consistency of the responses, we conduct repeated measurements by presenting each model with the same set of questions five times using each prompting technique. The responses for each technique and model are compared within and across groups.


## Step 1: Prepare the Dataset
The RD exam questions used in this study are not publicly available and can be accessed via https://www.eatrightprep.org. Please note this repository doesn't contain any original exam questions we used for the experiements. To prepare the dataset, we get the questions in Json format and import them into MySQL Workbench database with question_id, question, choices, answer and difficulty_level columns for each question so we can utilize the questions with different prompt instructions later. With the questions saved in the database, we can reuse the questions for each rounds of each LLMs.

## Step 2: Connect to the Database and Get the Question
In order to send the questions to the LLMs, we connect to the database to get the question contents and choices. After we have all the questions imported into the database, we save the database info to the .env file and connect to the database using the codes [here](conn_mysql.py). Detailed steps and .env file template can be found in [LLMs multiple choice eval](LLMs_multiple_choice_eval.ipynb). 

## Extra Step for RAP
For RAP specifically, it requires extra steps to collect relevant reference contents, process the contents into chunks, turn the chunks into embeddings and then use the cosine similarity to find the top 10 similar chunks. When sending the questions with the RAP, the top 10 similar chunks will be sent together so the model can generate responses by relying not only on its internal knowledge but also on external relevant information. In our study, the knowledge base contains 125 references, including articles, books, and guidelines, recommended by the Academy of Nutrition and Dietetics, as references for the RD exam. The whole reference list can be found in the supplementary table of the paper. Please note this repository doesn't contain any original reference content used for the experiements. [This file](pdf_to_chunks.py) is used to divide the pdf contents into chunks. Then follow the instructions in [LLMs multiple choice eval](LLMs_multiple_choice_eval.ipynb) to get the embeddings using Amazon Titan Embeddings V2 service and find the top 10 similar chunks for each question. These top 10 similar chunks will be sent with the RAP instruction and the questions to the LLMs later.

## Step 3: Choose the Prompts
3 different prompt instructions are used in this study, including ZS, CoT, and RAP. These instructions will be combined with the questions to form the prompt message to be sent to the LLMs to get responses. In [this file](questions_mysql.py), you can find the prompt functions for ZS, CoT, and RAP. For CoT-SC, we use the same prompt for CoT.

## Step 4: Connect to LLMs
When the prompt message with instruction and question is ready, the next step is to connect to the LLMs to send the prompt message and get the response from the LLMs. The responses got from each LLMs will be saved to a txt file for each round of experiment. The LLM-connecting modules we used are: [openai_api.py](openai_api.py) connects to GPT, [gemini_api.py](gemini_api.py) connects to Gemini, [anthropic_bedrock_api.py](anthropic_bedrock_api.py) connects to Claude via Amazon Bedrock. Detailed instructions and codes can be found in [LLMs multiple choice eval](LLMs_multiple_choice_eval.ipynb).

## Extract the Answers and Find the Missing Ones
After the txt file containing the LLM's responses to the questions is obtained, we will use codes to extract the answers in xml tags. In some occassions, the LLMs may not give an answer, give an answer in other formath or give an irrelavant answer to some questions. Therefore, we also have codes to deal with those situations by listing them out. We then look into those questions and modify them to the xml format. Then we run the codes to extract the answers again and the final list of LLM's choices to the question will then be saved to the original txt file at the end. Detailed instructions and codes can be found in [LLMs multiple choice eval](LLMs_multiple_choice_eval.ipynb).


## Evaluate the LLM responses in terms of accuracy and consistency
[LLM Response Analysis](LLM_response_analysis_pub.ipynb) includes code to assess the responses and perform statistical analysis. The evaluation of responses is based on two key metrics: accuracy and consistency. Accuracy assess how closely a set of responses aligns with the ground truth answers. To this end, the responses are initially imported and compared with the ground truth answers. Consistency measures the extent to which responses produce the same results. Our analysis is divided into four different parts.

1) **Overall Accuracy:** We calculate the percentage scores by determining the ratio of correct responses to total responses and multiplying by 100. The percentage score reflects the ability of the LLMs to identify the correct option. Each measurement is repeated five times. The five repeated measurements in each test are grouped, and the mean and standard deviation of the scores are calculated.

2) **Subcategory analysis:** The responses are categorized according to the questions’ proficiency levels and nutrition topics. The average error rates for these subcategories are then computed.

3) **Inter-rater analysis:** [Cohen's Kappa](https://journals.sagepub.com/doi/abs/10.1177/001316446002000104) is used to measure the degree of agreement between two sets of responses. For example, the agreement between responses obtained from GPT-4o with Zero Shot prompting and with Chain of Thought prompting are calculated. 

4) **Intra-rater analysis:** [Fleiss Kappa test](https://psycnet.apa.org/record/1972-05083-001) is used to measure the degree of overall agreement between the repeated measurements under fixed conditions. For instance, we assess whether GPT-4o with Zero Shot prompting provides the same choices in repeated measurements.
 


