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
    
        if self.cleaned_data.get('tempo_check') <= 0 or self.cleaned_data.get('tempo_check') >59:
            raise forms.ValidationError('Instervalo de tempo não permitido!')

        return self.cleaned_data

    # def clean(self):

    #     if self.cleaned_data.get('tempo_check') <= 0 or self.cleaned_data.get('tempo_check') >59:
    #         raise forms.ValidationError('Instervalo de tempo não permitido!')

    #     return self.cleaned_data

class AssetListForm(forms.ModelForm):
   
    class Meta:
        model = AssetList
        fields = ['nome', 'bolsa']

    