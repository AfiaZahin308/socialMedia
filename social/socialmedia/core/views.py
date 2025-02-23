from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, PostForm
from .models import Post
from django.db.models import Q
from django.core.paginator import Paginator

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'core/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'core/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

# @login_required
# def home(request):
#     posts = Post.objects.all().order_by('-created_at')
#     return render(request, 'core/home.html', {'posts': posts})



@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')

    
    date_filter = request.GET.get('date_filter')
    if date_filter == 'oldest':
        posts = posts.order_by('created_at')

    
    media_filter = request.GET.get('media_filter')
    if media_filter == 'text':
        posts = posts.filter(image__isnull=True)
    elif media_filter == 'images':
        posts = posts.filter(image__isnull=False)

    
    user_filter = request.GET.get('user_filter')
    if user_filter:
        posts = posts.filter(user__username=user_filter)

    
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(Q(content__icontains=search_query))


    paginator = Paginator(posts, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/home.html', {'page_obj': page_obj})

@login_required
def profile(request):
    posts = Post.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/profile.html', {'posts': posts})
   


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'core/create_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    messages.success(request, 'Post deleted successfully!')
    return redirect('profile')