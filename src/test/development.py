import os

from src.modules.agents import (AgentProtocol, 
                                GuardAgent)

def main():
    guard_agent = GuardAgent()

    messages = []
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print('----------Print messages----------')
        for message in messages:
            print(f"{message['role'].capitalize()}: {message['content']}")
        
        prompt = input("User: ")
        messages.append({"role": "user", "content": prompt})

        guard_agent_response = guard_agent.get_response(messages)

        print(f"Response: {guard_agent_response}")

        print(f'Guard Agent: {guard_agent_response['content']}\nDecision: {guard_agent_response['memory']['guard_decision']}')

        messages.append(guard_agent_response)

if __name__ == "__main__":
    main()