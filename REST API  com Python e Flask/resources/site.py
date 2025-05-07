from flask import request
from flask_restful import Resource
from models.site import SiteModel

class Sites(Resource):
    def get(self):
        """GET /sites — lista todos os sites"""
        sites = SiteModel.find_all()
        return {'sites': [s.json() for s in sites]}, 200

    def post(self):
        """POST /sites — cria um novo site"""
        if not request.is_json:
            return {"message": "Envie JSON e defina Content-Type: application/json"}, 400

        data = request.get_json(force=True)
        nome = data.get('nome')
        url  = data.get('url')

        if not nome or not url:
            return {"message": "Campos 'nome' e 'url' são obrigatórios."}, 400

        if SiteModel.find_by_url(url):
            return {"message": f"URL '{url}' já cadastrada."}, 400

        site = SiteModel(nome=nome, url=url)
        try:
            site.save()
            return site.json(), 201
        except Exception as e:
            return {"message": "Erro ao salvar site.", "erro": str(e)}, 500

class Site(Resource):
    def get(self, site_id):
        """GET /sites/<site_id> — detalhes de um site"""
        site = SiteModel.find_by_id(site_id)
        if site:
            return site.json(), 200
        return {"message": "Site não encontrado."}, 404

    def put(self, site_id):
        """PUT /sites/<site_id> — atualiza ou cria um site"""
        if not request.is_json:
            return {"message": "Envie JSON e defina Content-Type: application/json"}, 400

        data = request.get_json(force=True)
        nome = data.get('nome')
        url  = data.get('url')

        if not nome or not url:
            return {"message": "Campos 'nome' e 'url' são obrigatórios."}, 400

        existente = SiteModel.find_by_url(url)
        site = SiteModel.find_by_id(site_id)

        # Atualizar existente
        if site:
            if existente and existente.site_id != site_id:
                return {"message": f"URL '{url}' em uso por outro site."}, 400
            site.nome = nome
            site.url  = url
            try:
                site.save()
                return site.json(), 200
            except Exception as e:
                return {"message": "Erro ao atualizar site.", "erro": str(e)}, 500

        # Criar novo
        if existente:
            return {"message": f"URL '{url}' já cadastrada."}, 400
        novo = SiteModel(nome=nome, url=url)
        try:
            novo.save()
            return novo.json(), 201
        except Exception as e:
            return {"message": "Erro ao criar site.", "erro": str(e)}, 500

    def delete(self, site_id):
        """DELETE /sites/<site_id> — remove site e hotéis relacionados"""
        site = SiteModel.find_by_id(site_id)
        if not site:
            return {"message": "Site não encontrado."}, 404
        try:
            site.delete()
            return {"message": "Site e hotéis excluídos com sucesso."}, 200
        except Exception as e:
            return {"message": "Erro ao excluir site.", "erro": str(e)}, 500

class HoteisPorSite(Resource):
    def get(self, url):
        """
        GET /sites/<url>/hoteis
        Retorna todos os hotéis do site cuja URL foi passada.
        """
        site = SiteModel.find_by_url(url)
        if not site:
            return {"message": "Site não encontrado."}, 404

        hoteis = [h.json() for h in site.hoteis.all()]
        return {"site": site.url, "hoteis": hoteis}, 200
