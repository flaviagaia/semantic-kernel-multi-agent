# Multi-Agent Pipeline with Semantic Kernel — Sequential Orchestration

[🇧🇷 Português](#-português) · [🇺🇸 English](#-english)

Python · Semantic Kernel ≥ 1.43 (Agent Framework) · OpenAI / Azure OpenAI

---

## 🇧🇷 Português

### Visão geral

Pipeline multi-agente sobre o framework de agentes do [Semantic Kernel](https://github.com/microsoft/semantic-kernel):

- **`ChatCompletionAgent`** — agentes com `instructions`, `description` e serviço de chat próprios. Cada agente encapsula um papel, com limites e critérios de qualidade independentes.
- **`SequentialOrchestration`** — topologia declarativa em que a saída de um agente é a entrada do próximo. A orquestração é um grafo de mensagens, não código imperativo.
- **`InProcessRuntime`** — runtime de atores que agenda a troca de mensagens entre agentes no mesmo processo. O mesmo modelo de programação escala para runtimes distribuídos.
- **`agent_response_callback`** — hook de observabilidade invocado a cada mensagem produzida. Em produção, é o ponto de acoplamento para logging estruturado, métricas de token/latência por etapa e trilha de auditoria.

### Arquitetura

```
TAREFA (fatos numéricos brutos)
  │
  ▼
📊 analista  ── rascunho técnico (números + contexto)
  │                    │ callback → log/auditoria
  ▼
🔍 revisor   ── verificação de números, riscos, inconsistências
  │                    │ callback → log/auditoria
  ▼
✍️ editor    ── resumo executivo final (≤ 3 parágrafos)
  │
  ▼
OrchestrationResult.get(timeout=120)
```

### Por que decompor em vez de um prompt único

Um prompt monolítico que "analisa, revisa e edita" tem três modos de falha indistinguíveis. A decomposição traz propriedades de engenharia:

- **Auditabilidade** — a saída intermediária de cada papel é inspecionável; o callback materializa o estado entre etapas.
- **Isolamento de falha** — degradação de qualidade é localizável em uma etapa específica.
- **Substituibilidade** — cada agente pode trocar de modelo (ex.: revisor com modelo mais forte) ou de instruções sem afetar os demais.
- **Princípio adversarial** — o revisor tem instruções explícitas para criticar o analista, padrão que reduz erros de propagação acrítica.

### Outras topologias com o mesmo código

`ConcurrentOrchestration` (fan-out paralelo), `GroupChatOrchestration` (debate mediado por um chat manager) e `HandoffOrchestration` (transferência dinâmica de controle). A escolha da topologia é configuração, não reescrita.

### Execução

```bash
pip install -r requirements.txt
cp .env.example .env   # OPENAI_API_KEY
python src/main.py
```

---

## 🇺🇸 English

### Overview

Multi-agent pipeline built on the [Semantic Kernel](https://github.com/microsoft/semantic-kernel) agent framework:

- **`ChatCompletionAgent`** — agents with their own `instructions`, `description` and chat service. Each agent encapsulates one role, with independent constraints and quality criteria.
- **`SequentialOrchestration`** — a declarative topology where each agent's output becomes the next agent's input. Orchestration is a message graph, not imperative glue code.
- **`InProcessRuntime`** — an actor runtime that schedules message passing between agents within the same process. The same programming model scales to distributed runtimes.
- **`agent_response_callback`** — an observability hook invoked on every produced message. In production this is the attachment point for structured logging, per-stage token/latency metrics and audit trails.

### Architecture

```
TASK (raw numeric facts)
  │
  ▼
📊 analyst   ── technical draft (numbers + context)
  │                    │ callback → log/audit
  ▼
🔍 reviewer  ── number verification, risks, inconsistencies
  │                    │ callback → log/audit
  ▼
✍️ editor    ── final executive summary (≤ 3 paragraphs)
  │
  ▼
OrchestrationResult.get(timeout=120)
```

### Why decompose instead of one mega-prompt

A monolithic prompt that "analyzes, reviews and edits" has three indistinguishable failure modes. Decomposition buys engineering properties:

- **Auditability** — each role's intermediate output is inspectable; the callback materializes inter-stage state.
- **Failure isolation** — quality degradation is traceable to a specific stage.
- **Swappability** — any agent can change model (e.g., a stronger model for the reviewer) or instructions without touching the others.
- **Adversarial principle** — the reviewer is explicitly instructed to challenge the analyst, a pattern that reduces uncritical error propagation.

### Other topologies, same code

`ConcurrentOrchestration` (parallel fan-out), `GroupChatOrchestration` (debate mediated by a chat manager) and `HandoffOrchestration` (dynamic control transfer). Topology choice is configuration, not a rewrite.

### Running

```bash
pip install -r requirements.txt
cp .env.example .env   # OPENAI_API_KEY
python src/main.py
```

---

Part of my LinkedIn series on Semantic Kernel → [Flávia Gaia](https://www.linkedin.com/in/flavia-gaia/)
