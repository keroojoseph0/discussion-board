from django.shortcuts import render
from .models import Board
from django.shortcuts import get_object_or_404
from .forms import TopicForm
from django.shortcuts import redirect

# Create your views here.

def home(request):
    boards = Board.objects.all()
    
    context = {'boards': boards}
    return render(request, 'home.html', context)

def board_topics(request, slug):
    board = get_object_or_404(Board, slug = slug)
    topics = board.topics.all()
        
    context = {'topics': topics, 'board': board}
    return render(request, 'boards.html', context)

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
    return render(request, 'add_new_topic.html', context)