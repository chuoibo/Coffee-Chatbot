import os

from dotenv import load_dotenv

from src.utils.common import load_yaml_file

load_dotenv()

class ChatbotConfig:
    cfg = load_yaml_file('src/config/config_file/chatbot.yaml')

    RUNPOD_TOKEN = os.getenv("RUNPOD_TOKEN")
    RUNPOD_URL = os.getenv("RUNPOD_URL")

    chatbot_cfg = cfg['chatbot']
    embedding_cfg = cfg['embedding']

    chatbot_model_name = chatbot_cfg['model_name']
    temperature = chatbot_cfg['temperature']
    top_p = chatbot_cfg['top_p']
    max_tokens = chatbot_cfg['max_tokens']

    embedding_model_name = embedding_cfg['model_name']


