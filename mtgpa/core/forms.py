from django import forms


class CardsForm(forms.Form):
    cards = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 25}), required=True, label='Cartas')
    precision = forms.IntegerField(min_value=1, max_value=500, initial='10', required=False, label='Precisão de preço')