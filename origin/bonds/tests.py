from django.db.backends import sqlite3
from rest_framework.test import APITestCase
from .models import Bond
from django.contrib.auth.models import User
from rest_framework.test import APIClient

import json


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

    # Test for a post request with a valid bond with a valid lei
    def test_post(self):

        client = APIClient()
        client.force_authenticate(user=self.test_user1)

        resp = client.post("/bonds/", self.example_bond, format="json",)
        assert resp.status_code == 201 and Bond.objects.get(isin=self.example_bond['isin']).legal_name == "BNPPARIBAS"

    # Test for a post request with a bond with a invalid lei
    def test_post_bad_lei(self):

        client = APIClient()
        client.force_authenticate(user=self.test_user1)

        resp = client.post("/bonds/", self.wrong_lei_bond, format="json", )

        assert resp.status_code == 422 and not Bond.objects.filter(isin=self.wrong_lei_bond['isin']).exists()

    # Test for a valid get
    def test_get(self):

        client = APIClient()
        client.force_authenticate(user=self.test_user1)
        client.post("/bonds/", self.example_bond, format="json", )

        resp = client.get("/bonds/")
        data = json.loads(resp.data)
        assert resp.status_code == 200 and data[0]['fields']['isin'] == self.example_bond['isin']

    # Test get with no bonds
    def test_get_no_bonds(self):

        client = APIClient()
        client.force_authenticate(user=self.test_user1)

        resp = client.get("/bonds/")
        assert resp.status_code == 404

    # Test that filtering occurs for users
    def test_get_only_users_bonds(self):

        client = APIClient()
        client.force_authenticate(user=self.test_user1)
        client.post("/bonds/", self.example_bond, format="json", )

        test_user2 = User.objects.create_user(username="testuser2", password="testpass321!")
        client = APIClient()
        client.force_authenticate(user=test_user2)
        client.post("/bonds/", self.example_bond, format="json", )

        resp = client.get("/bonds/")
        data = json.loads(resp.data)
        assert resp.status_code == 200 and len(data) == 1
