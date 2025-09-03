from flask import Flask,request,jsonify,render_template,render_template_string
import logging
import markdown
from models import DataBase
###
host = "192.168.3.31"
user = "k2bd05"
password = "k2bd05"
database = "k2bd05"
###
app = Flask(__name__)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main.log'),
        logging.StreamHandler()
    ]
)
db = DataBase(host,user,password,database)
if db:
    logging.log(logging.INFO, f"Connect db {database} complite")
else:
    logging.log(logging.INFO, f"Connect db {database} false")

def log_with_ip(message,level=logging.INFO):
    ip_address = request.remote_addr
    log_message = f"{message} [IP: {ip_address}]"
    logging.log(level,log_message)
@app.route('/')
def home():
    with open('README.md','r',encoding='utf-8')as f:
        content = f.read()
        content_html=markdown.markdown(content)
        return render_template_string(content_html)
@app.route('/registration',methods=['POST'])
def registration():
    data = request.json
    login = data.get('login')
    password = data.get('password')
    if data.get('token'):
        token = data.get('token')
    name = data.get('name')
    if not login or not password or not name:
        log_with_ip("Registration attempt without login/password/name", logging.WARNING)
        return jsonify({'error':'login or Password or Name required'}),400
    if db.registration(login,password,name):
        log_with_ip(f"User {login} registered")
        return jsonify({'message': 'User created'}), 201
    else:
        log_with_ip(f"User {login} no registered")
        return jsonify({'message': 'User no created'}), 401
@app.route('/auth',methods=['POST'])
def auth():
    data = request.json
    login = data.get('login')
    password = data.get('password')
    if not login or not password :
        log_with_ip("Registration attempt without login/password", logging.WARNING)
        return jsonify({'error':'login or Password required'}),400
    if db.auth(login,password):

        log_with_ip(f"User {login}  authorized", logging.INFO)

        return jsonify({'message': 'User authorized'}), 201
    else:

        log_with_ip(f"User {login} no authorized")
        return jsonify({'message': 'User no authorized'}), 401
@app.route('/out',methods=['POST'])
def out():
    data = request.json
    login = data.get('login')
    token = data.get('token')
    if not login or not token :
        log_with_ip("Registration attempt without login/token", logging.WARNING)
        return jsonify({'error':'login or token  required'}),400
    if db.out(login,token):
        log_with_ip(f"User {login}  came out", logging.INFO)
        return jsonify({'message': 'User came out'}), 201
    else:
        log_with_ip(f"User {login} no came out")
        return jsonify({'message': 'User no came out'}), 401


@app.route('/edit_password', methods=['POST'])
def edit_password():
    data = request.json
    login = data.get('login')
    old_pass = data.get('old_password')
    new_pass = data.get('new_password')

    if db.edit_password(login, old_pass, new_pass):
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'failed'}), 400

if __name__ == '__main__':
    logging.log(logging.INFO,"Auth_server Start")
    app.run(host='0.0.0.0', port=5007, debug=True)
