from django.shortcuts import render
from .models import Board, Topic, Post
from django.shortcuts import get_object_or_404
from .forms import TopicForm, PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
    queryset = board.topics.order_by('-updated_at').annotate(replies=Count('posts') - 1)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 12)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        topics = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        topics = paginator.page(paginator.num_pages)
    
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

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Board, Topic, Post

def topic_posts(request, slug, topic_slug):
    board = get_object_or_404(Board, slug=slug)
    topic = get_object_or_404(Topic, board=board, topic_slug=topic_slug)

    # Queryset for all replies (ordered)
    posts_qs = Post.objects.filter(topic=topic).order_by('created_at')

    # Increment view count (keep as you had it)
    topic.views += 1
    topic.save()

    # Pagination config - change 5 to whatever number of replies per page you want
    paginator = Paginator(posts_qs, 3)
    page_number = request.GET.get('page', 0)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'board': board,
        'topic': topic,
        # keep the name `posts` (this is a Page object)
        'posts': posts,
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

class PostUpdateView(LoginRequiredMixin ,UpdateView):
    model = Post
    fields = ['message']
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('board_topics:topic_posts')
    template_name = 'board/edit_post.html'
    context_object_name = 'post'
    
    def get_object(self, queryset=None):
        # make sure we fetch the post that belongs to the right topic + board
        return get_object_or_404(
            Post,
            pk=self.kwargs.get('pk'),
            topic__topic_slug=self.kwargs.get('topic_slug'),
            topic__board__slug=self.kwargs.get('slug')
        )
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.created_by = self.request.user
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('board_topics:topic_posts', slug=post.topic.board.slug, topic_slug=post.topic.topic_slug)

class TopicUpdateView(LoginRequiredMixin, UpdateView):
    model = Topic
    fields = ['subject', 'message']
    template_name = 'board/edit_topic.html'
    context_object_name = 'topic'

    def get_object(self, queryset=None):
        # ✅ use topic_slug instead of slug
        return get_object_or_404(
            Topic,
            topic_slug=self.kwargs.get('topic_slug'),
            board__slug=self.kwargs.get('slug')
        )

    def form_valid(self, form):
        topic = form.save(commit=False)
        topic.updated_at = timezone.now()
        topic.save()
        return redirect(
            'board_topics:topic_posts',
            slug=topic.board.slug,
            topic_slug=topic.topic_slug
        )