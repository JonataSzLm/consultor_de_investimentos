# 🤖 Warren Bot: Seu Companheiro de Investimentos Inteligente 📈

## ✨ Apresentação do Projeto

Bem-vindo ao Guardião Financeiro AI! Este projeto, desenvolvido como parte da **Imersão IA 2025 da Alura e Google**, é um consultor de investimentos inteligente construído para tornar o mundo financeiro mais acessível e compreensível para você. Utilizando o poder da Inteligência Artificial e uma arquitetura de múltiplos agentes, nossa aplicação guia o usuário desde a definição do seu perfil de investidor até a sugestão de um portfólio e a simulação de cenários futuros.

## 💡 O Problema que Resolvemos

Investir pode parecer complicado e intimidador para muitas pessoas. A falta de conhecimento, a vasta quantidade de informações e a incerteza sobre por onde começar são barreiras significativas. O Guardião Financeiro AI busca quebrar essas barreiras, oferecendo uma consultoria inicial personalizada e educativa, adaptada ao seu perfil e objetivos.

## 🧠 Nossa Solução: Uma Orquestra de Agentes IA

Nosso projeto implementa um sistema de múltiplos agentes de IA, cada um com uma função especializada no processo de consultoria. A interação acontece através de uma interface gráfica intuitiva, onde o fluxo da conversa é guiado pelo backend inteligente:

1.  **Definição do Perfil (Agente 1: Atendente):** Uma conversa inicial para entender seus objetivos, tolerância a risco e situação financeira. 🗣️
2.  **Análise e Sugestão (Agentes 2, 3, 4: Analista Financeiro, Sugestor de Portfólio, Educador Financeiro):** Uma vez que seu perfil é compreendido, o sistema realiza uma análise "nos bastidores" para sugerir um portfólio adequado e apresentar essa sugestão de forma clara e educativa. 📊 advisors.
3.  **Simulação e Dúvidas (Agente 5: Especialista em Simulação):** Após receber a sugestão, você pode interagir livremente, fazer perguntas detalhadas sobre a proposta ou simular como o portfólio se comportaria em diferentes cenários de mercado. 🔮

## ✅ Funcionalidades Chave

* **Coleta Interativa de Perfil:** Diálogo guiado para entender suas necessidades financeiras.
* **Análise Financeira Automatizada:** Processamento de informações para identificar tipos de investimentos relevantes.
* **Sugestão de Portfólio Personalizado:** Recomendação de alocação de ativos baseada no seu perfil e na análise.
* **Apresentação Clara e Didática:** Explicação detalhada da sugestão de forma compreensível.
* **Chat de Simulação:** Interaja com o Agente 5 para explorar cenários e tirar dúvidas aprofundadas.
* **Persistência de Dados:** Todo o perfil e a análise/sugestão completa são salvos e carregados, permitindo retomar a conversa e as simulações. 💾
* **Interface Gráfica Amigável:** Aplicação desktop simples e intuitiva (construída com Tkinter/ttk). ✨

## ⚙️ Como Funciona por Trás das Câmeras

O coração do Guardião Financeiro AI é a orquestração dos agentes de IA. Utilizamos conceitos da **Aula 05 ("Construindo agentes que resolvem tarefas por você")** da Imersão IA, onde um backend controla o fluxo da conversa através de um sistema de estados. O input do usuário é roteado para o agente apropriado (Agente 1 durante o perfilamento, Agente 5 durante o chat de simulação), e as respostas e dados gerados pelos Agentes 1, 2, 3 e 4 são encadeados e persistidos para uso futuro.

## 🏆 Alinhamento com os Critérios de Avaliação

Nosso projeto foi cuidadosamente elaborado para atender aos critérios da Imersão IA 2025:

* **Utilidade:** Oferece um serviço prático de consultoria financeira inicial e educação. 🤝
* **Criatividade:** A arquitetura multi-agente com um fluxo de estado gerenciado para uma tarefa complexa demonstra uma aplicação criativa dos conceitos de agentes. A persistência de todos os dados gerados para contexto futuro é um diferencial. 💡
* **Eficácia:** O objetivo é fornecer sugestões relevantes e respostas úteis baseadas no input do usuário e na simulação (mesmo que baseada em modelos simplificados para o projeto). ✅
* **Apresentação:** A interface gráfica (GUI) oferece uma forma clara e interativa para o usuário se comunicar com os agentes, com feedback visual do progresso e identificação dos agentes. ✨

## 💻 Tecnologias Utilizadas

* **Python:** Linguagem de programação principal.
* **Google AI SDK:** Para a criação e orquestração dos agentes de IA.
* **Tkinter / ttk:** Para a construção da interface gráfica do usuário.
* **python-dotenv:** Para o gerenciamento de variáveis de ambiente (como API keys).
* **json:** Para o tratamento de dados JSON.

## 🚀 Como Rodar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd guardiao-financeiro-ai # Ou o nome da pasta do seu projeto
    ```
2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate # No Windows, use `venv\Scripts\activate`
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    (Certifique-se de criar um arquivo `requirements.txt` com as bibliotecas necessárias: `google-generativeai`, `google-cloud-aiplatform`, `python-dotenv`, etc., dependendo da sua implementação exata do Google AI SDK).
4.  **Configure sua API Key do Google AI:** Crie um arquivo `.env` na raiz do projeto com o conteúdo:
    ```dotenv
    GOOGLE_API_KEY=SUA_API_KEY_AQUI
    ```
5.  **Crie a pasta de instruções:** Crie uma pasta chamada `instructions` na raiz do projeto.
    ```bash
    mkdir instructions
    ```
6.  **Adicione os arquivos de instrução:** Coloque os arquivos `.txt` com as instruções dos seus agentes (ex: `profile.txt`, `analyst.txt`, `suggestor.txt`, `detailed.txt`, `simulator.txt`) dentro da pasta `instructions`.
7.  **Execute a aplicação:**
    ```bash
    python main.py
    ```

A janela da aplicação deverá abrir, e a conversa com o consultor AI será iniciada.

## 🌟 Melhorias Futuras (Ideias!)

* Integração com APIs de dados financeiros reais para análises mais precisas.
* Simulações mais complexas considerando fatores como impostos, taxas, e contribuições regulares.
* Visualização gráfica dos resultados das simulações (usando Matplotlib ou outra biblioteca).
* Interface web em vez de desktop GUI para maior acessibilidade.
* Expansão dos tipos de investimentos considerados e das análises realizadas.

## 👋 Agradecimentos

Este projeto foi possível graças aos conhecimentos adquiridos na **Imersão IA 2025 da Alura e Google**. Agradecemos a oportunidade de explorar o desenvolvimento com modelos de IA e agentes.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---
