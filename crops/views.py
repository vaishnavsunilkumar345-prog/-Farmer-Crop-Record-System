from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Crop
from .forms import CropForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages

def home(request):
    return render(request, 'crops/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('crop_list')
        else:
            messages.error(request, 'Signup failed. Please correct the errors.')
    else:
        form = UserCreationForm()
    return render(request, 'crops/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('crop_list')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'crops/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required
def add_crop(request):
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crop_list')
    else:
        form = CropForm()
    return render(request, 'crops/add_crop.html', {'form': form})

@login_required
def crop_list(request):
    crops = Crop.objects.all()
    return render(request, 'crops/crop_list.html', {'crops': crops})

@login_required
def edit_crop(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    if request.method == 'POST':
        form = CropForm(request.POST, instance=crop)
        if form.is_valid():
            form.save()
            return redirect('crop_list')
    else:
        form = CropForm(instance=crop)
    return render(request, 'crops/edit_crop.html', {'form': form, 'crop': crop})

@login_required
def delete_crop(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    crop.delete()
    return redirect('crop_list')
