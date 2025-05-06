# models/site.py
from typing import List, Optional
from sql_alchemy import banco

class SiteModel(banco.Model):
    __tablename__ = 'sites'

    site_id = banco.Column(banco.Integer, primary_key=True, autoincrement=True)
    nome    = banco.Column(banco.String(80), nullable=False)
    url     = banco.Column(banco.String(200), nullable=False, unique=True)

    # Relacionamento 1→N: um site tem muitos hotéis; composição pura (cascade)
    hoteis  = banco.relationship(
        'HotelModel', back_populates='site', lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __init__(self, nome: str, url: str):
        self.nome = nome
        self.url  = url

    def json(self, include_hotels: bool = True) -> dict:
        """
        Retorna a representação JSON do site. Se include_hotels=True, inclui lista de hotéis.
        """
        data = {
            'site_id': self.site_id,
            'nome':    self.nome,
            'url':     self.url,
        }
        if include_hotels:
            data['hoteis'] = [hotel.json() for hotel in self.hoteis.all()]
        return data

    @classmethod
    def find_by_id(cls, site_id: int) -> Optional['SiteModel']:
        return cls.query.get(site_id)

    @classmethod
    def find_by_url(cls, url: str) -> Optional['SiteModel']:
        return cls.query.filter_by(url=url).first()

    @classmethod
    def find_all(cls) -> List['SiteModel']:
        return cls.query.all()

    def save(self) -> None:
        """Adiciona ou atualiza o site no banco."""
        banco.session.add(self)
        banco.session.commit()

    def delete(self) -> None:
        """Remove o site (e cascata de hotéis)."""
        banco.session.delete(self)
        banco.session.commit()