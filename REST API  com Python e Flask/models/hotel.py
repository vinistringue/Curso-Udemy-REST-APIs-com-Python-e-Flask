from sql_alchemy import banco

class HotelModel(banco.Model):
    """
    Modelo da tabela 'hoteis' no banco de dados.
    Representa um hotel com ID, nome, estrelas, valor da diária e cidade.
    """
    __tablename__ = "hoteis"

    # Definição das colunas da tabela
    hotel_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80), nullable=False)
    estrelas = banco.Column(banco.Float(precision=1), nullable=False)
    diaria = banco.Column(banco.Float(precision=2), nullable=False)
    cidade = banco.Column(banco.String(40), nullable=False)

    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        """
        Construtor da classe HotelModel.
        """
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def json(self):
        """
        Retorna os dados do hotel no formato JSON.
        Útil para retornar como resposta de API.
        """
        return {
            "hotel_id": self.hotel_id,
            "nome": self.nome,
            "estrelas": self.estrelas,
            "diaria": self.diaria,
            "cidade": self.cidade,
        }

    @classmethod
    def find_hotel(cls, hotel_id):
        """
        Busca um hotel no banco de dados pelo ID.
        """
        return cls.query.filter_by(hotel_id=hotel_id).first()

    def save_hotel(self):
        """
        Salva (ou atualiza) o hotel no banco de dados.
        """
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, nome, estrelas, diaria, cidade):
        """
        Atualiza os atributos do hotel e salva no banco.
        """
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        self.save_hotel()

    def delete_hotel(self):
        """
        Remove o hotel do banco de dados.
        """
        banco.session.delete(self)
        banco.session.commit()
