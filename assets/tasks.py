# projeto_acoes/tasks.py

from celery import shared_task
from assets.models import Asset, HistoricalPrice, AssetList
import requests
from datetime import datetime
import yfinance as yf
import pytz
from django.core.mail import send_mail
from core import settings

@shared_task
def obter_e_salvar_cotacoes():

    assets_list = AssetList.objects.filter(id__in = Asset.objects.filter(deleteted_at__isnull = True).values('asset').distinct())
    symbols_name = ['.'.join([ativo.nome,ativo.bolsa]) for ativo in assets_list]
    data_last_insert = HistoricalPrice.objects.order_by('-data').first()

    if len(symbols_name) > 0:

        data = yf.download(symbols_name, period='1d', interval='1m')
        df_reset = data.reset_index()

        max_datetime = df_reset['Datetime'].max()

        if ((data_last_insert == None) or (data_last_insert.data < max_datetime)) and len(data) > 0 :
            
            if len(symbols_name)> 1:

                values = data['Close'][symbols_name].values[-1]
            else:
                values = [data['Close'].values[-1]]

            symbols_name_insert = [name.split('.')[0] for name in symbols_name]

            # Create a list of HistoricalPrice instances from the data
            historical_price_instances = []
            for name, price in zip(symbols_name_insert,values):
                asset_item = AssetList.objects.filter(nome = name)
                if len(asset_item)>0:
                    asset_list = asset_item[0]
                    hist = HistoricalPrice(assetList = asset_list, preco = price, data = max_datetime )
                    hist.save()
                    historical_price_instances.append(hist)



    return "success"

@shared_task
def envio_email_cliente():

    today = datetime.now()
    time_min = today.minute
    assets = Asset.objects.filter(deleteted_at__isnull = True)

    list_checks = [asset for asset in assets if time_min%asset.tempo_check == 0]
    list_checks_assetList = list(set([asset.asset for asset in assets]))

    sp_timezone = pytz.timezone('America/Sao_Paulo')

    queryset_list = list(HistoricalPrice.objects.filter(assetList__in = list_checks_assetList).order_by('-data'))
    dict_max_values = {}
    for asset_list in queryset_list:
        if asset_list.assetList not in dict_max_values.keys():
            dict_max_values[asset_list.assetList] = asset_list

    for asset in assets:

        hist_price = dict_max_values[asset.asset]
        if asset.preco_maximo <= hist_price.preco:
            to_email=asset.user.email
            nome_asset = asset.asset.nome
            mail_subject = 'Aviso de preço!'
            message = '{} atingiu o preço mmáximo definido.'.format(nome_asset)
            send_mail(subject= mail_subject,message=message,from_email=settings.EMAIL_HOST_USER,recipient_list=[to_email],fail_silently=True,)
        if asset.preco_minimo >= hist_price.preco:
            to_email=asset.user.email
            nome_asset = asset.asset.nome
            mail_subject = 'Aviso de preço!'
            message = '{} atingiu o preço mínimo definido.'.format(nome_asset)
            send_mail(
                subject= mail_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=True,
            )


    
    return "success"


    


            

            
