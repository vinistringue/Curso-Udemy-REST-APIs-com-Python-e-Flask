from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Banco e blocklist
from sql_alchemy import banco
from blocklist import BLOCKLIST

# Recursos
from resources.site import Sites, Site, HoteisPorSite
from resources.hotel import Hoteis, Hotel
from resources.usuario import UserRegister, UserLogin, User, UserLogout, UserConfirm

# Modelos
from models.hotel import HotelModel
from models.site import SiteModel
from models.usuario import UserModel

import os

def create_app():
    app = Flask(__name__)

    # Configurações JWT
    app.config["JWT_SECRET_KEY"] = "sua_chave_secreta"
    jwt = JWTManager(app)

    # Configurações SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    banco.init_app(app)

    # Habilita CORS
    CORS(app)

    # Configurações de Email (Mailgun)
    app.config["MAILGUN_DOMAIN"] = "api.projeto.com"
    app.config["MAILGUN_API_KEY"] = "sua_api_key_mailgun"  # Substitua pela real
    app.config["EMAIL_FROM"] = "postmaster@api.projeto.com"
    app.config["SMTP_PASSWORD"] = "Hangloose12"  # Guardado apenas para referência

    api = Api(app)

    # Criação de tabelas
    with app.app_context():
        banco.create_all()

    # Callbacks JWT
    @jwt.token_in_blocklist_loader
    def verifica_token_na_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def token_revogado(jwt_header, jwt_payload):
        return jsonify({"message": "Você foi deslogado."}), 401

    # Rotas
    api.add_resource(UserRegister, "/cadastro")
    api.add_resource(UserLogin, "/login")
    api.add_resource(User, "/usuarios/<int:user_id>")
    api.add_resource(UserLogout, "/logout")
    api.add_resource(UserConfirm, "/confirmacao/<int:user_id>")

    api.add_resource(Sites, "/sites")
    api.add_resource(Site, "/sites/<int:site_id>")
    api.add_resource(HoteisPorSite, "/sites/<string:url>/hoteis")

    api.add_resource(Hoteis, "/hoteis")
    api.add_resource(Hotel, "/hoteis/<string:hotel_id>")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
