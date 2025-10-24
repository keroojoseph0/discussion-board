from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, board_topics, add_new_topic
from .models import Board, Post, Topic
from django.contrib.auth.models import User
from .forms import TopicForm

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
        board_topics_url = reverse('board_topics:topics_in_board', kwargs={'slug': self.board.slug})
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))
        
class BoardTopicsTest(TestCase):
    def setUp(self):
        Board.objects.create(name = 'web test', description = 'description test')
        
    def test_board_topics_view_status_code(self):
        url = reverse('board_topics:topics_in_board', kwargs={'slug': 'web-test'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics:topics_in_board', kwargs={'slug': 'Test'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_board_topics_url_resolve_board_topics_view(self):
        view = resolve('/boards/Web-programming')
        self.assertEqual(view.func, board_topics)
        
    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse('board_topics:topics_in_board', kwargs={'slug': 'web-test'})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        
    
        
class AddNewTopicTest(TestCase):
    def setUp(self):
        Board.objects.create(name = 'django test', description = 'description test')
        User.objects.create_user(username='john', email='john@doe.com', password='123')  
        
    def test_csrf(self):
        url = reverse('board_topics:add_new_topic', kwargs={'slug': 'django-test'})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')
        
    def test_new_topic_valid_post_data(self):
        pass
    
    def test_new_topic_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('board_topics:add_new_topic', kwargs={'slug': 'web-test'})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())
        
    def test_new_topic_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('board_topics:add_new_topic', kwargs={'slug': 'web-test'})
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 404)
        
    def test_add_new_topic_view_status_code(self):
        url = reverse('board_topics:add_new_topic', kwargs={'slug': 'django-test'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_add_new_topic_view_not_found_status_code(self):
        url = reverse('board_topics:add_new_topic', kwargs={'slug': 'django'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
        
    def test_add_new_topic_url_resolve_add_new_view(self):
        view = resolve('/boards/django-test/add')
        self.assertEqual(view.func, add_new_topic)
        
    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('board_topics:add_new_topic', kwargs={'slug': 'django-test'})
        board_topics_url = reverse('board_topics:topics_in_board', kwargs={'slug': 'django-test'})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))
        
    def test_contains_form(self):  # <- new test
        url = reverse('board_topics:add_new_topic', kwargs={'slug': 'django-test'})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, TopicForm)

    def test_new_topic_invalid_post_data(self):  # <- updated this one
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('board_topics:add_new_topic', kwargs={'slug': 'django-test'})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)