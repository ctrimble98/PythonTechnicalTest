from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from rest_framework import status

from .serializers import BondSerializer
from .models import Bond
from django.contrib.auth import authenticate


class BondView(APIView):
    def get(self, request):

        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:

            bonds = Bond.objects.all().filter(user=user)
            return Response({'bonds': bonds})

    def post(self, request):

        print(request.data)
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:

            data = request.data

            lei_request = requests.get('https://leilookup.gleif.org/api/v2/leirecords?lei=' + data['lei'])

            if lei_request.status_code == 200:

                if len(lei_request.json()) > 0:

                    legal_name = lei_request.json()[0]['Entity']['LegalName']['$']

                    data['legal_name'] = legal_name.replace(" ", "")
                    data['user'] = user

                    serializer = BondSerializer(data=data)

                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response()

            else:
                return Response('HTTP status code: ' + str(lei_request.status_code) + ' - ' + lei_request.json()['message'])
