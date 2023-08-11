from django.db import models
from django.conf import settings
from django.urls import reverse

DEFAULT_ASSET_LIST_ID = 1


class AssetList(models.Model):
    nome = models.CharField(max_length=100)
    bolsa = models.CharField(max_length=5)

    def __str__(self):
        return self.nome

# Create your models here.
class Asset(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    asset = models.ForeignKey(AssetList,on_delete=models.CASCADE, default=DEFAULT_ASSET_LIST_ID)
    preco_maximo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    tempo_check = models.IntegerField()
    deleteted_at =  models.DateTimeField(null=True)

    def __str__(self):
        return self.asset.nome
    
    def get_absolute_url(self):
        return reverse('assets:asset_detail', args=[self.id])
    
class HistoricalPrice(models.Model):
    assetList = models.ForeignKey(AssetList,on_delete=models.CASCADE, default=DEFAULT_ASSET_LIST_ID)
    data = models.DateTimeField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.assetList.nome} - {self.data}"