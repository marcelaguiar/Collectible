from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def home(request):
    return render(request, 'collectionsapp/Home.html')

def collection_types(request):
    return render(request, 'collectionsapp/CollectionTypes.html')


def signup(request):
    return render(request, 'signup.html')