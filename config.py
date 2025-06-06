import os

# AWS Configuration
AWS_REGION = "us-west-2"
BEDROCK_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"
TITAN_MODEL_ID = "amazon.titan-embed-text-v1"

# File paths
CSV_PATH = "/Users/ethanschultz/Documents/GSB_570_GEN_AI/Code:Project/Data_current/cal_poly_embeddings.csv"

# Model configuration
MODEL_KWARGS = {
    "max_tokens": 2048,
    "temperature": 0.1,
    "top_k": 250,
    "top_p": 0.9,
    "stop_sequences": ["\n\nHuman"]
}