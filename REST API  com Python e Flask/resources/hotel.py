from flask_restful import Resource, reqparse
from models.hotel import HotelModel

# Parser para filtros de busca via query string
filtro_hoteis = reqparse.RequestParser()
filtro_hoteis.add_argument("cidade", type=str, location="args")
filtro_hoteis.add_argument("estrelas_min", type=float, default=0, location="args")
filtro_hoteis.add_argument("estrelas_max", type=float, default=5, location="args")
filtro_hoteis.add_argument("diaria_min", type=float, default=0, location="args")
filtro_hoteis.add_argument("diaria_max", type=float, default=10000, location="args")
filtro_hoteis.add_argument("limit", type=int, default=50, location="args")
filtro_hoteis.add_argument("offset", type=int, default=0, location="args")

class Hoteis(Resource):
    def get(self):
        # Parseia apenas argumentos da URL; não há request.get_json() aqui
        args = filtro_hoteis.parse_args()

        # Constrói query dinâmica com SQLAlchemy
        query = HotelModel.query \
            .filter(HotelModel.estrelas >= args["estrelas_min"],
                    HotelModel.estrelas <= args["estrelas_max"],
                    HotelModel.diaria >= args["diaria_min"],
                    HotelModel.diaria <= args["diaria_max"])
        if args["cidade"]:
            query = query.filter_by(cidade=args["cidade"])

        hoteis = query.limit(args["limit"]).offset(args["offset"]).all()
        return {"hoteis": [h.json() for h in hoteis]}, 200


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("nome", type=str, required=True, help="O campo 'nome' é obrigatório.")
    argumentos.add_argument("estrelas", type=float, required=True, help="O campo 'estrelas' é obrigatório.")
    argumentos.add_argument("diaria", type=float, required=True, help="O campo 'diaria' é obrigatório.")
    argumentos.add_argument("cidade", type=str, required=True, help="O campo 'cidade' é obrigatório.")

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
            hotel.update_hotel(**dados)
            return hotel.json(), 200

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
