from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('<slug:slug>/add', views.add_new_topic, name = 'add_new_topic'),
    path('<slug:slug>/<slug:topic_slug>', views.topic_posts, name = 'topic_posts'),
    path('<slug:slug>/<slug:topic_slug>/<int:pk>/edit', views.PostUpdateView.as_view(), name = 'edit_post'),
    path('<slug:slug>/<slug:topic_slug>/edit/topic', views.TopicUpdateView.as_view(), name = 'edit_topic'),
    path('<slug:slug>/<slug:topic_slug>/reply', views.reply_topic, name = 'reply_topic'),
    path('<slug:slug>', views.board_topics, name = 'topics_in_board'),
]
