import os

from src.utils.logger import logging
from src.modules.agents import (AgentProtocol, 
                                GuardAgent,
                                ClassificationAgent)

def main():
    guard_agent = GuardAgent()
    classification_agent = ClassificationAgent()

    messages = []
    while True:
        # os.system('cls' if os.name == 'nt' else 'clear')
        
        print('----------Print messages----------')
        for message in messages:
            print(f"{message['role'].capitalize()}: {message['content']}")
        
        prompt = input("User: ")
        messages.append({"role": "user", "content": prompt})

        guard_agent_response = guard_agent.get_response(messages)
        if guard_agent_response['memory']['guard_decision'] == 'not_allowed':
            messages.append(guard_agent_response)
            continue

        classification_agent_response = classification_agent.get_response(messages=messages)
        chosen_agent = classification_agent_response['memory']['classification_agent']

        logging.info(f"Chosen Agent: {chosen_agent}")

        messages.append(guard_agent_response)

if __name__ == "__main__":
    main()