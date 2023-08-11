from django.contrib import admin
from .models import AssetList, Asset, HistoricalPrice

# Register your models here.
admin.site.register(AssetList)
admin.site.register(Asset)
admin.site.register(HistoricalPrice)