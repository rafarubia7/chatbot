"""
Gerenciador de sessão e histórico de chat
"""
from typing import Dict, List, Optional
from datetime import datetime

class SessionManager:
    def __init__(self):
        self.chat_histories: Dict[str, List[Dict]] = {}
        self.chat_titles: Dict[str, str] = {}
    
    def get_chat_history(self, chat_id: str) -> List[Dict]:
        """Recupera o histórico de um chat específico"""
        return self.chat_histories.get(chat_id, [])
    
    def save_chat(self, chat_id: str, title: str, messages: List[Dict]) -> None:
        """Salva ou atualiza um chat"""
        self.chat_histories[chat_id] = messages
        self.chat_titles[chat_id] = title
    
    def delete_chat(self, chat_id: str) -> bool:
        """Deleta um chat"""
        if chat_id in self.chat_histories:
            del self.chat_histories[chat_id]
            if chat_id in self.chat_titles:
                del self.chat_titles[chat_id]
            return True
        return False
    
    def list_chats(self) -> List[Dict]:
        """Lista todos os chats"""
        chats = []
        for chat_id in self.chat_histories.keys():
            messages = self.chat_histories[chat_id]
            title = self.chat_titles.get(chat_id, f"Conversa {chat_id}")
            last_message = messages[-1]['text'] if messages else "Conversa iniciada"
            
            chats.append({
                "id": chat_id,
                "title": title,
                "lastMessage": last_message if len(last_message) <= 50 else last_message[:47] + "...",
                "timestamp": messages[-1].get('timestamp') if messages else None
            })
        
        # Ordenar por timestamp, mais recente primeiro
        return sorted(chats, key=lambda x: x['timestamp'] if x['timestamp'] else "", reverse=True)
    
    def add_message(self, chat_id: str, text: str, sender: str) -> None:
        """Adiciona uma mensagem ao histórico do chat"""
        if chat_id not in self.chat_histories:
            self.chat_histories[chat_id] = []
        
        message = {
            "text": text,
            "sender": sender,
            "timestamp": str(datetime.now())
        }
        
        self.chat_histories[chat_id].append(message)
    
    def get_chat_title(self, chat_id: str) -> Optional[str]:
        """Recupera o título de um chat"""
        return self.chat_titles.get(chat_id)
    
    def update_chat_title(self, chat_id: str, title: str) -> None:
        """Atualiza o título de um chat"""
        self.chat_titles[chat_id] = title 