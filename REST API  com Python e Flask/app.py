from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from sql_alchemy import banco
from blocklist import BLOCKLIST

# Recursos
from resources.hotel import Hotel, Hoteis
from resources.usuario import UserRegister, UserLogin, User, UserLogout

# Modelos (imprescindível para create_all)
from models.hotel import HotelModel
from models.usuario import UserModel

app = Flask(__name__)

# Configurações JWT
app.config["JWT_SECRET_KEY"] = "sua_chave_secreta"
jwt = JWTManager(app)

# Configurações SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
banco.init_app(app)

api = Api(app)

# Cria todas as tabelas (só funciona se os modelos estiverem importados!)
with app.app_context():
    banco.create_all()

# Callbacks JWT
@jwt.token_in_blocklist_loader
def verifica_token_na_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

@jwt.revoked_token_loader
def token_revogado(jwt_header, jwt_payload):
    return {"message": "Você foi deslogado."}, 401

# Rotas
api.add_resource(UserRegister, "/cadastro")
api.add_resource(UserLogin,    "/login")
api.add_resource(User,         "/usuarios/<int:user_id>")
api.add_resource(UserLogout,   "/logout")
api.add_resource(Hoteis,       "/hoteis")
api.add_resource(Hotel,        "/hoteis/<string:hotel_id>")

if __name__ == "__main__":
    app.run(debug=True)
