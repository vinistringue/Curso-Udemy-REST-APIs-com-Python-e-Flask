from sql_alchemy import banco

class HotelModel(banco.Model):
    __tablename__ = 'hoteis'

    hotel_id = banco.Column(banco.String, primary_key=True, nullable=False)
    nome     = banco.Column(banco.String(80), nullable=False)
    estrelas = banco.Column(banco.Float(precision=1), nullable=False)
    diaria   = banco.Column(banco.Float(precision=2), nullable=False)
    cidade   = banco.Column(banco.String(40), nullable=False)

    # Relacionamento 1:N: um Site pode ter muitos Hotéis
    site_id = banco.Column(banco.Integer, banco.ForeignKey('sites.site_id'), nullable=True)
    site    = banco.relationship('SiteModel', back_populates='hoteis')

    def __init__(self, hotel_id: str, nome: str, estrelas: float,
                 diaria: float, cidade: str, site_id: int = None):
        self.hotel_id = hotel_id
        self.nome      = nome
        self.estrelas  = estrelas
        self.diaria    = diaria
        self.cidade    = cidade
        self.site_id   = site_id

    def json(self) -> dict:
        """
        Retorna uma representação JSON do hotel, incluindo o site associado (se existir).
        """
        data = {
            'hotel_id': self.hotel_id,
            'nome':      self.nome,
            'estrelas':  self.estrelas,
            'diaria':    self.diaria,
            'cidade':    self.cidade,
        }
        if self.site_id:
            data['site_id'] = self.site_id
        return data

    def __repr__(self) -> str:
        return f"<Hotel {self.nome} (ID: {self.hotel_id}) em {self.cidade}>"

    @classmethod
    def find_hotel(cls, hotel_id: str) -> 'HotelModel':
        """
        Busca um hotel pelo seu ID.
        """
        return cls.query.filter_by(hotel_id=hotel_id).first()

    @classmethod
    def find_all(cls) -> list['HotelModel']:
        """
        Retorna todos os hotéis.
        """
        return cls.query.all()

    @classmethod
    def find_by_site_id(cls, site_id: int) -> list['HotelModel']:
        """
        Retorna todos os hotéis associados a um determinado site.
        """
        return cls.query.filter_by(site_id=site_id).all()

    def save_hotel(self) -> None:
        """
        Adiciona ou atualiza o registro de hotel no banco de dados.
        """
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, nome: str, estrelas: float, diaria: float, 
                     cidade: str, site_id: int = None) -> None:
        """
        Atualiza os atributos do hotel e persiste no banco.
        """
        self.nome      = nome
        self.estrelas  = estrelas
        self.diaria    = diaria
        self.cidade    = cidade
        self.site_id   = site_id
        self.save_hotel()

    def delete_hotel(self) -> None:
        """
        Remove o hotel do banco de dados.
        """
        banco.session.delete(self)
        banco.session.commit()
