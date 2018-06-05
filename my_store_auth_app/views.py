from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse, HttpResponse

from my_store_auth_app.forms import RegistrationForm

# Create your views here.


@ensure_csrf_cookie
@require_POST
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'authorized'})
    else:
        return JsonResponse({'message': 'invalid login'})


def logout_view(request):
    logout(request)
    return HttpResponse(status=200)


@require_http_methods(['GET', 'POST'])
def signup_view(request):
    # Проверка на уже авторизованного пользователя
    if request.user.is_authenticated:
        return HttpResponse(status=404)

    if request.method == 'GET':
        registration_form = RegistrationForm()
        context = {'form': registration_form}

        return render(request, 'my_store_auth_app/signup.html', context)
