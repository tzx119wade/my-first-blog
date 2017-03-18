from django.shortcuts import render,get_object_or_404,redirect
from .models import Post
from .forms import PostForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

def post_home(request):
    return redirect('post_list')

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('created_date')
    return render(request,'blog/post_list.html',{'posts':posts})


def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required()
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)

    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form':form})

@login_required()
def post_edit(request,pk):

    # 编辑时要做其它的处理，因为不是在创建新的post，要通过原来的post对象来获取form对象
    post = get_object_or_404(Post,pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',pk = post.pk)
    else:
        # form是通过数据对象映射成一个表单对象，这个表单包含可以显示的字段，也可以往字段里填充内容
        # 我们可以通过原有的对象，把它重新映射成一个表单对象，那这个表单所显示的字段内容就会包含原有的对象内容
        # 方法是：postform(insetance = post)
        form = PostForm(instance=post)

    return render(request,'blog/post_edit.html',{'form':form})


# 处理草稿箱
@login_required()
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts':posts})


# 处理详情页的发布
@login_required()
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()

    return redirect('post_detail',pk=post.pk)


# 删除文章
@login_required()
def post_remove(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.delete()

    return redirect('post_list')