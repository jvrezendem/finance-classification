#modelo padronizado de guardar os dados das transações

from datetime import date
from typing import Literal
from pydantic import BaseModel

tipo_transacao = Literal[
    "credito",
    "debito",
    "pix",
    "outros"
]

direcao_transacao = Literal[
    "entrada",
    "saida",
    "desconhecido"
]



metodo_extracao = Literal[
    "parser",
    "llm",
    "ocr_llm"
]

#dados de uma transação
class Transacao(BaseModel):
    date_time: date | None

    description_raw: str
    description_normalized: str | None 

    amount_cents: int | None
    direction: direcao_transacao = "desconhecido"
    #tipo da transação
    transaction_type: tipo_transacao = "outros"

    balance_after_cents: int | None

    document_number: str | None 
    transaction_code: str | None

    source_page: int
    source_text: str

    extraction_method: metodo_extracao

#dados do extrato completo
class Extrato(BaseModel):
    bank_name: str | None
    account_holder: str | None
    account_reference_masked: str | None

    period_start: date | None 
    period_end: date | None

    transactions: list[Transacao]
    

    