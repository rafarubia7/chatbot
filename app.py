"""
Aplicação principal do chatbot do SENAI São Carlos
"""
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS

from config import FLASK_SECRET_KEY
from utils.chat_manager import process_message
from utils.session_manager import SessionManager
from info.responses import RESPOSTAS_PADRAO

app = Flask(__name__)
CORS(app)
app.secret_key = FLASK_SECRET_KEY

# Instanciar o gerenciador de sessão
session_manager = SessionManager()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if not username:
            return render_template('login.html', error="Por favor, insira seu nome")
        
        session['username'] = username
        return redirect(url_for('home'))
    
    return render_template('login.html')

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

@app.route('/chat', methods=['POST'])
def chat():
    try:
        if not request.is_json:
            return jsonify({"reply": "Erro: Content-Type deve ser application/json"}), 415
            
        data = request.get_json()
        user_message = data.get('message', '').strip()
        chat_id = data.get('chat_id')
        
        if not user_message:
            return jsonify({"reply": "Por favor, digite uma mensagem."}), 400
            
        if not chat_id:
            return jsonify({"error": "Chat ID não fornecido"}), 400
        
        # Adicionar mensagem do usuário ao histórico
        session_manager.add_message(chat_id, user_message, "user")
        
        # Processar a mensagem e gerar resposta
        chat_history = session_manager.get_chat_history(chat_id)
        ai_response = process_message(user_message, chat_history)
        
        # Adicionar resposta do AI ao histórico
        session_manager.add_message(chat_id, ai_response, "ai")
        
        return jsonify({"reply": ai_response})
            
    except Exception as e:
        print(f"Erro no processamento da mensagem: {str(e)}")
        return jsonify({"reply": RESPOSTAS_PADRAO["erro_geral"]})

@app.route('/chat/history', methods=['GET'])
def get_chat_history():
    try:
        chat_id = request.args.get('chat_id')
        if not chat_id:
            return jsonify({"error": "Chat ID não fornecido"}), 400
            
        chat_history = session_manager.get_chat_history(chat_id)
        return jsonify({"history": chat_history})
    except Exception as e:
        print(f"Erro ao recuperar histórico: {str(e)}")
        return jsonify({"error": "Erro ao recuperar histórico"}), 500

@app.route('/chat/save', methods=['POST'])
def save_chat():
    try:
        data = request.get_json()
        chat_id = data.get('chat_id')
        title = data.get('title')
        messages = data.get('messages', [])
        
        if not chat_id:
            return jsonify({"error": "Chat ID não fornecido"}), 400
            
        session_manager.save_chat(chat_id, title, messages)
        return jsonify({"status": "success"})
    except Exception as e:
        print(f"Erro ao salvar chat: {str(e)}")
        return jsonify({"error": "Erro ao salvar chat"}), 500

@app.route('/chat/list', methods=['GET'])
def list_chats():
    try:
        chats = session_manager.list_chats()
        return jsonify({"chats": chats})
    except Exception as e:
        print(f"Erro ao listar chats: {str(e)}")
        return jsonify({"error": "Erro ao listar chats"}), 500

@app.route('/chat/delete', methods=['POST'])
def delete_chat():
    try:
        data = request.get_json()
        chat_id = data.get('chat_id')
        
        if not chat_id:
            return jsonify({"error": "Chat ID não fornecido"}), 400
            
        if session_manager.delete_chat(chat_id):
            return jsonify({"status": "success"})
        else:
            return jsonify({"error": "Chat não encontrado"}), 404
    except Exception as e:
        print(f"Erro ao deletar chat: {str(e)}")
        return jsonify({"error": "Erro ao deletar chat"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)