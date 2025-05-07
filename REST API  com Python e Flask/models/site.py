from typing import List, Optional
from sql_alchemy import banco

class SiteModel(banco.Model):
    __tablename__ = 'sites'

    site_id = banco.Column(banco.Integer, primary_key=True, autoincrement=True)
    nome    = banco.Column(banco.String(80), nullable=False)
    url     = banco.Column(banco.String(200), nullable=False, unique=True)

    # == relação 1→N: um site tem muitos hotéis ==
    hoteis = banco.relationship(
        'HotelModel',
        back_populates='site',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __init__(self, nome: str, url: str):
        self.nome = nome
        self.url  = url

    def json(self, include_hoteis: bool = True) -> dict:
        """
        Retorna dict do site. Se include_hoteis=True,
        inclui também a lista de hotéis.
        """
        data = {
            'site_id': self.site_id,
            'nome':    self.nome,
            'url':     self.url,
        }
        if include_hoteis:
            data['hoteis'] = [h.json() for h in self.hoteis.all()]
        return data

    @classmethod
    def find_by_id(cls, site_id: int) -> Optional['SiteModel']:
        return cls.query.get(site_id)

    @classmethod
    def find_by_url(cls, url: str) -> Optional['SiteModel']:
        """
        Procura um site pela URL exata.
        Usado por GET /sites/<url>/hoteis.
        """
        return cls.query.filter_by(url=url).first()

    @classmethod
    def find_all(cls) -> List['SiteModel']:
        return cls.query.all()

    def save(self) -> None:
        """Salva (insert ou update) este site no banco."""
        banco.session.add(self)
        banco.session.commit()

    def delete(self) -> None:
        """Deleta este site (e cascata de hotéis)."""
        banco.session.delete(self)
        banco.session.commit()
