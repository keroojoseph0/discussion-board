from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('<slug:slug>/add', views.add_new_topic, name = 'add_new_topic'),
    path('<slug:slug>', views.board_topics, name = 'topics_in_board'),
]
