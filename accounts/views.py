from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect

from django.db.models import Q

from django.shortcuts import redirect, render

from django.contrib.auth import authenticate, login as auth, logout as leave
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User

from .forms import LoginForm, RegisterForm

# Aux functions

def guest(user: User) -> bool:
    return not user.is_authenticated

# Controllers

@user_passes_test(guest, login_url = "/dashboard")
def register(request: HttpRequest) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:

    if request.method == 'POST':

        name: str = request.POST.get('username')
        mail: str = request.POST.get('email')

        userAlreadyExists: bool = User.objects.filter(Q(username = name) | Q(email = mail)).values().exists()

        form: RegisterForm = RegisterForm(request.POST)

        if userAlreadyExists or not form.is_valid():
            return render(request, 'auth/register.html', { 'form': form })

        user: User = User.objects.create_user(
            name, mail, request.POST.get('password')
        )

        user.save()

        auth(request, user)

        return redirect('dashboard')

    return render(request, "auth/register.html", { 'form': RegisterForm() })

@user_passes_test(guest, login_url = "/dashboard")
def login(request: HttpRequest):

    if request.method == 'POST':

        user = authenticate(username = request.POST.get('username'), password = request.POST.get('password'))

        form: LoginForm = LoginForm(request.POST)

        if user != None and form.is_valid():

            auth(request, user)

            return redirect('dashboard')
        
        return render(request, "auth/login.html", {'form': form})

    return render(request, "auth/login.html", {'form': LoginForm()})

@login_required
def logout(request: HttpRequest) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    leave(request)
    return redirect('login')

@login_required
def profile(request: HttpRequest, id: int) -> HttpResponse:

    user: User = User.objects.get(id = id)

    evaluations = user.evaluation_set.all()

    return render(request, 'profile.html', {'user': user, 'evaluations': evaluations})