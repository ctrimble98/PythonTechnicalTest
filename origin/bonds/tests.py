from django.db.backends import sqlite3
from rest_framework.test import APITestCase
from .models import Bond
from django.contrib.auth.models import User
from rest_framework.test import APIClient


class BondTest(APITestCase):

    example_bond = {
            "isin": "FR0000131104",
            "size": 100000000,
            "currency": "EUR",
            "maturity": "2025-02-28",
            "lei": "R0MUWSFPU8MPRO8K5P83"
    }

    wrong_lei_bond = {
        "isin": "TEST00131104",
        "size": 100000000,
        "currency": "EUR",
        "maturity": "2025-02-28",
        "lei": "TESTWRONGLEI00000000"
    }

    if not User.objects.filter(username="testuser1").exists():
        test_user1 = User.objects.create_user(username="testuser1", password="testpass123!")
    else:
        test_user1 = User.objects.get_by_natural_key(username="testuser1")

    def test_post(self):
        client = APIClient()
        client.force_authenticate(user=self.test_user1)

        # print({**self.example_bond, **self.test_user1})
        resp = client.post("/bonds/", self.example_bond, format="json",)
        print(resp.status_code)
        assert resp.status_code == 201 and Bond.objects.get(isin="FR0000131104").legal_name == "BNPPARIBAS"

    def test_post_bad_lei(self):
        client = APIClient()
        client.force_authenticate(user=self.test_user1)
        # print({**self.example_bond, **self.test_user1})
        client.post("/bonds/", self.wrong_lei_bond, format="json", )
        assert Bond.objects.get(isin=self.wrong_lei_bond['lei']).legal_name == "BNPPARIBAS"

    def test_get(self):

        client = APIClient()
        client.force_authenticate(user=self.test_user1)

        resp = client.get("/bonds/")
        assert resp.status_code == 200
