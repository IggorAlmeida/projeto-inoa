# projeto_acoes/tasks.py

from celery import shared_task
from assets.models import Asset, HistoricalPrice, AssetList
import requests
from datetime import datetime
import yfinance as yf

def format_b3_symbol(symbol):
    # Formata o símbolo da ação para o formato aceito pelo Yahoo Finance para a B3.
    # Adiciona '.SA' ao final do símbolo para especificar a bolsa brasileira.
    return f"{symbol}.SA"

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
            
            #symbols_name = [format_b3_symbol(nome.get('asset')) for nome in Asset.objects.filter(deleteted_at__isnull = True).values('asset','tempo_check').distinct() if total_minutes % nome.get('tempo_check') == 0 ]

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


    # initial_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day,10,0)
    # now_time = datetime.now().replace(second=0, microsecond=0)
    # assets_list = AssetList.objects.filter(id__in = Asset.objects.filter(deleteted_at__isnull = True).values('asset').distinct())
    # symbols = [format_b3_symbol(ativo.nome) for ativo in assets_list]
    # data_last_insert = HistoricalPrice.objects.order_by('-data').first()
    # assets = Asset.objects.filter(deleteted_at__isnull = True)
    # assets_l = Asset.objects.filter(deleteted_at__isnull = True).values('asset').distinct()
    #symbols = [format_b3_symbol(ativo.get('asset')) for ativo in Asset.objects.filter(deleteted_at__isnull = True).values('asset','tempo_check').distinct()]
    
    # if len(symbols) > 0:

    #     data = yf.download(symbols, period='1d', interval='1m')
    #     df_reset = data.reset_index()

    #     max_datetime = df_reset['Datetime'].max()
    #     # min_datetime = df_reset['Datetime'].min()

    #     # total_minutes = (max_datetime.hour*60-max_datetime.minute) - (min_datetime.hour*60-min_datetime.minute)

    #     if (data_last_insert == None) or (data_last_insert.data < max_datetime):
            
    #         symbols_name = symbols#[format_b3_symbol(nome.get('asset')) for nome in Asset.objects.filter(deleteted_at__isnull = True).values('asset','tempo_check').distinct() if total_minutes % nome.get('tempo_check') == 0 ]

    #         values = data['Close'][symbols_name].values[-1]

    #         symbols_name_insert = [name.split('.')[0] for name in symbols_name]

    #         # Create a list of HistoricalPrice instances from the data
    #         historical_price_instances = []
    #         for name, price in zip(symbols_name_insert,values):
    #             hist = HistoricalPrice(asset = name, preco = price, data = max_datetime )
    #             hist.save()
    #             historical_price_instances.append(hist)

    return "success"

@shared_task
def envio_email_cliente():
    pass


            

            
