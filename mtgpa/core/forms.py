from django import forms


class CardsForm(forms.Form):
    cards = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 25}))
