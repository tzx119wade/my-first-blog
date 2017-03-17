from django.shortcuts import render,get_object_or_404,redirect
from .models import Post
from .forms import PostForm
from django.utils import timezone

# Create your views here.

def post_list(request):
    posts = Post.objects.order_by('created_date')
    return render(request,'blog/post_list.html',{'posts':posts})


def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)

    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form':form})

def post_edit(request,pk):

    # 编辑时要做其它的处理，因为不是在创建新的post，要通过原来的post对象来获取form对象
    post = get_object_or_404(Post,pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',pk = post.pk)
    else:
        # form是通过数据对象映射成一个表单对象，这个表单包含可以显示的字段，也可以往字段里填充内容
        # 我们可以通过原有的对象，把它重新映射成一个表单对象，那这个表单所显示的字段内容就会包含原有的对象内容
        # 方法是：postform(insetance = post)
        form = PostForm(instance=post)

    return render(request,'blog/post_edit.html',{'form':form})

