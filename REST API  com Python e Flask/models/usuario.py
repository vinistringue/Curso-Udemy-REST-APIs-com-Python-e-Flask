from sql_alchemy import banco
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(banco.Model):
    __tablename__ = "usuarios"

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(200), nullable=False)
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, senha, ativado=False):
        """
        Inicializa o usuário com login, senha (criptografada) e estado de ativação.
        """
        self.login = login
        self.senha = generate_password_hash(senha)
        self.ativado = ativado

    def json(self):
        return {
            "user_id": self.user_id,
            "login": self.login,
            "ativado": self.ativado
        }

    @classmethod
    def find_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_by_login(cls, login):
        return cls.query.filter_by(login=login).first()

    def verify_password(self, senha_texto):
        return check_password_hash(self.senha, senha_texto)

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
