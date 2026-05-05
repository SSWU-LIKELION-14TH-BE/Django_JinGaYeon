from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django. contrib.auth import login
from django. contrib. auth. decorators import login_required
from .forms import SignUpForm
from post.models import Post
from .forms import UserUpdateForm
from .models import CustomUser

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
        else:
             print(form.errors)
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

@login_required
def home_view(request):
    return redirect('post_list')

def find_password_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')

        try:
            user = CustomUser. objects.get(username=username, phone_number=phone_number)
            request.session['reset_password_id'] = user.id
            return redirect('reset_password')
        
        except CustomUser.DoesNotExist:
          return render(request, 'find_pw.html', {
            'error': '아이디 혹은 전화번호가 일치하지 않습니다.'
          })
        
    return render(request, 'find_pw.html')
        

def reset_password_view(request):
    user_id = request.session.get('reset_password_id')

    if not user_id:
        return redirect('find_password')
    
    user = CustomUser.objects.get(id=user_id)

    if request. method == 'POST':
       new_password = request.POST.get('password')

       user.set_password(new_password)
       user.save()

       del request. session['reset_password_id']
       return redirect ('login')
    
    return render(request, 'reset_pw.html')

@login_required
def mypage_view(request):
    user = request.user

    my_posts = Post. objects.filter(author=user).order_by('-created_at')

    return render(request, 'mypage.html', {
        'user': user,
        'my_posts': my_posts,
    })

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('mypage')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})


    