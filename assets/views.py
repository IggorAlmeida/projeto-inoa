from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Asset
from django.shortcuts import render, get_object_or_404, redirect
from .models import Asset, AssetList, HistoricalPrice
from django.contrib.auth.decorators import login_required
from .forms import AssetForm, AssetListForm
from django.utils.timezone import now
from datetime import datetime

# Create your views here.
@login_required
def asset_list(request):
    assets = Asset.objects.filter(user=request.user, deleteted_at__isnull = True)
    if request.method == 'POST':
        # A comment was posted
        asset_form = AssetForm(data=request.POST)

        if asset_form.is_valid():
            # Create Comment object but don't save to database yet
            new_assent = asset_form.save(commit=False)
            # Assign the current post to the comment
            new_assent.user = request.user
            # Save the comment to the database

            pklist = request.POST.get('asset_select')
            asset = get_object_or_404(AssetList, pk=pklist)
            new_assent.asset = asset

            new_assent.save()
    else:
        asset_form = AssetForm()

    return render(request, 'asset_list.html', {'asset_form': asset_form,'assets':assets,'section':'assets'})

# @login_required
# def asset_create(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         Asset.objects.create(name=name, user=request.user)
#         return redirect('asset_list')
#     return render(request, 'asset_create.html')

@login_required
def asset_update(request, pk):
    asset = get_object_or_404(Asset, pk=pk, user=request.user)
    if request.method == 'POST':
        # asset.nome = request.POST['asset_name']
        asset.preco_maximo = request.POST['max_price']
        asset.preco_minimo = request.POST['min_price']
        asset.tempo_check = request.POST['tempo_check']
        asset.save()
        return redirect('assets:list')
    return render(request, 'asset_update.html', {'asset': asset})

@login_required
def asset_delete(request, pk):
    asset = get_object_or_404(Asset, pk=pk, user=request.user)
    if request.method == 'POST':
        asset.deleteted_at = str(datetime.now())
        asset.save()
        return redirect('assets:list')
    return render(request, 'asset_delete.html', {'asset': asset})

@login_required
def asset_detail(request, pk):
    asset = get_object_or_404(Asset, user = request.user, id = pk, deleteted_at__isnull = True)
    hist_price = HistoricalPrice.objects.filter(assetList = asset.asset).order_by('-data')

    return render(request, 'asset_detail.html', {'asset': asset,'hist_price':hist_price})

@login_required
def assetList_list(request):
    assetsList = AssetList.objects.all()
    if request.method == 'POST':
        # A comment was posted
        assetList_form = AssetListForm(data=request.POST)

        if assetList_form.is_valid():
            # Create Comment object but don't save to database yet
            new_assent = assetList_form.save(commit=False)

            new_assent.save()
    else:
        assetList_form = AssetListForm()

    return render(request, 'assetList_list.html', {'asset_form': assetList_form,'assets':assetsList,'section':'assets'})



