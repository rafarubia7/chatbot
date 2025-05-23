from flask import Flask, render_template

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def home():
    return render_template('base.html')  # Tela principal que você quer mostrar ao iniciar

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/criar_conta')
def criar_conta():
    return render_template('criar_conta.html')

if __name__ == '__main__':
    app.run(debug=True)
