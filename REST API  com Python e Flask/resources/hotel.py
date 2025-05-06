from flask_restful import Resource, reqparse
from models.hotel import HotelModel

# Parser para filtros de busca via query string
filtro_hoteis = reqparse.RequestParser()
filtro_hoteis.add_argument("cidade",       type=str,   location="args")
filtro_hoteis.add_argument("estrelas_min", type=float, location="args", default=0)
filtro_hoteis.add_argument("estrelas_max", type=float, location="args", default=5)
filtro_hoteis.add_argument("diaria_min",   type=float, location="args", default=0)
filtro_hoteis.add_argument("diaria_max",   type=float, location="args", default=10000)
filtro_hoteis.add_argument("site_id",      type=int,   location="args")
filtro_hoteis.add_argument("limit",        type=int,   location="args", default=50)
filtro_hoteis.add_argument("offset",       type=int,   location="args", default=0)

class Hoteis(Resource):
    def get(self):
        """
        GET /hoteis
        Retorna lista de hotéis, aplicando filtros avançados via query string:
          - cidade, estrelas_min, estrelas_max, diaria_min, diaria_max, site_id, limit, offset
        """
        args = filtro_hoteis.parse_args()

        # Monta query dinâmica com SQLAlchemy
        query = HotelModel.query \
            .filter(HotelModel.estrelas >= args["estrelas_min"],
                    HotelModel.estrelas <= args["estrelas_max"],
                    HotelModel.diaria  >= args["diaria_min"],
                    HotelModel.diaria  <= args["diaria_max"] )
        if args["cidade"]:
            query = query.filter_by(cidade=args["cidade"])
        if args.get("site_id") is not None:
            query = query.filter_by(site_id=args["site_id"])

        # Paginação
        hoteis = query.limit(args["limit"]).offset(args["offset"]).all()
        return {"hoteis": [hotel.json() for hotel in hoteis]}, 200


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("nome",     type=str, required=True, help="O campo 'nome' é obrigatório.")
    argumentos.add_argument("estrelas", type=float, required=True, help="O campo 'estrelas' é obrigatório.")
    argumentos.add_argument("diaria",   type=float, required=True, help="O campo 'diaria' é obrigatório.")
    argumentos.add_argument("cidade",   type=str, required=True, help="O campo 'cidade' é obrigatório.")
    argumentos.add_argument("site_id",  type=int, required=False, help="Associa o hotel a um site (opcional).")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json(), 200
        return {"message": "Hotel não encontrado."}, 404

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": f"Hotel id '{hotel_id}' já existe."}, 400

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
            return hotel.json(), 201
        except Exception as e:
            return {"message": "Erro interno ao salvar hotel.", "erro": str(e)}, 500

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            # Atualiza todos os campos, inclusive site_id
            hotel.update_hotel(**dados)
            return hotel.json(), 200

        # Cria novo hotel se não existir
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
            return hotel.json(), 201
        except Exception as e:
            return {"message": "Erro ao tentar salvar hotel.", "erro": str(e)}, 500

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.delete_hotel()
            return {"message": "Hotel deletado com sucesso."}, 200
        return {"message": "Hotel não encontrado."}, 404
