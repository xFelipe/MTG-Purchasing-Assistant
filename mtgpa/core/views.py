from django.shortcuts import render

# https://ligamagic.net/?view=cards%2Fsearch&card=birds+of+paradise
# https://ligamagic.net/?view=cards%2Fsearch&card=aether+Vial
# https://ligamagic.net/?view=cards/card&card=Rancor
# Create your views here.


def home(request):
    cards = ' '
    if request.method == 'POST':
        cards = request.POST['cards']
    return render(request, 'home.html', {'cards': cards})

