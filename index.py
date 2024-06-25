import json
import os
import sys
import boto3

boto3_bedrock = boto3.client('bedrock')

boto3_bedrock.list_foundation_models()

print(f"OK: {boto3_bedrock.list_foundation_models()}")