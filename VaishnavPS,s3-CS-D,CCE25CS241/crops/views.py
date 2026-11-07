from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from django.db.models import Count, Q
from django.views.decorators.http import require_POST
from .models import Crop
from .forms import CropForm

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'crops/home.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Signup failed. Please correct the errors.')
    else:
        form = UserCreationForm()
    return render(request, 'crops/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'crops/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    if request.user.is_staff:
        crops = Crop.objects.all()
        context = {
            'total_crops': crops.count(),
            'total_farmers': crops.values('farmer_name').distinct().count(),
            'total_users': User.objects.filter(is_staff=False).count(),
            'unassigned': crops.filter(owner__isnull=True).count(),
            'seasons': crops.values('season').annotate(total=Count('id')).order_by('-total')[:5],
            'recent': crops.select_related('owner').order_by('-id')[:6],
        }
        return render(request, 'crops/admin_dashboard.html', context)
    crops = Crop.objects.filter(owner=request.user)
    context = {
        'total_crops': crops.count(),
        'total_seasons': crops.values('season').distinct().count(),
        'recent': crops.order_by('-id')[:5],
    }
    return render(request, 'crops/user_dashboard.html', context)

@login_required
def add_crop(request):
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            crop = form.save(commit=False)
            crop.owner = request.user
            crop.save()
            messages.success(request, 'Crop record added.')
            return redirect('crop_list')
    else:
        form = CropForm()
    return render(request, 'crops/add_crop.html', {'form': form})

@login_required
def crop_list(request):
    if request.user.is_staff:
        crops = Crop.objects.select_related('owner').order_by('-id')
    else:
        crops = Crop.objects.filter(owner=request.user).order_by('-id')
    query = request.GET.get('q', '').strip()
    if query:
        crops = crops.filter(Q(crop_name__icontains=query) | Q(farmer_name__icontains=query) | Q(season__icontains=query))
    return render(request, 'crops/crop_list.html', {'crops': crops, 'query': query})

@login_required
def edit_crop(request, pk):
    if request.user.is_staff:
        crop = get_object_or_404(Crop, pk=pk)
    else:
        crop = get_object_or_404(Crop, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = CropForm(request.POST, instance=crop)
        if form.is_valid():
            form.save()
            messages.success(request, 'Crop record updated.')
            return redirect('crop_list')
    else:
        form = CropForm(instance=crop)
    return render(request, 'crops/edit_crop.html', {'form': form, 'crop': crop})

@login_required
@require_POST
def delete_crop(request, pk):
    if request.user.is_staff:
        crop = get_object_or_404(Crop, pk=pk)
    else:
        crop = get_object_or_404(Crop, pk=pk, owner=request.user)
    crop.delete()
    messages.success(request, 'Crop record deleted.')
    return redirect('crop_list')
