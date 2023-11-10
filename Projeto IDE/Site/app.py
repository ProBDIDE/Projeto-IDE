# Importando as bibliotecas necessárias
from flask import Flask, request, render_template
from flaskext.mysql import MySQL

# Inicializando a aplicação Flask e o objeto MySQL
app = Flask(__name__)
mysql = MySQL()

# Configurando os detalhes do banco de dados MySQL
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '2323'
app.config['MYSQL_DATABASE_DB'] = 'Project_IDE'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# Definindo a rota padrão que renderiza a página de login
@app.route('/')
def home():
    return render_template('login.html')

# Definindo a rota de login que verifica as credenciais do usuário no banco de dados
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = mysql.connect()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM usuarios WHERE username=%s AND password=%s", (username, password))
    data = cursor.fetchone()
    
    if data is None:
        return render_template('login incorreto.html')
    else:
        return render_template('bem sucedido.html')

# Definindo a rota de registro que permite ao usuário criar uma nova conta
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = mysql.connect()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM usuarios WHERE username=%s", (username,))
        data = cursor.fetchone()
        if data is not None:
            return render_template('existe.html')  
        
        cursor.execute("INSERT INTO usuarios (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        conn.commit()
        
        return render_template('cadastro bem sucedido.html')  
    else:
        return render_template('register.html')  

# Iniciando a aplicação Flask
if __name__ == '__main__':
    app.run(debug=True)
