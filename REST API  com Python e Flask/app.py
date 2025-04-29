from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from sql_alchemy import banco

def create_app():
    """
    Função responsável por criar e configurar a aplicação Flask.
    Define as configurações do banco de dados e registra os recursos (endpoints) da API.
    """
    app = Flask(__name__)

    # Define o caminho do banco de dados SQLite e desativa o rastreamento de modificações
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"  # Banco será salvo no mesmo diretório
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Evita sobrecarga de monitoramento do SQLAlchemy

    # Inicializa o SQLAlchemy com a aplicação Flask
    banco.init_app(app)

    # Inicializa a API RESTful
    api = Api(app)

    # Registra os recursos (endpoints) da API
    # /hoteis         → Retorna todos os hotéis (GET)
    # /hoteis/<id>    → Permite criar, consultar, atualizar ou deletar um hotel específico (GET, POST, PUT, DELETE)
    api.add_resource(Hoteis, "/hoteis")
    api.add_resource(Hotel, "/hoteis/<string:hotel_id>")

    return app

# Ponto de entrada da aplicação Flask
if __name__ == "__main__":
    # Cria a aplicação Flask configurada
    app = create_app()
    
    # Garante que as tabelas do banco de dados sejam criadas antes do primeiro request
    with app.app_context():
        banco.create_all()

    # Inicia o servidor Flask em modo debug
    # Debug = True → recarrega automaticamente o servidor em alterações no código
    app.run(debug=True)
