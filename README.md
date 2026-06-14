# Otimização e Avaliação de Prompts (Bug to User Story)

Este projeto implementa uma pipeline completa para fazer o pull de prompts de baixa qualidade do LangSmith Prompt Hub, otimizá-los localmente usando técnicas avançadas de Prompt Engineering, reenviá-los ao Hub e avaliar sua qualidade contra um dataset de teste através do LangSmith (utilizando IA-como-juiz).

---

## 1. Como Executar o Projeto

### Pré-requisitos e Dependências
- **Python**: Versão 3.9 ou superior.
- **API Keys**: Uma API Key do LangSmith (obrigatório) e uma API Key do LLM de sua escolha (OpenAI ou Google Gemini).
- **Variáveis de Ambiente**: Recomenda-se atualizar e utilizar o arquivo `.env.example` (renomeado para `.env`) configurando as suas chaves de acesso conforme o modelo abaixo:

```ini
# LangSmith Configuration
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=sua_chave_langsmith_aqui
LANGSMITH_PROJECT=prompt-optimization-challenge-resolved
USERNAME_LANGSMITH_HUB=seu_username_langsmith_hub_aqui

# LLM Providers (Escolha 'google' ou 'openai')
LLM_PROVIDER=google
GOOGLE_API_KEY=sua_chave_gemini_aqui
LLM_MODEL=gemini-2.5-flash
EVAL_MODEL=gemini-2.5-flash
```

### Configuração do Ambiente Virtual
Crie e ative o ambiente virtual para gerenciar de forma isolada as dependências do projeto:

```bash
# Criar o virtualenv
python3 -m venv venv

# Ativar no macOS/Linux:
source venv/bin/activate

# Ativar no Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Instalar dependências necessárias
pip install -r requirements.txt
```

### Comandos para cada Fase do Projeto

- **Fase 1: Fazer pull do prompt v1 (baixo desempenho) do Hub**
  ```bash
  python src/pull_prompts.py
  ```
  *Baixa o prompt original `leonanluppi/bug_to_user_story_v1` do LangSmith Hub e salva localmente em `prompts/bug_to_user_story_v1.yml`.*

- **Fase 2: Otimizar o prompt localmente**
  *O prompt otimizado v2 é armazenado em `prompts/bug_to_user_story_v2.yml` aplicando técnicas avançadas.*

- **Fase 3: Fazer push do prompt otimizado v2 para o seu Hub público**
  ```bash
  python src/push_prompts.py
  ```
  *Valida localmente o prompt e faz push para a sua conta do LangSmith Hub sob o nome `{seu_username}/bug_to_user_story_v2`.*

- **Fase 4: Executar a suíte de testes de validação local**
  ```bash
  pytest tests/test_prompts.py
  ```
  *Executa os testes estáticos que validam as regras estruturais e de negócio do prompt (persona, Few-shot, ausência de TODOs, etc.).*

- **Fase 5: Executar a avaliação completa contra os 15 exemplos do Dataset no LangSmith**
  ```bash
  python src/evaluate.py
  ```
  *Roda os testes de avaliação usando IA-como-juiz, computa as métricas de qualidade e envia os logs para o seu dashboard do LangSmith.*

---

## 2. Técnicas Aplicadas

Na otimização do prompt `bug_to_user_story_v2`, foram aplicadas as seguintes técnicas avançadas de Prompt Engineering:

1. **Few-shot Learning (Aprendizado com Poucos Exemplos - Obrigatório)**:
   - **Justificativa**: É a técnica mais eficiente para treinar o LLM no formato de saída esperado. Alinha a estrutura e granularidade das User Stories e Critérios de Aceitação com o gabarito das referências, garantindo notas altas de F1-Score e Recall.
   - **Aplicação**: Foram fornecidos 3 exemplos de entrada/saída cobrindo os níveis de complexidade do dataset: *Simples*, *Médio* e *Complexo*.

2. **Role Prompting (Persona e Contexto Detalhado)**:
   - **Justificativa**: Ajusta a postura e o vocabulário técnico do modelo para responder como um Product Owner profissional, focando em empatia ao usuário e valor real de negócio.
   - **Aplicação**: O modelo foi instruído como um *Principal Technical Product Manager (TPM) e Product Owner (PO) sênior especialista em metodologias ágeis e resolução de débitos técnicos*.

3. **Chain of Thought (CoT - Pensamento Passo a Passo)**:
   - **Justificativa**: A análise de bugs complexos requer a identificação sistemática da persona, causa-raiz, complexidade e critérios técnicos. O raciocínio passo a passo previne a omissão de detalhes importantes.
   - **Aplicação**: Instrução de "Chain of Thought Interno" orientando o modelo a realizar 5 etapas lógicas de análise mentalmente antes de começar a responder.

4. **Diretrizes Anti-Alucinação e Restrições de Formato**:
   - **Justificativa**: Garante que o modelo não invente logs, IDs ou caminhos, o que comprometeria a métrica de *Precision*.
   - **Aplicação**: Regras estritas de formatação (impedindo cabeçalhos conversacionais extras e delimitações de código markdown desnecessárias no output final) e de preservação de dados técnicos originais.

---

## 3. Resultados Finais

> [!NOTE]
> Os valores abaixo são placeholders e devem ser preenchidos após a execução da avaliação do prompt v2 em sua própria conta do LangSmith.

### Tabela Comparativa de Desempenho

| Métrica | Baseline (v1) | Prompt Otimizado (v2) | Limite Mínimo | Status |
| :--- | :---: | :---: | :---: | :---: |
| **Helpfulness** | [Valor v1] | **[Valor v2]** | 0.80 | [Pendente] |
| **Correctness** | [Valor v1] | **[Valor v2]** | 0.80 | [Pendente] |
| **F1-Score** | [Valor v1] | **[Valor v2]** | 0.80 | [Pendente] |
| **Clarity** | [Valor v1] | **[Valor v2]** | 0.80 | [Pendente] |
| **Precision** | [Valor v1] | **[Valor v2]** | 0.80 | [Pendente] |

### Evidências no LangSmith
- **Link público do dashboard:** `[INSIRA O LINK PÚBLICO DO SEU PROJETO NO LANGSMITH AQUI]`
- **Prints do Dashboard e Tracing:** `[INSIRA OS PRINTS DE TELA COMPROVANDO AS MÉTRICAS DE AVALIAÇÃO E O TRACING DETALHADO DO LANGSMITH AQUI]`
