from django.shortcuts import render

# Create your views here
from django. contrib. auth. decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from . forms import PostForm, CommentForm
from django.db.models import Count

def post_list(request):
    query = request.GET.get('q', '')   
    sort = request.GET.get('sort', 'latest')

    posts = Post.objects.all().order_by('-created_at')  

    #검색
    if query:
        posts = posts.filter(title__icontains=query)  

    #정렬
    if sort == 'popular':
        posts = posts.annotate(like_count=Count('likes')).order_by('-like_count')   
    else:
        posts = posts.order_by('-created_at')
    
    return render(request, 'postlist.html', {
        'posts' : posts,
        'query': query,
        'sort' : sort,
        })

#게시물작성
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) 
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form':form}) 

#댓글작성
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()
    comments = post.comments.all()   # parent 안 쓰는 상태면 이걸로
    return render(request, 'post_detail.html', {
        'post': post,
        'comment_form': comment_form,
        'comments': comments,
    })

def comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(post=post, parent__isnull=True).order_by('-created_at')
    form = CommentForm()

    post.views += 1
    post.save()

    return render(request, 'post_comment.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })

 #게시물수정   
@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        return redirect('post_list')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'post_form.html', {'form': form})

#게시물 삭제
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
        
    if request.user != post.author:
        return redirect('post_list')
    
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    
    return render(request, 'post_delete.html', {'post': post})

#게시물 좋아요
@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)  
    else:
        post.likes.add(request.user)     
    return redirect('post_list')

#댓글 작성
@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment =form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment. save()
            return redirect('comment', pk=pk)
            
    return redirect('comment', pk=pk)


#댓글 삭제
@login_required
def comment_delete(request, pk, comment_pk):
    post = get_object_or_404(Post, pk=pk)
    comment = get_object_or_404(Comment, pk=comment_pk,post=post)

    if request.method == 'POST':
        comment.delete()
        return redirect('comment', pk=pk)
       
    return render (request, 'post_delete.html', {
        'comment': comment,
        'post': post,
    }) 
 

#답글 작성
def comment_reply(request, pk, comment_pk):
    post = get_object_or_404(Post, pk=pk)
    parent_comment = get_object_or_404(Comment, pk=comment_pk, post=post)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = post
            reply.author = request.user
            reply.parent = parent_comment
            reply.save()
            return redirect('comment', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'comment_reply.html', {
        'post': post,
        'parent_comment': parent_comment,
        'form': form,
    })
 

#댓글 좋아요
@login_required
def comment_like(request, pk , comment_pk):
    post = get_object_or_404(Post, pk=pk)
    comment = get_object_or_404(Comment, pk=comment_pk,post=post)

    if request.user in comment.likes.all():
        comment.likes.remove(request.user)  
    else:
        comment.likes.add(request.user)     
    return redirect('comment', pk=pk)


   

