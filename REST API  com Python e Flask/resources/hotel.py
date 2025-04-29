from flask_restful import Resource, reqparse
from models.hotel import HotelModel

class Hoteis(Resource):
    def get(self):
        """
        Retorna uma lista de todos os hotéis cadastrados no banco de dados.
        """
        hoteis = [hotel.json() for hotel in HotelModel.query.all()]
        return {"hoteis": hoteis}


class Hotel(Resource):
    # Parser para validar e extrair os dados enviados na requisição
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("nome", type=str, required=True, help="O campo 'nome' é obrigatório.")
    argumentos.add_argument("estrelas", type=float, required=True, help="O campo 'estrelas' é obrigatório.")
    argumentos.add_argument("diaria", type=float, required=True, help="O campo 'diaria' é obrigatório.")
    argumentos.add_argument("cidade", type=str, required=True, help="O campo 'cidade' é obrigatório.")

    def get(self, hotel_id):
        """
        Busca um hotel pelo ID.
        Retorna os dados do hotel caso encontrado, senão retorna 404.
        """
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {"message": "Hotel não encontrado."}, 404

    def post(self, hotel_id):
        """
        Cadastra um novo hotel. O ID deve ser único.
        Retorna 400 se já existir um hotel com o mesmo ID.
        """
        if HotelModel.find_hotel(hotel_id):
            return {"message": f"Hotel ID '{hotel_id}' já existe."}, 400

        dados = Hotel.argumentos.parse_args()
        novo_hotel = HotelModel(hotel_id, **dados)

        try:
            novo_hotel.save_hotel()
            return novo_hotel.json(), 201
        except Exception as e:
            return {"message": f"Erro ao salvar hotel: {str(e)}"}, 500

    def put(self, hotel_id):
        """
        Atualiza um hotel existente ou cria um novo caso o ID não exista.
        """
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            # Atualiza os dados do hotel existente
            hotel_encontrado.nome = dados["nome"]
            hotel_encontrado.estrelas = dados["estrelas"]
            hotel_encontrado.diaria = dados["diaria"]
            hotel_encontrado.cidade = dados["cidade"]
            hotel = hotel_encontrado
        else:
            # Cria um novo hotel com o ID informado
            hotel = HotelModel(hotel_id, **dados)

        try:
            hotel.save_hotel()
            return hotel.json(), 200
        except Exception as e:
            return {"message": f"Erro ao atualizar/salvar hotel: {str(e)}"}, 500

    def delete(self, hotel_id):
        """
        Deleta um hotel pelo ID.
        Retorna 404 se o hotel não for encontrado.
        """
        hotel = HotelModel.find_hotel(hotel_id)
        if not hotel:
            return {"message": "Hotel não encontrado."}, 404

        try:
            hotel.delete_hotel()
            return {"message": "Hotel excluído com sucesso."}, 200
        except Exception as e:
            return {"message": f"Erro ao deletar hotel: {str(e)}"}, 500
