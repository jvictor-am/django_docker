# data_loader/models.py
from django.db import models

class DataRecord(models.Model):
    nome = models.CharField(max_length=255)
    idade = models.IntegerField()
    cep = models.CharField(max_length=10)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    uf = models.CharField(max_length=255, null=True, blank=True)
    regiao = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nome


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name