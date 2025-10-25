from django.test import TestCase
from django.urls import reverse, resolve
from ..views import home
from ..models import Board

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
        board_topics_url = reverse('board_topics:topics_in_board', kwargs={'slug': self.board.slug})
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))