from src.modules.agents import(
    GuardAgent,
    ClassificationAgent,
    DetailAgent,
    RecommendationAgent,
    OrderTakingAgent,
    AgentProtocol
)

class AgentController():
    def __init__(self):
        self.guard_agent = GuardAgent()
        self.classification_agent = ClassificationAgent()
        self.recommendation_agent = RecommendationAgent()
        self.agent_dict: dict[str, AgentProtocol] = {
            "detail_agents": DetailAgent(),
            "order_taking_agents": OrderTakingAgent(self.recommendation_agent),
            "recommendation_agents": self.recommendation_agent
        }

    def get_response(self, input):
        job_input = input['input']
        messages = job_input['messages']

        guard_agent_response = self.guard_agent.get_response(messages=messages)
        if guard_agent_response['memory']['guard_decision'] == 'not_allowed':
            return guard_agent_response
        
        classification_response = self.classification_agent.get_response(messages=messages)
        chosen_agent = classification_response['memory']['classification_decision']

        agent = self.agent_dict[chosen_agent]

        response = agent.get_response(message=messages)

        return response



