from flask import Flask
from flask_restful import Api
from sql_alchemy import banco
from flask_jwt_extended import JWTManager
from resources.usuario import UserRegister, UserLogin, User, UserLogout
from blocklist import BLOCKLIST

app = Flask(__name__)

# Configurações do JWT
app.config["JWT_SECRET_KEY"] = "sua_chave_secreta"  # Troque por uma chave segura
jwt = JWTManager(app)

# Configurações do SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

banco.init_app(app)
api = Api(app)

# Criação do banco
with app.app_context():
    banco.create_all()

# Verificação se o token está na blocklist
@jwt.token_in_blocklist_loader
def verifica_token_na_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

# Mensagem padrão para token revogado
@jwt.revoked_token_loader
def token_revogado(jwt_header, jwt_payload):
    return {"message": "Você foi deslogado."}, 401

# Rotas da API
api.add_resource(UserRegister, "/cadastro")
api.add_resource(UserLogin, "/login")
api.add_resource(User, "/usuarios/<int:user_id>")
api.add_resource(UserLogout, "/logout")

# Roda o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
