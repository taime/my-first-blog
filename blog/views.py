from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from .models import Post
from django.shortcuts import redirect
from urllib.request import urlopen



def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                # post.published_date = timezone.now()
                post.save()
                return redirect('blog.views.post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})
        
def post_edit(request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('blog.views.post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})

def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog.views.post_detail', pk=pk)    







def instagram (request):
    # url = 'http://rownarts.com'
    access_token = '26184090.1247a07.09c9456df4db48fd9d477c99e0d57733'

    # url = 'https://api.instagram.com/v1/users/self/?access_token=26184090.1247a07.09c9456df4db48fd9d477c99e0d57733'
    # my user id is 26184090
    url = 'https://api.instagram.com/v1/users/26184090/media/recent/?COUNT=100&MIN_ID=1279340983&MAX_ID=1279340983&access_token='+access_token
    # url = 'http://s.rwns.ru/insta-answer.html'
    response = urlopen(url)
    html = response.read()

    import json
    json_string = html
    parsed_string = json.loads(json_string.decode())
    html = parsed_string['data']
    test = 'Hello!'

    # test = sorted(html, key=len(created_time)
    html = sorted(html, reverse=True, key=lambda student: student['likes']['count'])

    # import operator
    # x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
    # sorted_x = sorted(html.comments.count.items(), key=operator.itemgetter(0))

    # html = {'name': 'ivan', 'age':12, 'city':'Moscow', 'data':'some data will be here'}
    # test = html['data']
    return render(request, 'blog/instagram.html', {'html': html,'test':test})


def bestfit (request):
    url='http://bestfit.su/page/4/timetable.html'
    response = urlopen(url)
    html = response.read()
    
    return render(request, 'blog/bestfit.html', {'html': html})



def parser (request):
    from grab import Grab
    import mymodule
    # url = 'http://moscross.ru/catalog/converse'
    url = 'http://moscross.ru/catalog/kedy-vans'

    # html = mymodule.getProductsText(url)
    # html = mymodule.getProductsImages(url)
    # html = mymodule.getLinks(url)
    # html = mymodule.getProductInfoFromcatalog()
    # html = mymodule.parseCatalogLinks('http://moscross.ru/catalog/Adidas-Equipment')
    # html = mymodule.parseAllCatalogs()
    # html = mymodule.getProduct('http://s.rwns.ru/some-test.html')
    # html = mymodule.getProduct('http://moscross.ru/item/885-nike-air-max-2014-belyjj-zelenyjj-rozovyjj-art040')



    # product_links = mymodule.giveAllProductsLinks()
    # html = mymodule.getProducts(product_links)  




    # html = mymodule.parseCollections(mymodule.newbalance_collections)
    html = mymodule.getProducts(mymodule.newbalance_links) 

    return render(request, 'blog/parser.html', {'html': html})











