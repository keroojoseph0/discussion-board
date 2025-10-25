from django.shortcuts import render
from .models import Board, Topic, Post
from django.shortcuts import get_object_or_404
from .forms import TopicForm, PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count


# Create your views here.

def home(request):
    boards = Board.objects.all()
    topic = Topic.objects.all()
    
    for board in boards:
        board.post_count = Post.objects.filter(topic__board=board).count()
    
    context = {'boards': boards, 'topic': topic}
    return render(request, 'board/home.html', context)

def board_topics(request, slug):
    board = get_object_or_404(Board, slug=slug)
    topics = board.topics.annotate(replies_count=Count('posts') - 1)

    context = {'board': board, 'topics': topics}
    return render(request, 'board/boards.html', context)

@login_required
def add_new_topic(request, slug):
    board = get_object_or_404(Board, slug = slug)
    
    if request.method == 'POST':
        form = TopicForm(request.POST)
        print('test valid')
        if form.is_valid():
            print('Valid')
            myform = form.save(commit=False)
            myform.created_by = request.user
            myform.board = board
            myform.save()
            return redirect('home')
    else:
        form = TopicForm()
    
    context = {'form': form, 'board': board}
    return render(request, 'board/add_new_topic.html', context)

def topic_posts(request, slug, topic_slug):
    board = get_object_or_404(Board, slug=slug)
    topic = get_object_or_404(Topic, board=board, topic_slug=topic_slug)

    # increment view count
    topic.views += 1
    topic.save()

    # count replies (excluding the first post)
    

    context = {
        'board': board,
        'topic': topic,
    }
    return render(request, 'board/topic_posts.html', context)

@login_required
def reply_topic(request, slug, topic_slug):
    topic = get_object_or_404(Topic, board__slug = slug, topic_slug = topic_slug)
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        
        if form.is_valid():
            myform = form.save(commit=False)
            myform.topic = topic
            myform.created_by = request.user
            myform.updated_by = request.user
            myform.save()
            return redirect('board_topics:topic_posts', slug = slug, topic_slug = topic_slug)
    
    else:
        form = PostForm()
        
    context = {'form': form, 'topic': topic}
    return render(request, 'board/reply_topic.html', context)
