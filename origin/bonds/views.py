from rest_framework.views import APIView
from rest_framework.response import Response
import requests

from .serializers import BondSerializer
from.models import Bond


class HelloWorld(APIView):
    def get(self, request):
        return Response("Hello World!")


class BondView(APIView):
    def get(self, request):

        return Response("Hello World!")

    def post(self, request):
        lei = request.data['lei']

        lei_request = requests.get('https://leilookup.gleif.org/api/v2/leirecords?lei=' + lei)

        if lei_request.status_code == 200:

            legal_name = lei_request.json()['Entity']['LegalName']['$']

            return Response(legal_name)

        else:
            return Response('HTTP status code: ' + str(lei_request.status_code) + ' - ' + lei_request.json()['message'])
