from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

#Importaciones para loginin y loginout
from django.contrib.auth import authenticate, login, logout
from django .http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in!")

#Login_required es un decorador (función django) que permite que el usuario solo pueda
#hacer logout cuando se realize login en cualquier view
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        #Se compara si son validos ambos formularios
        if user_form.is_valid() and profile_form.is_valid():
            #Almacena la información del formulario user
            user = user_form.save()
            #Hashing the password
            user.set_password(user.password)
            user.save()

            #Almacena la información del formulario profile
            #Commit=False evita que se produzca colisión, evita que se guarde la información y que se
            #produzca una sobreescritura
            profile = profile_form.save(commit=False)
            profile.user = user

            #Si se carga una foto,
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()

            #Confirmamos el registro
            registered = True

        #En caso de que no sean válidos los formularios...
        else:
            print(user_form.errors,profile_form.errors)

    #En caso de que no se produzca un POST
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Valida que el usuario y contraseña sean correctos
        user = authenticate(username=username, password=password)

        if user:
            #Si la cuenta usuario esta activada
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Your account is not active)")

        else:
            print("Someone tried to login and fail")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("Invalid login details")
    else:
        return render(request, 'basic_app/login.html', {})