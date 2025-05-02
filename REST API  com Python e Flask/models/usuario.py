from sql_alchemy import banco
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel(banco.Model):
    __tablename__ = "usuarios"

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(200), nullable=False)  # O hash da senha geralmente é longo

    def __init__(self, login, senha):
        """
        Construtor da classe UserModel.
        A senha é salva de forma criptografada.
        """
        self.login = login
        self.senha = generate_password_hash(senha)  # Gera o hash da senha na criação

    def json(self):
        """
        Retorna os dados do usuário no formato JSON.
        """
        return {
            'user_id': self.user_id,
            'login': self.login
        }

    @classmethod
    def find_user(cls, user_id):
        """
        Busca um usuário no banco de dados pelo user_id.
        """
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_by_login(cls, login):
        """
        Busca um usuário no banco de dados pelo login.
        """
        return cls.query.filter_by(login=login).first()

    def verify_password(self, senha_texto):
        """
        Verifica se a senha fornecida bate com o hash da senha armazenada.
        """
        return check_password_hash(self.senha, senha_texto)

    def save_user(self):
        """
        Salva o usuário no banco de dados.
        """
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        """
        Deleta o usuário do banco de dados.
        """
        banco.session.delete(self)
        banco.session.commit()
