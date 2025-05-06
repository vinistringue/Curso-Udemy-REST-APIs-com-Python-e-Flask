from flask import request
from flask_restful import Resource
from models.site import SiteModel


class Sites(Resource):
    def get(self):
        """GET /sites - Lista todos os sites"""
        sites = SiteModel.find_all()
        return {'sites': [site.json() for site in sites]}, 200

    def post(self):
        """POST /sites - Cria um novo site"""
        if not request.is_json:
            return {"message": "Requisição sem JSON ou 'Content-Type' incorreto."}, 400

        try:
            data = request.get_json(force=True)
        except Exception as e:
            return {"message": "Erro ao decodificar JSON.", "erro": str(e)}, 400

        nome = data.get('nome')
        url = data.get('url')

        if not nome or not url:
            return {"message": "Campos 'nome' e 'url' são obrigatórios."}, 400

        if SiteModel.find_by_url(url):
            return {"message": f"URL '{url}' já está cadastrada."}, 400

        novo_site = SiteModel(nome=nome, url=url)
        try:
            novo_site.save()
            return novo_site.json(), 201
        except Exception as e:
            return {"message": "Erro ao salvar no banco de dados.", "erro": str(e)}, 500


class Site(Resource):
    def get(self, site_id):
        """GET /sites/<site_id> - Retorna dados do site com seus hotéis"""
        site = SiteModel.find_by_id(site_id)
        if site:
            return site.json(), 200
        return {"message": "Site não encontrado."}, 404

    def put(self, site_id):
        """PUT /sites/<site_id> - Atualiza ou cria um novo site"""
        if not request.is_json:
            return {"message": "Requisição sem JSON ou 'Content-Type' incorreto."}, 400

        try:
            data = request.get_json(force=True)
        except Exception as e:
            return {"message": "Erro ao decodificar JSON.", "erro": str(e)}, 400

        nome = data.get('nome')
        url = data.get('url')

        if not nome or not url:
            return {"message": "Campos 'nome' e 'url' são obrigatórios."}, 400

        site_existente = SiteModel.find_by_url(url)
        site = SiteModel.find_by_id(site_id)

        if site:
            # Atualiza site existente
            if site_existente and site_existente.site_id != site_id:
                return {"message": f"URL '{url}' já está em uso por outro site."}, 400

            site.nome = nome
            site.url = url
            try:
                site.save()
                return site.json(), 200
            except Exception as e:
                return {"message": "Erro ao atualizar site.", "erro": str(e)}, 500

        # Cria novo site se não existir
        if site_existente:
            return {"message": f"URL '{url}' já está cadastrada."}, 400

        novo_site = SiteModel(nome=nome, url=url)
        try:
            novo_site.save()
            return novo_site.json(), 201
        except Exception as e:
            return {"message": "Erro ao criar novo site.", "erro": str(e)}, 500

    def delete(self, site_id):
        """DELETE /sites/<site_id> - Remove site e hotéis relacionados"""
        site = SiteModel.find_by_id(site_id)
        if site:
            try:
                site.delete()
                return {"message": "Site e hotéis associados excluídos com sucesso."}, 200
            except Exception as e:
                return {"message": "Erro ao excluir site.", "erro": str(e)}, 500
        return {"message": "Site não encontrado."}, 404
