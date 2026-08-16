#dividir o texto em blocos(chunks)
from app.services.pdf_extractor import Pagina
from dotenv import load_dotenv
import os

load_dotenv()

#transforma a pagina num bloco formatado
def build_page_block(page: Pagina):
    return (
        f"=== PÁGINA {page.page_num} ===\n"
        f"{page.text}\n"
        f"=== FIM DA PÁGINA {page.page_num} ===\n"
        f"\n"
    )

    #cria a lista de chunks
def create_chunks(pages: list[Pagina]):
    pages_per_chunk = int(os.getenv("PAGES_PER_CHUNK",2))

    chunks = []

    for i in range(0, len(pages), pages_per_chunk):
        #pega o indice i ate o indice i+pages_per_chunk
        chunk_pages = pages[i:i+pages_per_chunk]

        page_blocks = []
        for page in chunk_pages:
            page_block = build_page_block(page)
            page_blocks.append(page_block)

        #junta as duas paginas no chunk separadas por duas linhas
        chunk = "\n\n".join(page_blocks)

    chunks.append(chunk)

    return chunks


            
            
    
