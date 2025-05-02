from flask_restful import Resource, reqparse
from models.hotel import HotelModel

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("nome", type=str, required=True, help="O campo 'nome' é obrigatório.")
    argumentos.add_argument("estrelas", type=float, required=True, help="O campo 'estrelas' é obrigatório.")
    argumentos.add_argument("diaria", type=float, required=True, help="O campo 'diaria' é obrigatório.")
    argumentos.add_argument("cidade", type=str, required=True, help="O campo 'cidade' é obrigatório.")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {"message": "Hotel não encontrado."}, 404

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": f"Hotel id '{hotel_id}' já existe."}, 400

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {"message": "Erro interno ao salvar hotel."}, 500
        return hotel.json(), 201

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            return hotel_encontrado.json(), 200

        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {"message": "Erro ao tentar salvar hotel."}, 500
        return hotel.json(), 201

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.delete_hotel()
            return {"message": "Hotel deletado com sucesso."}
        return {"message": "Hotel não encontrado."}, 404

class Hoteis(Resource):
    def get(self):
        return {"hoteis": [hotel.json() for hotel in HotelModel.get_all()]}
