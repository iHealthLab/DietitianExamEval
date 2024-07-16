import ast
import pandas as pd
import numpy as np
import sys
sys.path.append('/Users/mohanqi/vscode/ai/ai-benchmark/com/ihealthlabs/common')
import openai_api
from questions_mysql import QuestionsMysql

from sklearn.metrics.pairwise import cosine_similarity
from embedding import TitanEmbeddings


def find_most_similar_chunks(
        query_embedding: list,
        df: pd.DataFrame,
        number_of_chunks: int = 10) -> np.ndarray:
    """
    Search for the most similar chunks
    
    Args:
        query_embedding (list): The embedding of the question.
        df (pd.DataFrame): The dataframe including the chunks and their embeddings.
        number_of_chunks (int): Number of smilar chunks to be selected.
    
    Returns:
        similar_chunks (np.ndarray): The array of N most similar chunks.
    """
    #print(type(query_embedding))
    # Convert the 'chunk_embedding' column to an array of arrays
    chunk_embeddings = df['chunk_embedding'].apply(ast.literal_eval).tolist()
    chunk_embeddings = np.array(chunk_embeddings)
    
    cosine_scores = cosine_similarity([query_embedding], chunk_embeddings)[0]
    cosine_scores_sorted_indices = np.argsort(cosine_scores)[::-1]
    print(cosine_scores[cosine_scores_sorted_indices])
    sorted_chunks_text = df['chunk'].iloc[cosine_scores_sorted_indices]
    similar_chunks = sorted_chunks_text.head(number_of_chunks)
    return similar_chunks.values


if __name__ == '__main__':
    # Read question from a file
    qsql = QuestionsMysql()
    # Connect to RD Exam Questions
    question_dict = qsql.get_RD_questions()

    api = openai_api.OpenAIAPI()

    # Load knowledge dataframe (chunks)
    FILE_PATH = '/Users/mohanqi/vscode/ai/ai-benchmark/rag_rd_exam/chunks_df_sample.csv'
    columns_to_read = ['chunk', 'chunk_embedding']
    df_knowledge = pd.read_csv(FILE_PATH, usecols=columns_to_read)

    response = "\n"
    for startIndex in range (1, len(question_dict) + 1, 1):
        query = question_dict[startIndex]['question'] + question_dict[startIndex]['choices']

        # Obtain the embedding of the question using the embedding model
        dimensions = 1024
        normalize = True

        titan_embeddings_v2 = TitanEmbeddings(model_id="amazon.titan-embed-text-v2:0")

        input_text = query
        query_embeddings = titan_embeddings_v2(input_text, dimensions, normalize)
        #print(query_embeddings)

        # Cosine similarity
        selected_chunks = find_most_similar_chunks(query_embeddings, df_knowledge)

        # Covert the selected chunks to string to be added to the prompt
        selected_chunks_str = np.array2string(selected_chunks, separator=', ')

        with open('gpt_4o_rag_test.txt', 'r') as file:
            content = file.read()

        prompt_str = qsql.get_rag_prompt_string(question_dict, startIndex, 1, selected_chunks_str)

        response += api.ask_chatgpt(prompt_str, "gpt-4o", 0)
        response += "\n"

        with open('gpt_4o_rag_test.txt', 'w') as file:
            file.write(content + prompt_str + "\n" + response + "\n\n\n")

    


    

