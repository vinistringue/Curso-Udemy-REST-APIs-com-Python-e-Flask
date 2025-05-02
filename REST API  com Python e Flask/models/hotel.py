from sql_alchemy import banco

class HotelModel(banco.Model):
    __tablename__ = "hoteis"

    hotel_id = banco.Column(banco.String, primary_key=True, nullable=False)
    nome = banco.Column(banco.String(80), nullable=False)
    estrelas = banco.Column(banco.Float(precision=1), nullable=False)
    diaria = banco.Column(banco.Float(precision=2), nullable=False)
    cidade = banco.Column(banco.String(40), nullable=False)

    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def json(self):
        return {
            "hotel_id": self.hotel_id,
            "nome": self.nome,
            "estrelas": self.estrelas,
            "diaria": self.diaria,
            "cidade": self.cidade,
        }

    def __repr__(self):
        return f"<Hotel {self.nome} ({self.hotel_id})>"

    def __eq__(self, other):
        return isinstance(other, HotelModel) and self.hotel_id == other.hotel_id

    def __hash__(self):
        return hash(self.hotel_id)

    @classmethod
    def find_hotel(cls, hotel_id):
        return cls.query.filter_by(hotel_id=hotel_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, nome, estrelas, diaria, cidade):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        self.save_hotel()

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()
