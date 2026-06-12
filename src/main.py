"""Pipeline multi-agente com Semantic Kernel: analista → revisor → editor.

Cada agente tem um papel claro e a saída de um vira entrada do próximo
(SequentialOrchestration). O callback imprime cada etapa, o que torna
o fluxo observável e auditável.
"""

import asyncio
import os

from dotenv import load_dotenv
from semantic_kernel.agents import ChatCompletionAgent, SequentialOrchestration
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.contents import ChatMessageContent

load_dotenv()

TAREFA = (
    "A área de marketing executou R$ 461.200 de um orçamento de R$ 450.000 "
    "neste trimestre (estouro de 2,5%). As demais áreas estão dentro do orçamento. "
    "Produza um resumo executivo sobre a situação orçamentária para a diretoria."
)


def make_service() -> OpenAIChatCompletion:
    return OpenAIChatCompletion(
        ai_model_id=os.getenv("OPENAI_CHAT_MODEL_ID", "gpt-4o-mini"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )


def build_agents() -> list[ChatCompletionAgent]:
    analista = ChatCompletionAgent(
        name="analista",
        description="Produz o rascunho técnico da análise.",
        instructions=(
            "Você é um analista de dados. Produza um rascunho técnico e objetivo "
            "da análise solicitada, com números e contexto. Não floreie."
        ),
        service=make_service(),
    )
    revisor = ChatCompletionAgent(
        name="revisor",
        description="Valida números e aponta inconsistências.",
        instructions=(
            "Você é um revisor técnico rigoroso. Verifique os números do texto recebido, "
            "aponte inconsistências, riscos e afirmações sem evidência. "
            "Devolva o texto corrigido com suas observações."
        ),
        service=make_service(),
    )
    editor = ChatCompletionAgent(
        name="editor",
        description="Produz a versão final para stakeholders.",
        instructions=(
            "Você é um editor executivo. Transforme o material recebido em um resumo "
            "claro e direto para a diretoria, em no máximo 3 parágrafos, em português."
        ),
        service=make_service(),
    )
    return [analista, revisor, editor]


def log_etapa(message: ChatMessageContent) -> None:
    """Observabilidade: imprime a saída de cada agente do pipeline."""
    print(f"\n{'=' * 60}\n🤖 [{message.name}]\n{'=' * 60}\n{message.content}")


async def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit(
            "OPENAI_API_KEY não configurada. "
            "Copie .env.example para .env e adicione sua chave."
        )

    orquestracao = SequentialOrchestration(
        members=build_agents(),
        agent_response_callback=log_etapa,
    )

    runtime = InProcessRuntime()
    runtime.start()
    try:
        resultado = await orquestracao.invoke(task=TAREFA, runtime=runtime)
        final = await resultado.get(timeout=120)
        print(f"\n{'#' * 60}\n✅ RESULTADO FINAL\n{'#' * 60}\n{final}")
    finally:
        await runtime.stop_when_idle()


if __name__ == "__main__":
    asyncio.run(main())
