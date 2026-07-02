import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"