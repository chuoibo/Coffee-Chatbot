import json

from copy import deepcopy

from src.utils.response import get_chat_response, get_client
from src.utils.logger import logging
from src.config.app_config import ChatbotConfig as cc


class GuardAgent:
    def __init__(self):
        self.client = get_client(
            api_key=cc.RUNPOD_TOKEN,
            url=cc.RUNPOD_URL
        )

        self.model_name = cc.chatbot_model_name
        logging.info('Initialize guard agent ...')
    

    def postprocess(self, output):
        output = json.loads(output)

        dict_output = {
            "role": "assistant",
            "content": output['message'],
            "memory":{
                "agent": "guard_agent",
                "guard_decision": output['decision']
            }
        }

        return dict_output


    def get_response(self, messages):
        messages = deepcopy(messages)

        system_prompt = """
            You are a helpful AI assistant for a coffee shop application which serves drinks and pastries.
            Your task is to determine whether the user is asking something relevant to the coffee shop or not.
            The user is allowed to:
            1. Ask questions about the coffee shop, like location, working hours, menu items and coffee shop related questions.
            2. Ash questions about menu items, they can ask for ingredients in an item and more details about the item.
            3. Make an order.
            4. Ask about recommendations of what to buy

            The user is not allowed to:
            1. Ask questions about anything else other than our coffee shop.
            2. Ask questions about the staff or how to make a certain menu item.

            Your output must be in structured json format like this below. Each key is a string and each value is a string. Make sure to follow the format strictly:
            {
            "chain of thought": go over each of the points above and let see if the message lies under this point or not. Then you write some of your thoughts about what point is this input relevant to. ,
            "decision": "allowed" or "not allowed". Pick one of those and only write the word. ,
            "message": leave the message empty if it's allowed, otherwise write "Sorry, I can't help you with that. May I help you with your order ?"
            }
            """

        input_messages = [{'role': "system", "content": system_prompt}] + messages[-3:]

        chatbot_output = get_chat_response(
            client=self.client,
            model_name=self.model_name,
            messages=input_messages
        )

        logging.info(f'-----------------------------{chatbot_output}')

        output = self.postprocess(output=chatbot_output)

        return output

