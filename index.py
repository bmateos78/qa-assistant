import json
import os
import sys
import boto3
from botocore.exceptions import ClientError


def generate_response(query=""):
    system_prompt = [{"text": "You are an assistant which writes test cases for a web project called AMG."
                        "The output should be formatted as a table in Jira with the headers 'Test Step' and 'Expected Result'. The basic table code is:"
                        "||Heading 1||Heading 2||"
                        "|Col A1|Col A2|"
                        "All testcases should include negative tests."
                        "All testcases that contain a change in design, should include these tests as the last steps of the table after all other tests (each step should appear once in the table):"
                        "- check i18n keys in German and English"
                        "- test on browsers Chrome, Firefox, Safari"
                        "- test on iPhone and Samsung phones"
                        "All testcases should be in a format to copy-paste it directly to Jira"}]
    
    # Start the conversation with the 1st message.
    message_1 = {"role": "user", "content": [{"text":"Generate a test case"}]}
    
    messages = []
    messages.append(message_1)
    
    #Inference parameters to use.
    modelId = 'anthropic.claude-3-sonnet-20240229-v1:0'
    temperature = 0.1
    top_k = 50
    inference_config = {"temperature": temperature}
    additional_model_fields = {"top_k": top_k}

    
    boto3_bedrock = boto3.client("bedrock-runtime",region_name="us-east-1")

    # Send the message.
    response = boto3_bedrock.converse(
        modelId=modelId,
        messages=messages,
        system=system_prompt,
        inferenceConfig=inference_config,
        additionalModelRequestFields=additional_model_fields
    )
    
    try:
        response_text = response['output']['message']
        return response_text
    except ClientError as err:
        error_message = err.response['Error']['Message']
        print(f"A client error occured: {error_message}")
        return error_message
    



resp = generate_response()
print(f"Response::::::::::::\n{resp['content'][0]['text']}")