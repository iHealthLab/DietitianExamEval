import os
import pandas as pd
import PyPDF2
from pdf_to_chunks import text_to_chunks


def pdf_read(dir_path: str, file_name: str) -> str:
    """
    Read PDF files
    
    Args:
        dir_path (str): The directory including references.
        file_name (str): The file name (PDF).
    
    Returns:
        file_text (str): The extracted text from PDF file
    """
    reader = PyPDF2.PdfReader(os.path.join(dir_path, file_name))
    num_pages = len(reader.pages)
    file_text = ""
    for page_num in range(num_pages):
        page = reader.pages[page_num]
        file_text += page.extract_text()
    return file_text


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
    # file_text = extract_text(os.path.join(dir_path, file_name))
    file_text = pdf_read(dir_path, file_name)
    split_text = text_to_chunks(file_text)
    for chunk_id, chunk in enumerate(split_text):
        data.append({'file_name': file_name, 'chunk_id': chunk_id, 'chunk': chunk})
    df_out = pd.concat([df_current, pd.DataFrame(data)], ignore_index=True)
    return df_out


if __name__ == '__main__':
    DIR_PATH = 'references'
    # Read from the error_list file
    with open('error_list.txt', 'r') as file:
        refs_list = file.readlines()
    refs_list = [line.strip() for line in refs_list]
    df = pd.DataFrame(columns=['file_name', 'chunk_id', 'chunk'])
    #
    for idx, ref in enumerate(refs_list):
        print(str(idx) + ": " + ref)
        df = pdf_to_chunks(DIR_PATH, ref, df)
    #print(df)
    df_loaded = pd.read_csv('chunks_df.csv')
    df = pd.concat([df_loaded, df], ignore_index=True)
    df.to_csv('chunks_df_updated.csv', index=False)
