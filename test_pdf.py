from pathlib import Path
import inspect 
from app.services.pdf_extractor import extrair_paginas_pdf
import app.services.pdf_extractor as pdf_extractor


pages = extrair_paginas_pdf(
    Path("./data/uploads/extratoBB.pdf")
)

for page in pages:
    print(f"pagina {page.page_num}")
    print(f"Método: {page.extraction_method}")
    print(page.text[:1000])
    print("-" * 60)