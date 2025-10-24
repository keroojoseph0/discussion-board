from django.shortcuts import render
from .models import Board
from django.shortcuts import get_object_or_404

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