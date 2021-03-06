from flask import Flask, request, session
from flask_cors import CORS
from flask_principal import Principal, identity_loaded, RoleNeed
from requests_toolbelt.adapters import appengine
from werkzeug.utils import redirect

from user.model import User

appengine.monkeypatch()

import json

from auth.controller import auth as auth_controller
from credit.controller import credit as credit_controller
from user.controller import user as user_controller
from product.controller import product as product_controller
from transaction.controller import transaction as transaction_controller
from balance.controller import balance as balance_controller

app = Flask(__name__, static_folder='web')

principals = Principal(app)
principals._init_app(app)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

app.register_blueprint(auth_controller, url_prefix='/api/auth')
app.register_blueprint(credit_controller, url_prefix='/api/credit')
app.register_blueprint(user_controller, url_prefix='/api/user')
app.register_blueprint(product_controller, url_prefix='/api/product')
app.register_blueprint(transaction_controller, url_prefix='/api/transaction')
app.register_blueprint(balance_controller, url_prefix='/api/balance')

@app.route('/')
def main():
    return app.send_static_file('index.html')

@app.route('/meuIp/')
def meu_ip():
    return json.dumps(request.headers.get('X-Forwarded-For', request.remote_addr))

@app.before_request
def filter():
    if verifyCronHeader(request):
        return

    if verifyHeader(request):
        return

    if 'barzinga_user' in session:
        return

    if '/api/auth' not in request.url and '/api/auth/token' not in request.url and '/user' not in request.url:
        if not 'barzinga_user' in session:
            return redirect('/api/auth/')

@app.errorhandler(403)
def forbidden(e):
    return 'Acao nao permitida.', 403

@app.errorhandler(404)
def page_not_found(e):
    return 'Sorry, Nothing at this URL.', 404

@app.errorhandler(500)
def application_error(e):
    return 'Sorry, unexpected error: {}'.format(e), 500

def verifyCronHeader(request):
    return request.headers.get('X-Appengine-Cron')

def verifyHeader(request):
    return request.headers.get('Authorization') == 'Bearer NHogQU8SvqDdiFWiJCeQIkDzo1JSEhRH'

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    user_json = session['barzinga_user']
    user = User.query().filter(User.email == user_json["email"]).get()

    if user:
        identity.user = user.key.id()

        if user.admin :
            identity.provides.add(RoleNeed('admin'))
