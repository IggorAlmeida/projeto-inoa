from django import forms
from .models import Asset, AssetList

class AssetForm(forms.ModelForm):
    asset_select = forms.ModelChoiceField(queryset=AssetList.objects.all())
    class Meta:
        model = Asset
        fields = ['preco_maximo', 'preco_minimo','tempo_check']


    def clean(self):
        preco_maximo = self.cleaned_data.get('preco_maximo')
        preco_minimo = self.cleaned_data.get('preco_minimo')

        if preco_maximo and preco_minimo and preco_maximo <= preco_minimo:
            raise forms.ValidationError('Preço mínimo maior ou igual ao preço máximo!')

        return self.cleaned_data
    