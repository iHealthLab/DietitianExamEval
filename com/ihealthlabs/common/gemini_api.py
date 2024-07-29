"""
Use the Gemini API to send a text message to Gemini and print the response stream.
"""
import google.generativeai as genai

from config import env
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type


class GeminiAIAPI(object):
    """
    This class connects to Gemini API directly.
    """

    def __init__(self):
        """
        Initializes a GeminiAIAPI object.
        """
        self._client = genai.configure(api_key=env.str("GEMINI_API_KEY"))

    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=10),
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type(ValueError)
    )
    def ask_gemini(self, question, model_str, temp):
        """
        Calls GeminiAPI for Gemini.
 
        Parameters:
            question (str): The prompt with the question you want to ask the LLM.
            model_id (str): The model you want to call the API with. 
            temp (str): The model temperature you want to set to.
    
        Returns:
            str: The response gets from the LLM.
        """
        # Error handling for ValueError
        try:
            res = ""
            model = genai.GenerativeModel(model_str)
            # Remove the default four safety settings
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
            ]

            response = model.generate_content(
                question,
                generation_config=genai.types.GenerationConfig(temperature=temp),
                safety_settings=safety_settings)

            # Debugging output
            # print("Response object:", response)

            for chunk in response:
                print(chunk.text)
                res += chunk.text
            return res
        except ValueError as e:
            # If a ValueError is raised, add "<answer>NaN<answer>" to the response and continue
            print(f"Exception caught: {e}")
            return "<answer>NaN</answer>"
