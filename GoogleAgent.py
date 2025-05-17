from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types


class GoogleAgent:
    def __init__(self, name: str, model: str, description: str, instruction: str, search_on_google: bool = False) -> None:
        """
        Inicializa o agente do Google com as informações fornecidas.
        """
        self.agent = MyAgent(
            name=name,
            model=model,
            description=description,
            instruction=instruction,
            search_on_google=search_on_google
        )
        self.session_service = InMemorySessionService()
        self.session = self.session_service.create_session(app_name=self.agent.name, user_id="user1", session_id="session1")
        self.runner = Runner(agent=self.agent, app_name=self.agent.name, session_service=self.session_service)

    def run(self, prompt: str) -> str:
            """
            Executa o agente com o prompt fornecido e retorna a resposta final.
            """
            content = types.Content(role="user", parts=[types.Part(text=f'{prompt}')])

            final_response = ""
            for event in self.runner.run(user_id="user1", session_id="session1", new_message=content):
                if event.is_final_response():
                    for part in event.content.parts:
                        if part.text is not None:
                            final_response += part.text
                            final_response += "\n"
            return final_response


class MyAgent(Agent):
    """
    Classe base para criar agentes personalizados.
    """
    def __init__(self, name: str, model: str, description: str, instruction: str, search_on_google: bool = False) -> None:
        super().__init__(name=name, model=model, description=description, instruction=instruction)
        self.tools = [google_search] if search_on_google else []