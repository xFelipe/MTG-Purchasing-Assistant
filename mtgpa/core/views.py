from django.shortcuts import render
from .forms import CardsForm
from re import match
from bs4 import BeautifulSoup
import requests

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
        market = dict()
        for line in content:
            if not line:
                continue

            interpreted_line = line_interpreter(line)

            stores_have = market_search(interpreted_line['card_name'])
            for store in stores_have:
                try:
                    market[store].append(interpreted_line['card_name'])
                except:
                    market[store] = [interpreted_line['card_name']]

            cards.append((interpreted_line['qnt'],
                          interpreted_line['card_name'],
                          link_engine(interpreted_line['card_name'])))
        return render(request, 'home.html', {'cards': cards, 'form': CardsForm(request.POST), 'markets': sort_market(market)},)


def link_engine(cardname):
    return link_base+str(cardname)


def sort_market(market):
    d = dict()
    for key in sorted(market, key=lambda key: len(market[key]), reverse=True):
        d[key] = market[key][:]
    return d


def line_interpreter(line):
    m = match(r'((?P<qnt>\d*)(x|X)?)?( )?(?P<card_name>.*)', line)
    g_dict = m.groupdict()
    if not g_dict['qnt']:
        g_dict['qnt'] = 1
    else:
        g_dict['qnt'] = int(g_dict['qnt'])
    return g_dict


def market_search(card_name):
    r = requests.get('https://ligamagic.net/?view=cards/card&card={}'.format(card_name))
    text = r.text
    soup = BeautifulSoup(text, 'lxml')
    result = soup.find_all('div', class_='estoque-linha primeiro', mp=2) + \
             soup.find_all('div', class_='estoque-linha', mp=2)
    result = list(map(lambda x: x.find_all('img'), result))  # Pegar nome
    result = list(map(lambda x: x[0], result))
    markets = list(map(lambda x: x['title'], result))

    return tuple(set(markets))[:]
