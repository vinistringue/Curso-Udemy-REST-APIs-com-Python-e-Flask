from flask import request, render_template
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt
)
from models.usuario import UserModel
from blocklist import BLOCKLIST
from utils.email import enviar_email_confirmacao  # ✅ Importação da função de e-mail

# Parser: só login e senha, não expomos 'ativado' no argumento
user_args = reqparse.RequestParser()
user_args.add_argument(
    'login', type=str, required=True,
    help="O campo 'login' não pode estar em branco.",
    location='json'
)
user_args.add_argument(
    'senha', type=str, required=True,
    help="O campo 'senha' não pode estar em branco.",
    location='json'
)


class User(Resource):
    @jwt_required()
    def get(self, user_id):
        """GET /usuarios/<user_id> — retorna dados do usuário"""
        user = UserModel.find_user(user_id)
        if user:
            return user.json(), 200
        return {"message": "Usuário não encontrado."}, 404

    @jwt_required()
    def delete(self, user_id):
        """DELETE /usuarios/<user_id> — exclui o usuário"""
        user = UserModel.find_user(user_id)
        if not user:
            return {"message": "Usuário não encontrado."}, 404
        try:
            user.delete_user()
            return {"message": "Usuário excluído com sucesso."}, 200
        except Exception as e:
            return {"message": "Erro ao deletar usuário.", "erro": str(e)}, 500


class UserRegister(Resource):
    def post(self):
        """POST /cadastro — registra um novo usuário"""
        dados = user_args.parse_args()
        if UserModel.find_by_login(dados['login']):
            return {'message': f"O login '{dados['login']}' já está em uso."}, 400

        novo_usuario = UserModel(**dados)
        novo_usuario.ativado = False
        try:
            novo_usuario.save_user()
            # ✅ Enviar email de confirmação
            enviar_email_confirmacao(novo_usuario)
            return {'message': 'Usuário criado com sucesso. Confirme seu email para ativar sua conta.'}, 201
        except Exception as e:
            return {'message': 'Erro ao salvar usuário.', 'erro': str(e)}, 500


class UserLogin(Resource):
    def post(self):
        """POST /login — autentica e retorna um access token"""
        dados = user_args.parse_args()
        usuario = UserModel.find_by_login(dados['login'])

        if not usuario or not usuario.verify_password(dados['senha']):
            return {'message': 'Usuário ou senha incorretos.'}, 401

        if not usuario.ativado:
            return {'message': 'Usuário não confirmado.'}, 401

        access_token = create_access_token(identity=str(usuario.user_id))
        return {'access_token': access_token}, 200


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        """POST /logout — invalida o token JWT atual"""
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Logout realizado com sucesso."}, 200


class UserConfirm(Resource):
    def get(self, user_id):
        """GET /confirmacao/<user_id> — ativa o usuário"""
        user = UserModel.find_user(user_id)
        if not user:
            return {"message": f"Usuário id '{user_id}' não encontrado."}, 404

        if user.ativado:
            return render_template("confirmacao_sucesso.html", mensagem="Usuário já estava confirmado.")

        user.ativado = True
        try:
            user.save_user()
            # ✅ Retorna uma página HTML de sucesso
            return render_template("confirmacao_sucesso.html", mensagem="Sua conta foi confirmada com sucesso!")
        except Exception as e:
            return {"message": "Erro ao confirmar usuário.", "erro": str(e)}, 500
