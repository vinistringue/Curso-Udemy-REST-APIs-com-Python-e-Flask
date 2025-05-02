from flask import Flask
from flask_restful import Api
from sql_alchemy import banco
from flask_jwt_extended import JWTManager  # Importar o JWTManager
from resources.usuario import UserRegister, UserLogin, User  # Atualizar com os recursos corretos

app = Flask(__name__)

# Configurações do JWT
app.config["JWT_SECRET_KEY"] = "sua_chave_secreta"  # Troque por uma chave segura
jwt = JWTManager(app)  # Inicializa o JWTManager com a aplicação

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

banco.init_app(app)

api = Api(app)

# Criação do banco
with app.app_context():
    banco.create_all()

# Adicionando as rotas de recursos
api.add_resource(UserRegister, "/cadastro")
api.add_resource(UserLogin, "/login")
api.add_resource(User, "/usuarios/<int:user_id>")

# ✅ Roda o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
