import json

from copy import deepcopy
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone


from src.utils.response import get_chat_response, get_client
from src.utils.logger import logging
from src.config.app_config import ChatbotConfig as cc

EMBEDDING_MODEL = None

class DetailAgent:
    def __init__(self):
        global EMBEDDING_MODEL

        self.client = get_client(
            api_key=cc.RUNPOD_TOKEN,
            url=cc.RUNPOD_URL
        )

        if EMBEDDING_MODEL is None:
            logging.info('Loading embedding model for the first time ...')
            EMBEDDING_MODEL = SentenceTransformer(
                model_name_or_path=cc.embedding_model_name,
                cache_folder=cc.embedding_model_cache
                )
        
        self.embedding = EMBEDDING_MODEL
        
        self.vector_database = Pinecone(api_key=cc.VECTOR_DATABASE_API_KEY)
        self.vector_database_index_name = cc.vector_database_index_name
        
        self.model_name = cc.chatbot_model_name
        logging.info('Initialize detail agent ...')


    def get_results(self, index_name, input_embedding, top_k):
        index = self.vector_database.Index(index_name)

        results = index.query(
            namespace=cc.namespace,
            vector=input_embedding,
            top_k=cc.top_k,
            include_values=False,
            include_metadata=True
        )

        return results
    

    def postprocess(self, output):
        output = {
            "role": "assistant",
            "content": output,
            "memory": {"agent":"details_agent"}
        }
        
        return output

    

    def get_response(self, messages):
        messages = deepcopy(messages)
        
        user_message = messages[-1]['content']
        
        embedding = self.embedding.encode(user_message).tolist()
        results = self.get_results(
            index_name=self.vector_database_index_name,
            input_embedding=embedding,
            top_k=cc.top_k
        )

        source_knowledge = "\n".join([x['metadata']['text'].strip()+'\n' for x in results['matches'] ])

        prompt = f"""
        Using the contexts below, answer the query.

        Contexts:
        {source_knowledge}

        Query: {user_message}
        """

        system_prompt = """ 
        You are a customer support agent for a coffee shop. You should answer every questions as if you are a waiter and provide the neccessary information to the user regarding their orders 
        """

        messages[-1]['content'] = prompt
        input_messages = [{'role': 'system', 'content': system_prompt}] + messages[-3:]

        chatbot_output = get_chat_response(
            client=self.client,
            model_name=self.model_name,
            messages=input_messages
        )

        output = self.postprocess(output=chatbot_output)

        return output