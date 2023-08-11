from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Asset
from django.shortcuts import render, get_object_or_404, redirect
from .models import Asset, AssetList
from django.contrib.auth.decorators import login_required
from .forms import AssetForm
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
    # hist_price = HistoricalPrice.objects.filter(asset=asset.nome).order_by('data')
    hist_price = []

    
    return render(request, 'asset_detail.html', {'asset': asset,'hist_price':hist_price})


