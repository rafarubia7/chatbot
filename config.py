"""
Configurações da aplicação
"""
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Flask
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'sua-chave-secreta-aqui')
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))

# Configurações do LM Studio
LM_STUDIO_URL = os.getenv('LM_STUDIO_URL', 'http://localhost:1234/v1/completions')
MODEL_NAME = os.getenv('MODEL_NAME', 'llama-3.1-tulu-3-8b')
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))
MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
RETRY_DELAY = int(os.getenv('RETRY_DELAY', 1))

# Configurações de logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'app.log')

# Configurações de sessão
SESSION_TYPE = 'filesystem'
SESSION_PERMANENT = False
PERMANENT_SESSION_LIFETIME = 1800  # 30 minutos

# Configurações de cache
CACHE_TIMEOUT = 300  # 5 minutos

# Configurações de logging
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'