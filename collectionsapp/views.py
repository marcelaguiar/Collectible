from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse


# Create your views here.
def home(request):
    return render(request, 'collectionsapp/Home.html')

def collection_types(request):
    return render(request, 'collectionsapp/CollectionTypes.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/signup.html', context)


def logout_view(request):
    logout(request)
    return redirect(reverse(home))