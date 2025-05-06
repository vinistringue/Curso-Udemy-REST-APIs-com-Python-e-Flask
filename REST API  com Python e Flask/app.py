from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Banco e blocklist
from sql_alchemy import banco
from blocklist import BLOCKLIST

# Recursos de Sites
from resources.site import Sites, Site
# Recursos de Hotéis
from resources.hotel import Hoteis, Hotel
# Recursos de Usuários e Autenticação
from resources.usuario import UserRegister, UserLogin, User, UserLogout

# Modelos (necessários para create_all)
from models.hotel import HotelModel
from models.site import SiteModel
from models.usuario import UserModel


def create_app():
    app = Flask(__name__)

    # Configurações do JWT
    app.config["JWT_SECRET_KEY"] = "sua_chave_secreta"  # Alterar para variável de ambiente em produção
    jwt = JWTManager(app)

    # Configurações do SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    banco.init_app(app)

    # Configuração CORS (permite requisições de outros domínios)
    CORS(app)

    api = Api(app)

    # Criação de todas as tabelas (executado dentro do contexto do app)
    with app.app_context():
        banco.create_all()

    # Callbacks JWT
    @jwt.token_in_blocklist_loader
    def verifica_token_na_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def token_revogado(jwt_header, jwt_payload):
        return jsonify({"message": "Você foi deslogado."}), 401

    # Rotas de Usuário e Autenticação
    api.add_resource(UserRegister, "/cadastro")
    api.add_resource(UserLogin,    "/login")
    api.add_resource(User,         "/usuarios/<int:user_id>")
    api.add_resource(UserLogout,   "/logout")

    # Rotas de Sites (proteja se necessário via JWT)
    api.add_resource(Sites, "/sites")
    api.add_resource(Site,  "/sites/<int:site_id>")

    # Rotas de Hotéis (proteja se necessário via JWT)
    api.add_resource(Hoteis, "/hoteis")
    api.add_resource(Hotel,  "/hoteis/<string:hotel_id>")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
