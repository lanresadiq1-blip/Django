from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import BlogForm
from .models import Blog
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def homepage(request): # view function
    # retrieve all the blog posts 
    # from the database
    blog_posts = Blog.objects.all()

    return render(
        request,
        "laurenzo/homepage.html",
        context={"blogs": blog_posts}
    )

@login_required
def blog_post(request):
    form = BlogForm()

    # If the user submits a form
    if request.method == "POST":
        # Collect all the data input
        form = BlogForm(request.POST)
        # checks if the input is correct
        if form.is_valid():
            # save the data to the database
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # what next?
            # redirect
            return redirect("home")

    return render(request, "laurenzo/create-blog.html", {"form": form}
                  )

# get the id
# Check the db to see if there's any blog post with that ID exist
# conditionally check if it exists:
    # Render the page with the blog post
# else
    # Redirect the user to /not_found
def article(request, pk):
    # Scan through the blog table
    # and get  blog_posts whose its ID
    # is the same as the pk
    blog_post = Blog.objects.filter(id=pk)

    if blog_post.exists():
        return render(
            request,
            "laurenzo/article.html",
            context={"blog": blog_post.first()},
        )
    else:
        return redirect("/not_found")

def not_found(request):
    return HttpResponse("The page you are looking for does not exist.")

@login_required
def article_delete(request, pk):
    blog_post = Blog.objects.filter(id=pk)
    if request.method == "POST":

     if blog_post.exists():
        post = blog_post.first()
        if post.author != request.user:
                return HttpResponse(
                    "Permission Denied. You're not the owner of the blog post dummy.", status=403
                )
        post.delete()
        return redirect("/")

    return redirect("/not_found")

@login_required
def edit_blog(request, pk):
    # Retrieved all blog posts that shared/have the id
    # filter() Returns QuerySet
    blog_post = Blog.objects.filter(id=pk)

    # Checks if any blog posts were returned
    # If not, redirect the user to not_found
    if not blog_post.exists():
        return redirect("/not_found")

    # Get the first blog post
    post = blog_post.first()

    if post.author != request.user:
        return HttpResponse(
            "Permission Denied. You're not the owner of the blog post dummy.", status=403
        )
    
    # HTTP 1xx --> info
    # 2xx -> Request ok
    # 3x -> Redirection
    # 4xx -> Client/User error
    # 5xx -> Server   

    # Instantiate a form
    form = BlogForm(instance=post)

    # We check if user sumbit a form 
    if request.method == "POST":
        form = BlogForm(request.POST, instance=post)
        # Check if the form is vaild i.e user entered correct data
        if form.is_valid():
            _post = form.save(commit=False)
            _post.author = request.user
            _post.published_at = post.published_at
            _post.save()
            # What next?
            # We redirect!
            return redirect("read-blog", pk=post.pk)
        
    # Display a template to the end-user
    return render(request, 'laurenzo/edit_blog.html', {'blog_post': post})


def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    return render(request, "registration/register.html", {"form": form})

@login_required
def profile(request):
    user = request.user
    # use the reverse accessor to obtain all the posts that belong to the user
    # and assign it to a variable called 'user_posts'
    user_posts = user.blog_set.all()
    return render(request, "registration/profile.html", context={'blogs': user_posts})