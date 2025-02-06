import os

from dotenv import load_dotenv

from src.utils.common import load_yaml_file

load_dotenv()

class ChatbotConfig:
    cfg = load_yaml_file('src/config/config_file/chatbot.yaml')

    RUNPOD_TOKEN = os.getenv("RUNPOD_TOKEN")
    RUNPOD_URL = os.getenv("RUNPOD_URL")

    VECTOR_DATABASE_API_KEY = os.getenv('PINECONE_API_KEY')

    chatbot_cfg = cfg['chatbot']
    embedding_cfg = cfg['embedding']
    recommendation_cfg = cfg['recommendation']

    chatbot_model_name = chatbot_cfg['model_name']
    temperature = chatbot_cfg['temperature']
    top_p = chatbot_cfg['top_p']
    max_tokens = chatbot_cfg['max_tokens']

    embedding_model_name = embedding_cfg['model_name']
    embedding_model_cache = embedding_cfg['model_cache']
    vector_database_index_name = embedding_cfg['vector_database_index_name']
    namespace = embedding_cfg['namespace']
    top_k = embedding_cfg['top_k']

    apriori_recommendation_path = recommendation_cfg['apriori_recommendation_path']
    popular_recommendation_path = recommendation_cfg['popular_recommendation_path']
    apriori_top_k = recommendation_cfg['apriori_top_k']
    popular_top_k = recommendation_cfg['popular_top_k']


