from django.shortcuts import render,redirect
from content_app.models import Blog
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required



# Create your views here.

def home(request):
    # post_count = Blog.objects.count()
    # context = {
    #     'post_count': post_count
    # }
    if request.user.is_authenticated:
        if request.user.is_superuser:
            blogs=Blog.objects.all
        else:
            blogs = Blog.objects.filter(auther = request.user)
    else:
        blogs=Blog.objects.all()
    count = blogs.count()
    context = {
        'count' : count,
        'blogs' : blogs
    }
    # blogs= get_object_or_404(Blog, pk=id)
    # if blogs.author != request.user:
    #     return render(request,  {'message': 'You are not authorized to view this blog.'})
    # else:
    #
      
    return render(request , 'app/home.html', context)

@login_required(login_url="login")   
def add(request):
    if request.method=='GET':
        return render(request,'app/add.html')
    else:
        title=request.POST['title']
        content=request.POST['content']
        Blog.objects.create(title=title,content=content,auther_id=request.user.id)
        return redirect('home')
    
@login_required(login_url="login") 
def delete(request ,id):
    Blog.objects.get(id=id).delete()
    return redirect('home')
    # return render(request,'app/delete.html')
    
@login_required(login_url="login") 
def edit(request,id):
    if request.method=='GET':
        blog=Blog.objects.get(id=id)
        return render(request,'app/edit.html',{'blog':blog})
    elif request.method=='POST':
        blog=Blog.objects.get(id=id)
        title=request.POST['title']
        content=request.POST['content']
        Blog.objects.update_or_create(id = id, defaults={
            'title' : title,
            'content' : content
        })
        return redirect('home')
    
@login_required(login_url="login") 
def delete_all(request):
    if Blog>1:
        Blog.objects.all().delete()
    
    return redirect('home')
    # return render(request,'app/delete_app.html')
    
def register(request):
    if request.method=="GET":
        return render(request ,'app/register.html')
    else:
        fn=request.POST['firstname']
        ln=request.POST['lastname']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        
        user = User(first_name=fn,last_name=ln,email=email,username=username,password=password)
        user.save()
        login(request, user)
        
        return redirect('home')
    
def signin(request):
    if request.method=="GET":
        return render(request ,"app/login.html")
    else:
        uname=request.POST['username']
        password=request.POST['password']
        
        user=authenticate(username=uname,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return redirect("login")
        
def signout(request):
    logout(request)
    return redirect('login')