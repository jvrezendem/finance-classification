import os 
from dotenv import load_dotenv 

load_dotenv() 

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 
OPENAI_MODEL = os.getenv("OPENAI_MODEL") 

MAX_PDF_SIZE_MB = int( os.getenv("MAX_PDF_SIZE_MB", "15") ) 
PAGES_PER_CHUNK = int( os.getenv("PAGES_PER_CHUNK", "2") ) 

def validate_settings() -> None: 
    if not OPENAI_API_KEY: 
        raise RuntimeError( "A variável OPENAI_API_KEY não foi configurada." ) 
    if not OPENAI_MODEL: 
        raise RuntimeError( "A variável OPENAI_MODEL não foi configurada." )
