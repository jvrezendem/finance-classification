from pathlib import Path
from app.services.dataframe_service import export_df, transaction_to_dataframe
from app.services.pdf_extractor import extrair_paginas_pdf
from app.services.llm_extractor import extract_transactions_with_llm
from app.services.statement_chunks import create_chunks

pdf_path = Path("./data/uploads/extratoBB.pdf")

pages = extrair_paginas_pdf(pdf_path)

chunks = create_chunks(pages)

result = extract_transactions_with_llm(chunks[0], "llm")

df = transaction_to_dataframe(result.transactions)

export_df(df, "result_test", Path("./data/outputs"))

    

