"""
Use the OpenAI API to send a text message to GPT 4o and print the response stream.
"""

import openai
from openai import OpenAI
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from httpx import RemoteProtocolError

from config import env

class OpenAIAPI(object):
    """
    This class connects to OpenAI API.
    """

    def __init__(self):
        """
        Initializes an OpenAIAPI object.
        """
        openai.api_key = env.str("OPENAI_API_KEY")

    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=10),
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type(RemoteProtocolError)
    )
    def ask_chatgpt(self, question, model_str, temp):
        """
        Calls OpenAI API for GPT 4o.
 
        Parameters:
            question (str): The prompt with the question you want to ask the LLM.
            model_id (str): The model you want to call the API with. 
            temp (str): The model temperature you want to set to.
    
        Returns:
            str: The response gets from the LLM.
        """
        res = ""
        client = OpenAI(api_key = env.str("OPENAI_API_KEY"))
        stream = client.chat.completions.create(
            model=model_str,
            messages=[{"role": "user", "content": question}],
            stream=True,
            temperature=temp,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")
                res += chunk.choices[0].delta.content
        return res
