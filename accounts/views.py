from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from app.models import Post

# Create your views here.
def create_user(request):
    
    if request.method == 'POST':
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        
        new_user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email = email,
            username=username
        )
        
        new_user.set_password(password)
        new_user.save()
        return redirect('login_user')
    
    return render(request, 'register.html')

def login_user(request):
    
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user=user)
            return redirect('home')
        
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login_user')

@login_required(login_url='/accounts/login')
def profile(request):
    posts = Post.objects.filter(user = request.user)
    
    if request.method == 'POST':
        if request.POST.get('delete_post'):
            post = Post.objects.get(id = request.POST.get('delete_post'))
            post.delete()
            
            return redirect('profile_user')
        
        elif request.POST.get('toggle_privacy'):
            post = Post.objects.get(id = request.POST.get('toggle_privacy'))
            post.is_private = not post.is_private
            post.save()
            
            return redirect('profile_user')
    
    return render(request, 'profile.html', {'posts': posts})

@login_required(login_url='/accounts/login')
def edit_profile(request):

    if request.method == 'POST':
        user = request.user
        data = request.POST
        new_first_name = data.get('first_name',user.first_name)
        new_last_name = data.get('last_name',user.last_name)
        new_email = data.get('email',user.email)
        new_username = data.get('username',user.username)
        new_password = data.get('password')
        
        existing_user = User.objects.get(username=user.username)

        existing_user.username = new_username
        existing_user.email = new_email
        existing_user.first_name = new_first_name
        existing_user.last_name = new_last_name
        
        if new_password:
            existing_user.set_password(new_password)

        existing_user.save()

        if new_password:
            login(request, existing_user)
        
        return redirect('profile_user')
    
    return render(request, 'edit-profile.html')