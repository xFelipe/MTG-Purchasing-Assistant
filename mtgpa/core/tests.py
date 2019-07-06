from django.test import TestCase
from mtgpa.core.views import line_interpreter, market_search,  sort_market
from .forms import CardsForm


# Create your tests here.
class TestHome(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_home_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_home_status(self):
        self.assertEqual(200, self.response.status_code)

    def test_input_numbers(self):
        self.assertContains(self.response, '<textarea', 1)
        self.assertContains(self.response, '<input', 3)  # csrf


class TestFunctions(TestCase):
    def test_line_interpreter(self):
        self.assertEqual(line_interpreter('1x Rancor'), {'qnt': 1, 'card_name': 'Rancor'})
        self.assertEqual(line_interpreter('2X Leyline of the Void'), {'qnt': 2, 'card_name': 'Leyline of the Void'})
        self.assertEqual(line_interpreter("5 Hero's Downfall"), {'qnt': 5, 'card_name': "Hero's Downfall"})
        self.assertEqual(line_interpreter('4Rancor'), {'qnt': 4, 'card_name': 'Rancor'})
        self.assertEqual(line_interpreter('Saskia the Unyielding'), {'qnt': 1, 'card_name': 'Saskia the Unyielding'})

    def test_market_search(self):
        self.assertIn('A Loja do Pai', market_search('Llanowar Elves'))
        self.assertIn('Card Castle', market_search('Lightning Bolt'))
        self.assertIn('Cards e Games', market_search('Saskia the Unyielding'))

    def test_sort_market(self):
        d = {'b': [1,2], 'a': [1,2,3], 'c': [1]}
        self.assertEqual(tuple(sort_market(d).items()), (('a', [1,2,3]), ('b', [1,2]), ('c', [1])))


class TestForm(TestCase):
    def test_form_fields(self):
        form = CardsForm({'cards': 'aaa\nbbb', 'precision': 5})
        self.assertEqual(True, form.is_valid())
        self.assertEqual(form.cleaned_data['cards'], 'aaa\nbbb')
        self.assertEqual(form.cleaned_data['precision'], 5)
