import ast
import pandas as pd
import numpy as np
import sys
sys.path.append('/Users/mohanqi/vscode/ai/ai-benchmark/com/ihealthlabs/common')
import openai_api

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
    # TODO
    query = 'An RDN is planning a community nutrition program and has already completed the community needs assessment, defined program goals and objectives, and developed a program plan. What is the next step in the process?\nA. Identify funding sources. B. Define the management system. C. Implement the program. D. Seek support from the stakeholders '

    # Obtain the embedding of the question using the embedding model
    # TODO
    dimensions = 1024
    normalize = True

    titan_embeddings_v2 = TitanEmbeddings(model_id="amazon.titan-embed-text-v2:0")

    input_text = query
    query_embeddings = titan_embeddings_v2(input_text, dimensions, normalize)
    #print(query_embeddings)


    # Load knowledge dataframe (chunks)
    FILE_PATH = '/Users/mohanqi/vscode/ai/ai-benchmark/rag_rd_exam/chunks_df_sample.csv'
    columns_to_read = ['chunk', 'chunk_embedding']
    df_knowledge = pd.read_csv(FILE_PATH, usecols=columns_to_read)

    # Cosine similarity
    selected_chunks = find_most_similar_chunks(query_embeddings, df_knowledge)
    #print(selected_chunks)
    #print(type(selected_chunks))
    # Add the chunks to the input prompt
    # TODO
    
    api = openai_api.OpenAIAPI()
    selected_chunks_str = np.array2string(selected_chunks, separator=', ')
    prompt_str = query + "Instructions: Solve the following multiple choice question based on the information provided below. Output a single option as the final answer and enclosed by xml tags <answer></answer> \n" + selected_chunks_str
    print("Prompt:" + prompt_str)
    response = api.ask_chatgpt(prompt_str, "gpt-4o", 0)
    print("GPT 4o Response: " + response)

