from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, board_topics
from .models import Board, Topic

# Create your tests here.

class HomeTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name = 'web home test', description = 'description home test')
        
        
    def test_home_view_status_code(self):
        url = reverse('home')
        respone = self.client.get(url)
        self.assertEqual(respone.status_code, 200)
        
    def test_home_url_resolve_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func, home)
        
    def test_home_view_contains_link_to_topics_page(self):
        response = self.client.get(reverse('home'))
        board_topics_url = reverse('board_topics', kwargs={'slug': self.board.slug})
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))
        
class BoardTopicsTest(TestCase):
    def setUp(self):
        Board.objects.create(name = 'web test', description = 'description test')
        
    def test_board_topics_view_status_code(self):
        url = reverse('board_topics', kwargs={'slug': 'web-test'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'slug': 'Test'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_board_topics_url_resolve_board_topics_view(self):
        view = resolve('/boards/Web-programming')
        self.assertEqual(view.func, board_topics)
        
    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse('board_topics', kwargs={'slug': 'web-test'})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))