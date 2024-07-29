"""
Use the BedRock API to send a text message to Anthropic Claude and print the response stream.
"""
import json
import boto3
import urllib3.exceptions

from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

class AnthropicBedRockAPI:
    """
    This class connects to Amazon BedRock API for Anthropic Claude AI.
    """
    def __init__(self):
        """
        Initializes an AnthropicBedRockAPI object.
        """
        # Create a Bedrock Runtime client in the AWS Region of your choice.
        self.client = boto3.client("bedrock-runtime", region_name="us-east-1")

    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=10),
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type(urllib3.exceptions.ReadTimeoutError)
    )
    def ask_claude(self, question, model_id, temp):
        """
        Calls BedRockAPI for Claude AI.
 
        Parameters:
            question (str): The prompt with the question you want to ask the LLM.
            model_id (str): The model you want to call the API with. 
            temp (str): The model temperature you want to set to.
    
        Returns:
            str: The response gets from the LLM.
        """
        # Format the request payload using the model's native structure.
        native_request = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2046,
            "temperature": temp,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": question}],
                }
            ],
        }

        # Convert the native request to JSON.
        request = json.dumps(native_request)

        # Invoke the model with the request.
        streaming_response = self.client.invoke_model_with_response_stream(
            modelId=model_id, body=request
        )

        res = ""
        # Extract and print the response text in real-time.
        for event in streaming_response["body"]:
            chunk = json.loads(event["chunk"]["bytes"])
            if chunk["type"] == "content_block_delta":
                print(chunk["delta"].get("text", ""), end="")
                res += chunk["delta"].get("text", "")
        return res
