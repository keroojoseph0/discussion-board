from django.test import TestCase
from django.urls import reverse, resolve
from .views import home

# Create your tests here.

class HomeTest(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        respone = self.client.get(url)
        self.assertEqual(respone.status_code, 200)
        
    def test_home_url_resolve_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func, home)
        
