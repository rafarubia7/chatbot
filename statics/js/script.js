document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    function addMessage(sender, message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        
        addMessage('user', message);
        userInput.value = '';
        
        try {
            // Mostra indicador de digitação
            const typingIndicator = document.createElement('div');
            typingIndicator.className = 'typing-indicator';
            typingIndicator.innerHTML = `
                <div class="typing-dots">
                    <div></div>
                    <div></div>
                    <div></div>
                </div>
                <span>Digitando...</span>
            `;
            chatMessages.appendChild(typingIndicator);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            // Remove indicador de digitação
            chatMessages.removeChild(typingIndicator);
            
            if (!response.ok) throw new Error('Erro na resposta');
            
            const data = await response.json();
            addMessage('bot', data.reply);
            
        } catch (error) {
            addMessage('bot', 'Desculpe, ocorreu um erro ao processar sua mensagem.');
            console.error('Erro:', error);
        }
    }

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});