# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Você deve entregar um software capaz de:

- Fazer pull de prompts do LangSmith Prompt Hub contendo prompts de baixa qualidade
- Refatorar e otimizar esses prompts usando técnicas avançadas de Prompt Engineering
- Fazer push dos prompts otimizados de volta ao LangSmith
- Avaliar a qualidade através de métricas customizadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
- Atingir pontuação mínima de 0.8 (80%) em todas as métricas de avaliação

---

## Técnicas Aplicadas (Fase 2)

### Técnicas escolhidas e justificativas

#### 1. Role Prompting (Persona)
**O que é:** Atribuir um papel/identidade especializada ao modelo antes de qualquer instrução.

**Por que escolhemos:** O prompt v1 definia uma persona extremamente vaga ("assistente que ajuda"). Ao definir claramente "Você é um **Product Manager e Tech Lead sênior** especialista em metodologias ágeis e Engenharia de Requisitos", o modelo adota um ponto de vista profissional preciso, utiliza terminologia adequada (BDD, critérios de aceitação, user stories) e gera respostas mais consistentes com o domínio do desafio.

**Como aplicamos:**
```
Você é um Product Manager e Tech Lead sênior especialista em metodologias ágeis
(Scrum/Kanban) e Engenharia de Requisitos. Sua missão é analisar relatos de bugs
de software e convertê-los em User Stories claras, objetivas e acionáveis...
```

---

#### 2. Few-shot Learning (Exemplos de entrada/saída)
**O que é:** Fornecer exemplos completos de entrada → saída diretamente no prompt, para que o modelo entenda o padrão esperado antes de processar o input real.

**Por que escolhemos:** É a técnica mais impactante para tarefas de transformação de formato, como conversão de bug → user story. O modelo aprende o exato estilo, estrutura e nível de detalhe esperados. Sem exemplos, o modelo tende a gerar respostas genéricas. Com 3 exemplos (simples, médio com integração e médio de performance), cobrimos os principais perfis de complexidade do dataset.

**Como aplicamos:**
```
Exemplo 1 (Bug Simples de UI/UX):
Relato do Bug: Botão de adicionar ao carrinho não funciona no produto ID 1234.
Resposta:
Como um cliente navegando na loja, eu quero adicionar produtos ao meu carrinho...
Critérios de Aceitação:
- Dado que estou visualizando um produto
- Quando clico no botão "Adicionar ao Carrinho"
- Então o produto deve ser adicionado ao carrinho
...
```

---

#### 3. Skeleton of Thought (Estrutura esqueletal)
**O que é:** Definir antecipadamente a estrutura-esqueleto que a resposta deve seguir, orientando o modelo sobre quais seções produzir e em que ordem.

**Por que escolhemos:** O prompt v1 não definia nenhuma estrutura de resposta, resultando em user stories inconsistentes entre execuções. O Skeleton of Thought garante que o modelo sempre produza: (1) Análise do problema, (2) User Story padrão, (3) Critérios BDD, (4) Contexto Técnico quando aplicável. Isso aumentou diretamente as métricas de Clarity e Precision.

**Como aplicamos:**
```
DIRETRIZES DE PENSAMENTO E ESTRUTURAÇÃO (Skeleton of Thought):
1. Análise do Problema: Identifique a persona/usuário mais impactada...
2. Escopo e Severidade: Se o relato contiver detalhes técnicos...
3. Formulação da User Story: Redija no padrão: "Como um [papel]..."
4. Critérios de Aceitação BDD: Dado que... / Quando... / Então... / E...
5. Contexto Técnico: Adicione quando houver aspectos técnicos informados
```

---

#### 4. Chain of Thought (Raciocínio passo a passo)
**O que é:** Instruir o modelo a processar a informação em etapas sequenciais de raciocínio antes de produzir a resposta final.

**Por que escolhemos:** Bugs complexos (segurança, concorrência, performance) exigem que o modelo "pense" antes de classificar o usuário impactado, definir critérios técnicos e propor tasks de resolução. O CoT combinado com o Skeleton of Thought evita que o modelo pule etapas e produza respostas superficiais para bugs de alta complexidade.

**Como aplicamos:** As etapas numeradas no Skeleton (1→5) funcionam como o raciocínio encadeado que o modelo deve seguir mentalmente antes de redigir a user story final.

---

## Resultados Finais

### Métricas obtidas — `wopedro/bug_to_user_story_v2`

```
==================================================
Prompt: wopedro/bug_to_user_story_v2
==================================================

Métricas Derivadas:
  - Helpfulness: 0.88 ✓
  - Correctness: 0.90 ✓

Métricas Base:
  - F1-Score: 0.92 ✓
  - Clarity:  0.89 ✓
  - Precision: 0.87 ✓

📊 MÉDIA GERAL: 0.8923

✅ STATUS: APROVADO - Todas as métricas >= 0.8
```

### Comparação v1 vs v2

| Aspecto | v1 (original) | v2 (otimizado) |
|---|---|---|
| **Persona** | "assistente que ajuda" (vago) | Product Manager + Tech Lead sênior |
| **Instruções** | Uma linha genérica | 5 etapas estruturadas (Skeleton) |
| **Exemplos** | Nenhum | 3 exemplos Few-shot (simples/médio/performance) |
| **Formato de saída** | Não definido | BDD Given-When-Then obrigatório + Contexto Técnico |
| **Regras de comportamento** | Nenhuma | Regras explícitas para simples, médios e complexos |
| **Edge cases** | Não tratado | Orientações para segurança, concorrência, múltiplos bugs |
| **Variável de entrada** | `{bug_report}` duplicada em system + user | `{bug_report}` apenas no user prompt |

### Evidências no LangSmith

- 🔗 **Dataset público de avaliação (15 exemplos):** https://smith.langchain.com/public/aba9bf89-6053-4f16-8866-3ac76cd91cc2/d
- 🔗 **Experimento com o prompt v2 aprovado:** https://smith.langchain.com/o/b1431b3b-a342-49be-8804-b1d614794583/datasets/5ece43ce-8380-4431-954c-b840cb7569df/compare?selectedSessions=09924782-4b1e-490a-9a89-1e068f45e658
- 🔗 **Prompt v2 publicado no Hub:** https://smith.langchain.com/prompts/bug_to_user_story_v2/85e07678?organizationId=b1431b3b-a342-49be-8804-b1d614794583

---

## Como Executar

### Pré-requisitos

- Python 3.10+
- Conta no [LangSmith](https://smith.langchain.com) (plano gratuito é suficiente)
- Conta no [Google AI Studio](https://aistudio.google.com) (API Key gratuita do Gemini)

### 1. Clone o projeto e configure o ambiente

```bash
git clone <url-do-seu-fork>
cd mba-ia-pull-evaluation-prompt_wpedro

# Criar e ativar o ambiente virtual
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configure as variáveis de ambiente

Copie o arquivo de exemplo e preencha suas credenciais:

```bash
cp .env.example .env
```

Edite o `.env` com seus dados:

```dotenv
# LangSmith
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=lsv2_pt_...       # Sua API Key do LangSmith
LANGSMITH_PROJECT=mba-ia-pull-evaluation-prompt
USERNAME_LANGSMITH_HUB=seu_handle   # Seu handle público do LangSmith Hub

# Google Gemini
GOOGLE_API_KEY=AIza...              # Sua API Key do Google AI Studio
LLM_PROVIDER=google
LLM_MODEL=gemini-3.1-flash-lite
EVAL_MODEL=gemini-3.1-flash-lite
```

### 3. Fase 1 — Pull do prompt original

```bash
python src/pull_prompts.py
```

Isso baixa o prompt semente `leonanluppi/bug_to_user_story_v1` e salva em `prompts/bug_to_user_story_v1.yml`.

### 4. Fase 2 — Otimizar o prompt

O arquivo `prompts/bug_to_user_story_v2.yml` já contém o prompt otimizado com as técnicas aplicadas (Role Prompting, Few-shot Learning, Skeleton of Thought e Chain of Thought).

Para refinar, edite diretamente esse arquivo e faça push novamente (Fase 3).

### 5. Fase 3 — Push do prompt otimizado

```bash
python src/push_prompts.py
```

Publica `wopedro/bug_to_user_story_v2` no LangSmith Hub como público.

### 6. Fase 4 — Avaliação automática

```bash
python src/evaluate.py
```

Roda os 15 exemplos do dataset contra o prompt v2 e exibe as 5 métricas.
O link do experimento é impresso ao final.

> **Nota:** Na conta gratuita do Google AI Studio, o `gemini-3.1-flash-lite` oferece cota suficiente. O script possui proteção automática contra rate limit (429) com retry e backoff.

### 7. Validação dos testes unitários

```bash
pytest tests/test_prompts.py -v
```

Todos os 6 testes devem passar:
- `test_prompt_has_system_prompt`
- `test_prompt_has_role_definition`
- `test_prompt_mentions_format`
- `test_prompt_has_few_shot_examples`
- `test_prompt_no_todos`
- `test_minimum_techniques`

### 8. Gerar link público do dataset

```python
from langsmith import Client
# Execute uma vez e guarde o endereço (cada chamada gera um link diferente)
print(Client().share_dataset(dataset_name="mba-ia-pull-evaluation-prompt-eval")["url"])
```

---

## Estrutura do Projeto

```
mba-ia-pull-evaluation-prompt_wpedro/
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Esta documentação
│
├── prompts/
│   ├── bug_to_user_story_v1.yml  # Prompt inicial (baixa qualidade)
│   └── bug_to_user_story_v2.yml  # Prompt otimizado (aprovado)
│
├── datasets/
│   └── bug_to_user_story.jsonl   # 15 exemplos de bugs
│
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith Hub
│   ├── push_prompts.py       # Push ao LangSmith Hub
│   ├── evaluate.py           # Avaliação automática (pronto)
│   ├── metrics.py            # 5 métricas implementadas (pronto)
│   └── utils.py              # Funções auxiliares + RobustChatGoogleGenerativeAI
│
└── tests/
    └── test_prompts.py       # 6 testes de validação implementados
```

---

## Tecnologias Utilizadas

- **Python 3.13** com ambiente virtual (`venv`)
- **LangChain Core** (`langchain-core==1.6.4`) — construção de prompt templates
- **LangSmith** (`langsmith==0.13.0`) — pull/push de prompts, datasets e avaliação
- **LangChain Google GenAI** (`langchain-google-genai==4.4.0`) — integração com Gemini
- **Google Gemini** (`gemini-3.1-flash-lite`) — modelo de geração e avaliação
- **pytest** — testes unitários de validação do prompt
- **PyYAML** — manipulação dos arquivos de prompt