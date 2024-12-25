from django.shortcuts import render,redirect # type: ignore
from .models import Post
from django.core.files.storage import default_storage
from django.db.models import Q

# Create your views here.
def get_images(request):
    posts = Post.objects.all().filter(is_private = False)
    
    if request.method == 'POST':
        query = request.POST.get('search_post')
        posts = Post.objects.filter(
            Q(title__icontains=query),
            Q(description__icontains=query),
            Q(is_private = False)
        )

    return render(request, './main/home.html', {'posts': posts})

def create_post(request): 
    
    if request.method == 'POST':
        data = request.POST
        title = data.get('title')
        description = data.get('description')
        image = request.FILES.get('image')
        is_private = data.get('is_private') == 'on'
        
        if image:
            image_path = default_storage.save(f'posts/{image.name}',image)
            
            Post.objects.create(
                title=title,
                description=description,
                image=image_path,
                is_private=is_private,
                user = request.user
            )
            return redirect('home')
        else:
            redirect('create_post')
    
    return render(request, './main/create-post.html')
