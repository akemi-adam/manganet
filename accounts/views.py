from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth, logout as leave
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Q
from .forms import LoginForm, RegisterForm

# Aux functions

def guest(user) -> bool:
    return not user.is_authenticated

# Controllers

@user_passes_test(guest, login_url = "/dashboard")
def register(request):

    if request.method == 'POST':

        name = request.POST.get('username')
        mail = request.POST.get('email')

        userAlreadyExists = User.objects.filter(Q(username = name) | Q(email = mail)).values().exists()

        form = RegisterForm(request.POST)

        if userAlreadyExists or not form.is_valid():
            return render(request, 'auth/register.html', { 'form': form })

        user = User.objects.create_user(
            name, mail, request.POST.get('password')
        )

        user.save()

        auth(request, user)

        return redirect('dashboard')

    return render(request, "auth/register.html", { 'form': RegisterForm() })

@user_passes_test(guest, login_url = "/dashboard")
def login(request):

    if request.method == 'POST':

        user = authenticate(username = request.POST.get('username'), password = request.POST.get('password'))

        form = LoginForm(request.POST)

        if user != None and form.is_valid():

            auth(request, user)

            return redirect('dashboard')
        
        return render(request, "auth/login.html", {'form': form})

    return render(request, "auth/login.html", {'form': LoginForm()})

@login_required
def logout(request):

    leave(request)
    
    return redirect('login')

@login_required
def profile(request, id):

    user = User.objects.get(id = id)

    return render(request, 'profile.html', {'user': user})