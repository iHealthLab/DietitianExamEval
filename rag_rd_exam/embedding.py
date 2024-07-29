"""
This module provides an interface to obtain embeddings using the Amazon Titan Embeddings V2 service.
"""
import json
import boto3

class TitanEmbeddings(object):
    """
    A class to obtain embeddings from the Amazon Titan Embeddings V2 service.

    Attributes:
        accept (str): The accepted response format.
        content_type (str): The content type of the request.
        bedrock (boto3.Client): The Boto3 client for interacting with Bedrock runtime.
        model_id (str): The model ID for generating embeddings.

    Methods:
        __call__(text, dimensions, normalize=True): Returns the embeddings for the given text.
    """
    accept = "application/json"
    content_type = "application/json"

    def __init__(self, model_id="amazon.titan-embed-text-v2:0"):
        """
        Initializes the TitanEmbeddings class with a specified model ID.

        Parameters:
            model_id (str): The ID of the model to use for embedding.
        """
        self.bedrock = boto3.client(service_name='bedrock-runtime', region_name="us-west-2")
        self.model_id = model_id

    def __call__(self, text, dimensions, normalize=True):
        """
        Returns Titan Embeddings
        Args:
            text (str): text to embed
            dimensions (int): Number of output dimensions.
            normalize (bool): Whether to return the normalized embedding or not.
        Return:
            List[float]: Embedding
            
        """
        body = json.dumps({
            "inputText": text,
            "dimensions": dimensions,
            "normalize": normalize
        })
        response = self.bedrock.invoke_model(
            body=body, modelId=self.model_id, accept=self.accept, contentType=self.content_type
        )
        response_body = json.loads(response.get('body').read())
        return response_body['embedding']
