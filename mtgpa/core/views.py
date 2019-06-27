from django.shortcuts import render

# https://ligamagic.net/?view=cards%2Fsearch&card=birds+of+paradise
# https://ligamagic.net/?view=cards%2Fsearch&card=aether+Vial
# Create your views here.


def home(request):
    context = ' '
    if request.method == 'POST':
        context = request.POST['cards']
    return render(request, 'home.html', {'cards': context})

