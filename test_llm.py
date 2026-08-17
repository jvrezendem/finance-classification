from pathlib import Path
from app.services.llm_extractor import extract_transactions_with_llm
from app.services.pdf_extractor import extrair_paginas_pdf
from app.services.statement_chunks import create_chunks

pages = extrair_paginas_pdf(Path("./data/uploads/extratoBB.pdf"))

chunks = create_chunks(pages)

result = extract_transactions_with_llm(chunks[0], "llm")

print(result.model_dump_json(indent=4, ensure_ascii=False))