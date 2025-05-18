# main.py
# -*- coding: utf-8 -*-
import tkinter as tk
from dotenv import load_dotenv
import warnings
import json
import os

from interface import AgentChatGUI

from GoogleAgent import GoogleAgent
from Profile import InvestorProfile


load_dotenv()
warnings.filterwarnings("ignore", category=UserWarning, module="google.genai")


def read_instructions(instructions_filename) -> str:
    """
    Lê as instruções do arquivo de configuração.
    """
    instructions_path = os.path.join("./instructions", f"{instructions_filename}.txt")
    try:
        with open(instructions_path, "r", encoding='utf-8') as file:
            instructions = file.read()
        return instructions
    except FileNotFoundError:
        print(f"Erro: Arquivo de instrução '{instructions_path}' não encontrado.")
        return f"Erro: Instruções para '{instructions_filename}' não encontradas. O agente pode não se comportar como esperado."

def agent_investor_profile() -> GoogleAgent:
    """
    Cria o agente de perfil do investidor (GoogleAgent wrapper).
    """
    instructions = read_instructions('profile')
    agent = GoogleAgent(
        name="InvestorProfileAgent",
        model="gemini-2.0-flash",
        description="Agente de perfil do investidor.",
        instruction=instructions,
        search_on_google=False
    )
    return agent

def response_is_json(response: str):
    """
    Verifica se a resposta é um JSON válido e retorna o objeto JSON ou None.
    """
    try:
        start_json = response.find("{")
        end_json = response.rfind("}") + 1
        if start_json > -1 and end_json > -1 and end_json > start_json:
            json_string = response[start_json:end_json]
            return json.loads(json_string)
        return None
    except (ValueError, json.JSONDecodeError):
        return None


def agent_analyst_financial() -> GoogleAgent:
     """
     Cria o agente de análise de mercado e produtos financeiros (GoogleAgent wrapper).

     """
     instructions = read_instructions('analyst')
     agent = GoogleAgent(
         name="AnalystFinancialAgent",
         model="gemini-2.0-flash",
         description="Agente de análise de mercado e produtos financeiros.",
         instruction=instructions,
         search_on_google=True
     )
     return agent

def agent_portfolio_suggestor() -> GoogleAgent:
     """
     Cria o agente de análise de mercado e produtos financeiros (GoogleAgent wrapper).

     """
     instructions = read_instructions('suggestor')
     agent = GoogleAgent(
         name="PortfolioSuggestorAgent",
         model="gemini-2.0-flash",
         description="Agente sugestor de portfólio.",
         instruction=instructions,
         search_on_google=True
     )
     return agent

def agent_detailed_analysis() -> GoogleAgent:
     """
     Cria o agente de análise detalhada (GoogleAgent wrapper).

     """
     instructions = read_instructions('detailed')
     agent = GoogleAgent(
         name="DetailedAnalysisAgent",
         model="gemini-2.0-flash",
         description="Agente de análise detalhada.",
         instruction=instructions,
         search_on_google=True
     )
     return agent

def agent_simulator() -> GoogleAgent:
     """
     Cria o agente de simulação (GoogleAgent wrapper).

     """
     instructions = read_instructions('simulator')
     agent = GoogleAgent(
         name="SimulatorAgent",
         model="gemini-2.0-flash",
         description="Agente de simulação.",
         instruction=instructions,
         search_on_google=True
     )
     return agent



def get_investor_profile(user_input: str, profile_agent: GoogleAgent) -> tuple[str, dict]:
    """
    Processa um único turno da conversa de perfil com o agente.
    Retorna a resposta do agente e o dicionário do perfil JSON (ou None).
    """
    response = profile_agent.run(user_input)
    print(f"\nResposta do agente de perfil (turno único):\n{response}\n") # Debug

    profile_data = response_is_json(response)

    return response, profile_data



COMPLETE_DATA_FILEPATH = "complete_investor_data.json"

class AgentBackend:
    def __init__(self, gui_instance: AgentChatGUI):
        self.gui = gui_instance # Referência à instância da GUI
        self.profile_manager = InvestorProfile(COMPLETE_DATA_FILEPATH) # Usamos InvestorProfile para salvar/carregar o arquivo completo

        # --- Criação das Instâncias de GoogleAgent (Uma vez) ---
        self.profile_agent_instance = agent_investor_profile()
        self.analyst_agent_instance = agent_analyst_financial()
        self.suggestor_agent_instance = agent_portfolio_suggestor()
        self.detailed_analysis_agent_instance = agent_detailed_analysis()
        self.simulator_agent_instance = agent_simulator()

        # --- Dados Completos do Investidor ---
        # Esta variável armazenará toda a informação (Perfil, Análise, Sugestão, A4 Response)
        self.complete_investor_data = None

        # --- Estado da Aplicação ---
        # Estados possíveis: 'initial_profiling', 'profile_complete_generating', 'simulation_chat'
        self.current_state = 'initial_profiling'

        # Tenta carregar os dados completos existentes ao iniciar
        self._load_complete_data()

        # Inicia a conversa na GUI com base no estado inicial
        if self.current_state == 'initial_profiling':
            self.gui.append_message("🤖📋 Assistente", "Olá! Eu sou o assistente do Warren Bot.\nVamos começar definindo seu perfil. Por favor, me diga seu nome e idade aproximada.")
        elif self.current_state == 'simulation_chat':
            self.gui.append_message("🤖💼 Warren Bot", "Olá! Eu sou o Warren Bot, o seu consultor de investimentos IA.\nAnalisei suas informações. Posso te ajudar com dúvidas, simulações ou outras análises?")


    def process_user_input(self, user_input: str):
        """
        Callback chamado pela GUI quando o usuário envia uma mensagem.
        Gerencia o fluxo da conversa com base no estado atual.
        """
        print(f"\n--- Backend: Recebeu input no estado '{self.current_state}' ---")
        print(f"Input: '{user_input}'")

        agent_response_text = "Processando..."
        sender = "🤖📋 Assistente"

        try:
            # --- Lógica Baseada no Estado Atual ---
            if self.current_state == 'initial_profiling':
                # Interage com o Agente de Perfil
                # Chama a função modificada get_investor_profile
                profile_response, profile_data = get_investor_profile(user_input, self.profile_agent_instance)
                agent_response_text = profile_response
                

                if profile_data: # Verifica se o JSON do perfil foi detectado na resposta do A1

                    # Muda o estado para geração da sugestão e executa a sequência A2-A4
                    self.current_state = 'profile_complete_generating'
                    self.gui.receive_agent_response(agent_response_text, "🤖📋 Assistente")

                    # 1. Chamar o Agente Analista (A2) com o perfil
                    self.gui.receive_agent_response("Enviei seu perfil para nosso análista financeiro.\nPor favor aguarde...", "🤖📋 Assistente")
                    # Passamos o perfil diretamente como input JSON para o Analista.
                    analyst_input_json = json.dumps({"perfil_investidor": profile_data, "tarefa": "Analise o mercado e produtos adequados."})
                    analyst_response_text = self.analyst_agent_instance.run(analyst_input_json)
                    print(f"Resposta Agente A2:\n{analyst_response_text}")

                    # 2. Chamar o Agente Sugestor (A3) com o resultado da análise
                    self.gui.receive_agent_response("Análise completa!\nAgora nosso time está levantando algumas sugestões para você.\nPor favor aguarde...", "🤖📋 Assistente")
                    # Passamos o perfil e a resposta textual do Analista como input para o Sugestor.
                    suggestor_input = {"perfil_investidor": profile_data, "analise_mercado_resposta": analyst_response_text, "tarefa": "Gere uma sugestão de portfólio com alocação de ativos."}
                    suggestor_response_text = self.suggestor_agent_instance.run(json.dumps(suggestor_input))
                    print(f"Resposta Agente A3:\n{suggestor_response_text}")
                    suggestor_suggestion_json = response_is_json(suggestor_response_text) # Tenta extrair JSON da sugestão

                    # 3. Chamar o Agente de Análise Detalhada (A4) com a sugestão e perfil
                    self.gui.receive_agent_response("Sugestões levantadas!\nAgora vamos analisar detalhadamente as sugestões.\nPor favor aguarde...", "🤖📋 Assistente")
                    # Passamos o perfil, a sugestão (JSON se disponível, texto se não) e a resposta do A3 como contexto para o A4
                    input_for_a4 = {
                         "perfil_investidor": profile_data,
                         "sugestao_portfolio": suggestor_suggestion_json if suggestor_suggestion_json else suggestor_response_text,
                         "tarefa": "Apresente esta sugestão de portfólio para o usuário de forma clara e didática.",
                         "resposta_agente_3_original": suggestor_response_text # Incluir a resposta textual original do A3 pode ser útil
                    }
                    a4_response_text = self.detailed_analysis_agent_instance.run(json.dumps(input_for_a4))
                    print(f"Resposta Agente A4:\n{a4_response_text}")

                    # --- Armazena TODOS os dados no objeto completo ---
                    self.complete_investor_data = {
                        "profile": profile_data,
                        "analyst_response_a2": analyst_response_text,
                        "suggestor_response_a3": suggestor_response_text,
                        "suggestion_json_a3": suggestor_suggestion_json,
                        "detailed_analysis_response_a4": a4_response_text
                    }

                    # --- Salva os dados completos no arquivo ---
                    self._save_complete_data(self.complete_investor_data)

                    # --- Muda o estado para o chat com o Agente 5 ---
                    self.current_state = 'simulation_chat'

                    # A resposta final para o usuário neste turno é a resposta do A4.
                    agent_response_text = a4_response_text
                    
                    sender = "🤖💼 Warren Bot"

                # Se o perfil JSON não foi detectado, a resposta do agente de perfil (A1)
                # já foi definida como agent_response_text no início do bloco.
                # O estado permanece 'initial_profiling'.


            elif self.current_state == 'profile_complete_generating':
                 # Este estado é transitório durante a execução da sequência A2-A4.
                 # Se receber input aqui, significa que o usuário digitou enquanto a sequência rodava.
                 # Neste caso, apenas informa para aguardar.
                 agent_response_text = "[Sistema] Ainda estou finalizando a análise e sugestão. Por favor, aguarde um momento."


            elif self.current_state == 'simulation_chat':
                sender = "🤖💼 Warren Bot"
                # Interage com o Agente de Simulação (A5) para todas as perguntas subsequentes

                # Passamos o input do usuário E os dados completos como contexto para o A5.
                # Isso garante que o Agente 5 sempre tenha as informações de perfil, análise e sugestão.
                # Embora o .run() do GoogleAgent reinicie a sessão, passar o contexto explicitamente
                # ajuda o agente a "lembrar" das informações relevantes a cada turno no modo Simulação.
                input_for_a5 = {
                     "solicitacao_usuario": user_input,
                     "dados_completos_investidor": self.complete_investor_data # Passa todos os dados
                 }
                input_for_a5_string = json.dumps(input_for_a5)
                agent_response_text = self.simulator_agent_instance.run(input_for_a5_string)
                print(f"Resposta Agente A5:\n{agent_response_text}")


            else:
                agent_response_text = "Estado da aplicação desconhecido. Por favor, reinicie."


        except Exception as e:
             agent_response_text = f"Desculpe, ocorreu um erro interno: {e}"
             # Em caso de erro, talvez você queira resetar o estado ou dar opções ao usuário
             # self.current_state = 'initial_profiling' # Exemplo: voltar para o início


        # --- Envia a resposta de volta para a GUI ---
        # Esta chamada acontece APÓS o processamento do turno e, se aplicável, a sequência A2-A4.
        self.gui.receive_agent_response(agent_response_text, sender)


    def _save_complete_data(self, data):
         """Salva o objeto de dados completos em um arquivo JSON usando InvestorProfile."""
         try:
             # Usa a instância do gerenciador de perfil que aponta para o arquivo de dados completos
             self.profile_manager.save_profile_to_file(data)
         except Exception as e:
             print(f"Backend: Erro ao salvar dados completos usando InvestorProfile: {e}")

    def _load_complete_data(self):
         """Tenta carregar os dados completos existentes ao iniciar o backend."""
         try:
             # Usa a instância do gerenciador de perfil para carregar do arquivo de dados completos
             loaded_data = self.profile_manager.load_profile_from_file() # InvestorProfile.load_profile_from_file retorna o conteúdo ou None

             # Verifica se os dados carregados parecem ser os dados completos esperados
             if loaded_data and isinstance(loaded_data, dict) and "profile" in loaded_data and "detailed_analysis_response_a4" in loaded_data:
                 self.complete_investor_data = loaded_data
                 # Se dados completos foram carregados, o estado inicial é 'simulation_chat'
                 self.current_state = 'simulation_chat'
             else:
                 # Se não encontrar dados completos ou o formato for inesperado, estado inicial é 'initial_profiling'
                 self.current_state = 'initial_profiling'
         except Exception as e:
             print(f"Backend: Erro ao carregar dados completos existentes: {e}")
             # Mesmo com erro ao carregar, o estado inicial deve ser 'initial_profiling'
             self.current_state = 'initial_profiling'


# --- Execução Principal da Aplicação ---

if __name__ == "__main__":
    print("Iniciando aplicação de Consultor de Investimentos IA...")
    # Cria a janela principal da GUI
    root = tk.Tk()

    # Cria a instância da GUI
    gui = AgentChatGUI(root)

    # Cria a instância do backend, passando a instância da GUI para ele
    # O backend gerencia a lógica dos agentes e o estado da conversa
    backend = AgentBackend(gui)

    # Conecta o callback da GUI ao método de processamento do backend
    # Agora, quando a GUI recebe um input, ela chama backend.process_user_input
    gui.on_message_sent_callback = backend.process_user_input

    # A mensagem inicial para o usuário é enviada pelo backend em __init__
    # após verificar se um perfil existente foi carregado.

    # Inicia o loop principal da interface gráfica
    # Este loop mantém a janela aberta e responsiva.
    root.mainloop()

    print("Aplicação finalizada.")