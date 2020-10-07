from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from rest_framework import status

from .serializers import BondSerializer
from .models import Bond
from rest_framework.permissions import IsAuthenticated


class BondView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):

        bonds = Bond.objects.all().filter(username=request.user.username)

        if len(bonds) is 0:
            return Response("No bonds for this user found", status=status.HTTP_404_NOT_FOUND)

        return Response({'bonds': bonds})

    def post(self, request):

        data = request.data

        lei_request = requests.get('https://leilookup.gleif.org/api/v2/leirecords?lei=' + data['lei'])

        if lei_request.status_code == 200:

            if len(lei_request.json()) > 0:

                legal_name = lei_request.json()[0]['Entity']['LegalName']['$']

                data['legal_name'] = legal_name.replace(" ", "")
                data['username'] = request.user.username

                serializer = BondSerializer(data=data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response("Invalid LEI", status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        else:
            return Response('HTTP status code: ' + str(lei_request.status_code) + ' - ' + lei_request.json()['message'])
