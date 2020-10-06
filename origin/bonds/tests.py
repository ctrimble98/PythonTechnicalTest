from rest_framework.test import APITestCase
from .models import Bond


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

    def test_bonds(self):
        resp = self.client.get("/bonds/")
        assert resp.status_code == 200

    def test_post(self):

        self.client.post("/bonds/", self.example_bond, format="json")
        assert Bond.objects.get(isin="FR0000131104").legal_name == "BNPPARIBAS"

    def test_post_bad_lei(self):
        self.client.post("/bonds/", self.example_bond, format="json")
        assert Bond.objects.get(isin="TEST00131104").legal_name == "BNPPARIBAS"
