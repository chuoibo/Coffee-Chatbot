import json

from copy import deepcopy

from src.utils.response import get_chat_response, get_client
from src.utils.logger import logging
from src.config.app_config import ChatbotConfig as cc


class ClassificationAgent:
    def __init__(self):
        self.client = get_client(
            api_key=cc.RUNPOD_TOKEN,
            url=cc.RUNPOD_URL
        )

        self.model_name = cc.chatbot_model_name
        logging.info('Initialize classification agent ...')


    def postprocess(self, output):
        output = json.loads(output)

        dict_output = {
            "role": "assistant",
            "content": output['message'],
            "memory": {
                "agent": "classification_agent",
                "classification_agent": output['decision']
            }
        }

        return dict_output

    
    def get_response(self, messages):
        messages = deepcopy(messages)

        system_prompt = """
            You are a helpful AI assistant for coffee shop application.
            Your task is to determine which agent should handle user input. You have 3 agents to choose from:
            1. detail_agent: This agent is responsible for answering questions about the coffee shop like location, delivery places, working hours, detail about menu items or listing items in the menu or asking what we have.
            2. order_taking_agent: This agent is responsible for taking orders from the user. It's responsible to have a conversation with the user about the orders until it is completed.
            3. recommendation_agent: This agent is responsible for giving recommendations to the user about what to buy. If the user asks for the recommendation, this agent will be used.

            Your output must be in structured json format like this below. Each key is a string and each value is a string. Make sure to follow the format strictly:
            {
            "chain of thought": go over each of the points above and let see if the message lies under this point or not. Then you write some of your thoughts about what point is this input relevant to. ,
            "decision": "details_agent" or "order_taking_agent" or "recommendation_agent". Pick one of those and only write the word. ,
            "message": leave the message empty
            }
            """
        
        input_messages = [
            {'role': 'system', 'content': system_prompt}
        ]

        input_messages += messages[-3:]

        chatbot_output = get_chat_response(
            client=self.client,
            model_name=self.model_name,
            messages=input_messages
        )

        
        logging.info(f'-----------------------------{chatbot_output}')


        output = self.postprocess(output=chatbot_output)

        return output