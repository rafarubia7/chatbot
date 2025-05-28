"""
Sistema de cache para respostas do chatbot
"""
from typing import Any, Optional
import redis
import json
from datetime import datetime, timedelta
import os
from loguru import logger

class Cache:
    def __init__(self):
        """Inicializa a conexão com Redis"""
        try:
            self.redis = redis.from_url(
                os.getenv('REDIS_URL', 'redis://localhost:6379/0')
            )
            self.timeout = int(os.getenv('CACHE_TIMEOUT', 300))
            self.enabled = True
        except redis.ConnectionError:
            logger.warning("Redis não disponível. Cache será desabilitado.")
            self.enabled = False

    def _generate_key(self, query: str) -> str:
        """Gera uma chave única para a query"""
        return f"chatbot:response:{query.lower().strip()}"

    def get(self, query: str) -> Optional[Any]:
        """Recupera uma resposta do cache"""
        if not self.enabled:
            return None
            
        try:
            key = self._generate_key(query)
            data = self.redis.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            logger.error(f"Erro ao recuperar do cache: {e}")
        return None

    def set(self, query: str, response: Any) -> bool:
        """Armazena uma resposta no cache"""
        if not self.enabled:
            return False
            
        try:
            key = self._generate_key(query)
            data = {
                'response': response,
                'timestamp': datetime.now().isoformat()
            }
            self.redis.setex(
                key,
                self.timeout,
                json.dumps(data)
            )
            return True
        except Exception as e:
            logger.error(f"Erro ao armazenar no cache: {e}")
            return False

    def invalidate(self, query: str) -> bool:
        """Invalida uma entrada específica do cache"""
        if not self.enabled:
            return False
            
        try:
            key = self._generate_key(query)
            self.redis.delete(key)
            return True
        except Exception as e:
            logger.error(f"Erro ao invalidar cache: {e}")
            return False

    def clear_all(self) -> bool:
        """Limpa todo o cache do chatbot"""
        if not self.enabled:
            return False
            
        try:
            keys = self.redis.keys("chatbot:response:*")
            if keys:
                self.redis.delete(*keys)
            return True
        except Exception as e:
            logger.error(f"Erro ao limpar cache: {e}")
            return False

# Instância global do cache
cache = Cache() 