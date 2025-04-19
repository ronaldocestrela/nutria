# from settings import OPENAI_API_KEY

from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType

from dotenv import load_dotenv
import os

from chat.memory import SqliteMemory
from tools import (
    ImageFoodAnalyzerTool,
    DietPlanTool,
    # MealEntryTool,
    # ReportTool,
    UserRegistrationTool,
    # WeightUpdateTool,
    UserInfoTool
    )

load_dotenv()

SYSTEM_PROPT = """
    Backstory:
        Esse agente é uma referência global no campo da nutrição, apelidado de “Mestre dos Alimentos” ou o “Nutrólogo Supremo”. 
        Consultado por celebridades, atletas e profissionais de saúde, ele desenvolve planos alimentares personalizados, equilibrando saúde, desempenho e sustentabilidade. 
        Com vasto conhecimento em bioquímica e dietas globais (como a mediterrânea, cetogênica e ayurvédica), é defensor do consumo consciente e da preservação ambiental. 
        Agora, ele expande sua expertise para o mundo digital, oferecendo orientação de alta qualidade pelo Telegram para ajudar pessoas a montarem suas próprias dietas e responder dúvidas sobre alimentação.

        Expected Result:
        O agente deve ter um visual que una sua autoridade com a acessibilidade de um consultor digital. 
        Seu entorno deve mostrar opiniões de nutrição: informações de nutrientes, alimentos de diversas culturas e elementos químicos, criando um ambiente que pareça um “laboratório” virtual de alimentação.
"""

class NutritionistAgent:
    def __init__(self, session_id: str):
        self.session_id = session_id
        
        self.llm = ChatOpenAI(
            model_mame="gpt-4o-mini",
            temperature=0.1,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        )
        
        self.memory = SqliteMemory(session_id).history
        
        self.tools = [
            ImageFoodAnalyzerTool(),
            DietPlanTool(),
            # MealEntryTool(),
            # ReportTool(),
            UserRegistrationTool(),
            # WeightUpdateTool(),
            UserInfoTool()
        ]
        
        self.agent = initialize_agent(
            llm = self.llm,
            tools = self.tools,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory,
            agent_kwargs={'system_message': SYSTEM_PROPT},
        )
        
    def run(self, input_text: str) -> str:
        try:
            response = self.agent.invoke(input_text)
            return response.get("output")
        except Exception as e:
            print(f"Error: {e}")
            return "Desculpe, ocorreu um erro ao processar sua solicitação. Por favor, tente novamente."