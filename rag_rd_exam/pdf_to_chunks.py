import os
import math
from pdfminer.high_level import extract_text
import pandas as pd
from typing import List


def get_references_list(dir_path: str) -> List[str]:
    """
    Extract the list of PDF files in the directory.
    
    Args:
        dir_path (str): The directory including references.
    
    Returns:
        pdf_files (List[str]): The list of PDF files in the directory.
    """
    files = os.listdir(dir_path)
    pdf_files = [file for file in files if file.lower().endswith('.pdf')]
    pdf_files.sort()
    return pdf_files


def text_to_chunks(text: str,
                   tokens_per_chunk: int = 512,
                   chars_per_token: float = 4.7) -> List[str]:
    """
    Split the input text into chunks
    
    Args:
        text (str): the input text.
        tokens_per_chunk (int): The number of tokens per chunk.
        chars_per_token (float): The average number of characters per token.
    
    Returns:
        chunks (List[str]): A list of chunks.
    """
    chars_per_chunk = math.ceil(tokens_per_chunk * chars_per_token)
    chunks = [text[i:i+chars_per_chunk] for i in range(0, len(text), chars_per_chunk)]
    return chunks


def pdf_to_chunks(dir_path: str,
                   file_name: str,
                   df_current: pd.DataFrame) -> pd.DataFrame:
    """
    Read PDF files and convert them into text chunks
    
    Args:
        dir_path (str): The directory including references.
        file_name (str): The file name (PDF).
        df_current (pd.DataFrame): The dataframe to which the new data are added.
    
    Returns:
        df_out (pd.DataFrame): A dataframe including the chunks
    """
    data = []
    file_text = extract_text(os.path.join(dir_path, file_name))
    split_text = text_to_chunks(file_text)
    for chunk_id, chunk in enumerate(split_text):
        data.append({'file_name': file_name, 'chunk_id': chunk_id, 'chunk': chunk})
    df_out = pd.concat([df_current, pd.DataFrame(data)], ignore_index=True)
    return df_out


if __name__ == '__main__':
    DIR_PATH = 'references'
    refs_list = get_references_list(DIR_PATH)
    df = pd.DataFrame(columns=['file_name', 'chunk_id', 'chunk'])
    #
    refs_with_error = []
    for idx, ref in enumerate(refs_list):
        try:
            print(str(idx) + ": " + ref)
            df = pdf_to_chunks(DIR_PATH, ref, df)
        except Exception as e:
            refs_with_error.append(ref)
    with open('error_list.txt', 'w') as file:
        for item in refs_with_error:
            file.write(f"{item}\n")
    df.to_csv('chunks_df.csv', index=False)
