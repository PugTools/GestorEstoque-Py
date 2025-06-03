import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from src.models.user import db
from src.models.product import Product # Adicionado
from src.models.stock_movement import StockMovement # Adicionado
from src.routes.user import user_bp
from src.routes.product import product_bp # Adicionado
from src.routes.stock_movement import stock_movement_bp # Adicionado

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Configuração do Banco de Dados SQLite
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'estoque.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Cria o diretório instance se não existir
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

db.init_app(app)

# Registrar Blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(product_bp, url_prefix='/api') # Adicionado
app.register_blueprint(stock_movement_bp, url_prefix='/api') # Adicionado

with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
