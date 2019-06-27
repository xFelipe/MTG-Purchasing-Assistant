from django.test import TestCase


# Create your tests here.
class TestHome(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def testHomeTemplate(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def testHomeStatus(self):
        self.assertEqual(200, self.response.status_code)

    def testInputNumbers(self):
        self.assertContains(self.response, '<textarea', 1)
        self.assertContains(self.response, '<input', 1)