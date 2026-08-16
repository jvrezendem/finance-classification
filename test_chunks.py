from app.services.pdf_extractor import extrair_paginas_pdf
from app.services.statement_chunks import create_chunks
from pathlib import Path

#caminho do pdf
pages = extrair_paginas_pdf(Path("./data/uploads/extratoBB.pdf"))

#cria os chunks
chunks = create_chunks(pages)   

print(f"Quantidade de chunks: {len(chunks)}")

print(chunks[0])