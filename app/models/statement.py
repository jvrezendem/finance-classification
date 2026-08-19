#modelo padronizado de guardar os dados das transações

from datetime import date
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

tipo_transacao = Literal[
    "pix",
    "ted",
    "boleto",
    "transferencia",
    "compra_cartao",
    "saque",
    "deposito",
    "tarifa",
    "juros",
    "estorno",
    "unknown",
]

direcao_transacao = Literal[
    "debit",
    "credit",
    "unknown",
]



metodo_extracao = Literal[
    "parser",
    "llm",
    "ocr_llm"
]

#dados de uma transação
class Transacao(BaseModel):
    model_config = ConfigDict(extra="forbid")

    date_time: date | None

    description_raw: str
    description_normalized: str | None 

    amount_cents: int | None
    direction: direcao_transacao
    #tipo da transação
    transaction_type: tipo_transacao

    balance_after_cents: int | None

    document_number: str | None 
    transaction_code: str | None

    source_page: int
    source_text: str

    extraction_method: metodo_extracao

    warnings: list[str] = Field(
        default_factory=list,
        exclude=True,       # kept off the JSON schema sent to Groq (strict mode requires all props in `required`)
    )

#dados do extrato completo
class Extrato(BaseModel):
    model_config = ConfigDict(extra="forbid")

    bank_name: str | None
    account_holder: str | None
    account_reference_masked: str | None

    period_start: date | None 
    period_end: date | None

    transactions: list[Transacao]
    

    
