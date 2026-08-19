from pathlib import Path
from groq import Groq
from app.config import LLM_API_KEY, LLM_MODEL, validate_settings
from app.models.statement import Extrato


validate_settings()

#cria o cliente do llm
client = Groq(api_key=LLM_API_KEY)

def load_prompt():
    # Resolve path relative to this file, not the working directory
    prompt_path = Path(__file__).parent.parent / "prompts" / "statement_extraction.txt"
    return prompt_path.read_text(encoding="utf-8")

def _extrato_schema_for_llm() -> dict:
    """Return the Extrato JSON schema with post-processing fields removed.

    Groq strict mode requires every property listed in `required`.
    Fields like `warnings` have defaults and are populated after LLM extraction,
    so they must be stripped from the schema before sending to the API.
    """
    schema = Extrato.model_json_schema()

    # Strip `warnings` from Transacao definition
    transacao = schema.get("$defs", {}).get("Transacao", {})
    transacao.get("properties", {}).pop("warnings", None)
    if "required" in transacao and "warnings" in transacao["required"]:
        transacao["required"].remove("warnings")

    return schema

def extract_transactions_with_llm(extrato_text, extraction_method):   
    prompt = load_prompt()

    user_content = f"""
    {prompt}

    A resposta deve ser exclusivamente o objeto JSON definido pelo schema de saída.

    Método de Extração: {extraction_method}

    Conteúdo do Extrato Bancário:

    {extrato_text}
    """

    response = client.chat.completions.create(
        model=LLM_MODEL, 
        messages=[
            {"role": "user", "content": user_content},
        ],
        reasoning_effort="low",
        include_reasoning=False,
        max_completion_tokens=4096,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "extrato",
                "strict": True,
                "schema": _extrato_schema_for_llm(),
            },
        }
    )

    result = Extrato.model_validate_json(response.choices[0].message.content)

    if not result:
        raise RuntimeError("O LLM não retornou dados estruturados")
    
    return result
