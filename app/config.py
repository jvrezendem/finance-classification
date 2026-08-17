import os 
from dotenv import load_dotenv 

load_dotenv() 

#arquivo que irá disponibilizar as credenciais da ia para os outros arquivos do sistema

LLM_API_KEY = os.getenv("LLM_API_KEY") 
LLM_MODEL = os.getenv("LLM_MODEL") 

MAX_PDF_SIZE_MB = int( os.getenv("MAX_PDF_SIZE_MB", "15") ) 
PAGES_PER_CHUNK = int( os.getenv("PAGES_PER_CHUNK", "2") ) 


#função que irá validar as configurações
def validate_settings():
    if not LLM_API_KEY: 
        raise RuntimeError( "A variável LLM_API_KEY não foi configurada." ) 
    if not LLM_MODEL: 
        raise RuntimeError( "A variável LLM_MODEL não foi configurada." )
