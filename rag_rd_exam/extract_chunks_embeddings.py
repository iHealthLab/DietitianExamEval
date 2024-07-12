import pandas as pd

from embedding import TitanEmbeddings


if __name__ == '__main__':
    # Load the knowledge dataframe (chunks)
    #FILE_NAME = 'chunks_df_sample.csv'
    #df_knowledge = pd.read_csv(FILE_NAME)
    file_path = '/Users/mohanqi/vscode/ai/ai-benchmark/rag_rd_exam/chunks_df_sample.csv'
    df_knowledge = pd.read_csv(file_path)

    all_chunk_embeddings = []
    # Obtain the embedding of the chunks using the embedding model
    # TODO
    for chunk in df_knowledge['chunk']:
        dimensions = 1024
        normalize = True
    
        titan_embeddings_v2 = TitanEmbeddings(model_id="amazon.titan-embed-text-v2:0")

        input_text = chunk
        chunk_embeddings = titan_embeddings_v2(input_text, dimensions, normalize)
        all_chunk_embeddings.append(chunk_embeddings)
        print(chunk_embeddings)

    # Add the embedding to the dataframe under a column, for example
        # with the following name 'chunk_embedding'
    df_knowledge['chunk_embedding'] = all_chunk_embeddings

    # Save the updated dataframe
    df_knowledge.to_csv(file_path, index=False)
    print("Done!")
