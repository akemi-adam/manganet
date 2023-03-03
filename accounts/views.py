from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect

from django.shortcuts import redirect, render

from django.db.models import Q

from .forms import LoginForm, RegisterForm

from django.contrib.auth import authenticate, login as auth, logout as leave
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User

# Aux functions

def guest(user: User) -> bool:
    """ Checks that the visitor is not logged in """

    return not user.is_authenticated

# Controllers

@user_passes_test(guest, login_url = "/dashboard")
def register(request: HttpRequest) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
    """
    Enters a new user. If the method is POST, it checks if a user with the passed credentials already exists and validates the form; if all is correct, it creates, authenticates and redirects the user to the dashboard.

    If the method is GET, it renders the registration page
    """

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
def login(request: HttpRequest) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
    """
    Checks that the request method is POST. If it is, try to log the user in and validate the form to send them to the dashboard page.

    If it fails or the request is GET, it renders the login page
    """

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
    """ Logs the user out and redirects them to the login page """

    leave(request)
    return redirect('login')

@login_required
def profile(request: HttpRequest, id: int) -> HttpResponse:
    """ Retrieves the user and his ratings and renders his profile """

    user: User = User.objects.get(id = id)

    evaluations = user.evaluation_set.all()

    return render(request, 'profile.html', {'user': user, 'evaluations': evaluations})