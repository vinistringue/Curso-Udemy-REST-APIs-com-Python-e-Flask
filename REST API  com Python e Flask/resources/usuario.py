from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from models.usuario import UserModel
from blocklist import BLOCKLIST

# Parser único e centralizado
user_args = reqparse.RequestParser()
user_args.add_argument('login', type=str, required=True, help="O campo 'login' não pode estar em branco.")
user_args.add_argument('senha', type=str, required=True, help="O campo 'senha' não pode estar em branco.")

class User(Resource):
    @jwt_required()
    def get(self, user_id):
        """
        Retorna informações de um usuário com base no user_id.
        """
        user = UserModel.find_user(user_id)
        if user:
            return user.json(), 200
        return {"message": "Usuário não encontrado."}, 404

    @jwt_required()
    def delete(self, user_id):
        """
        Deleta um usuário com base no user_id.
        """
        user = UserModel.find_user(user_id)
        if not user:
            return {"message": "Usuário não encontrado."}, 404
        try:
            user.delete_user()
            return {"message": "Usuário excluído com sucesso."}, 200
        except Exception as e:
            return {"message": f"Erro ao deletar usuário: {str(e)}"}, 500

class UserRegister(Resource):
    def post(self):
        """
        Registra um novo usuário.
        """
        dados = user_args.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'message': f"O login '{dados['login']}' já está em uso."}, 400

        novo_usuario = UserModel(**dados)
        novo_usuario.save_user()
        return {'message': 'Usuário criado com sucesso.'}, 201

class UserLogin(Resource):
    def post(self):
        """
        Realiza o login de um usuário e retorna o token JWT.
        """
        dados = user_args.parse_args()
        usuario = UserModel.find_by_login(dados['login'])

        if usuario and usuario.verify_password(dados['senha']):
            access_token = create_access_token(identity=str(usuario.user_id))
            return {'access_token': access_token}, 200

        return {'message': 'Usuário ou senha incorretos.'}, 401

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        """
        Realiza o logout do usuário invalidando o token atual.
        """
        jwt_token = get_jwt()
        jti = jwt_token["jti"]  # ID único do token
        BLOCKLIST.add(jti)
        return {"message": "Logout realizado com sucesso."}, 200
