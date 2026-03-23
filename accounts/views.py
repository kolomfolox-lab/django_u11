from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegisterForm, LoginForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            from django.contrib.auth.models import Group
            user_group, created = Group.objects.get_or_create(name='User')
            user.groups.add(user_group)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            return redirect('book_list')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

from django.utils import timezone
from .models import VerificationCode
from .utils import send_email_thread

def forgot_password_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            from django.contrib.auth.models import User
            user = User.objects.get(username=username)
            code_obj = VerificationCode.objects.create(user=user)
            send_email_thread('Parolni tiklash', f'Code: {code_obj.code}', [user.email])
            return redirect('restore_password')
        except User.DoesNotExist:
            pass
    return render(request, 'accounts/forgot_password.html')

def restore_password_view(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password == confirm_password:
            try:
                code_obj = VerificationCode.objects.get(code=code)
                if code_obj.expired_date > timezone.now():
                    user = code_obj.user
                    user.set_password(new_password)
                    user.save()
                    code_obj.delete()
                    return redirect('login')
            except VerificationCode.DoesNotExist:
                pass
    return render(request, 'accounts/restore_password.html')
