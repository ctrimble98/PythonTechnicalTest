from django.db import models


class Bond(models.Model):

    isin = models.CharField(max_length=12)
    size = models.IntegerField()
    currency = models.CharField(max_length=3)
    maturity = models.DateField()
    lei = models.CharField(max_length=20)
    legal_name = models.CharField(max_length=60)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
