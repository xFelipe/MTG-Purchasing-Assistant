from django.shortcuts import render
from .forms import CardsForm
from re import match

# https://ligamagic.net/?view=cards%2Fsearch&card=birds+of+paradise
# https://ligamagic.net/?view=cards%2Fsearch&card=aether+Vial
# https://ligamagic.net/?view=cards/card&card=Rancor
# m = match(r'((?P<qnt>\d*)(x|X){0,1}){0,1}( ){0,1}(?P<card_name>.*)', '123x Gelatinous Genesis')
# m = match(r'((?P<qnt>\d*)(x|X)?)?( )?(?P<card_name>.*)', '1x Gelatinous Genesis')
# Create your views here.
link_base = 'https://ligamagic.net/?view=cards/card&card='


def home(request):
    if request.method != 'POST':
        return render(request, 'home.html', {'form': CardsForm()})
    else:
        cards = []
        content = request.POST['cards'].split('\r\n')
        for line in content:
            cards.append((line, link_engine(line), ))
        return render(request, 'home.html', {'cards': cards, 'form': CardsForm(request.POST)})


def link_engine(cardname):
    return link_base+str(cardname)


def line_interpreter(line):
    m = match(r'((?P<qnt>\d*)(x|X)?)?( )?(?P<card_name>.*)', line)
    g_dict = m.groupdict()
    if not g_dict['qnt']:
        g_dict['qnt'] = 1
    else:
        g_dict['qnt'] = int(g_dict['qnt'])

    return g_dict
