from django.shortcuts import render, redirect
from .models import Project, Material
from .forms import QuoteRequestForm
from django.http import JsonResponse
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from .forms import SignUpForm
from .models import QuoteRequest
from django.contrib import messages

def home(request):
    context = {}
    if request.user.is_authenticated:
        # Add user-specific data to the context if needed
        context['user_id'] = request.user.id
    else:
        # Handle the case for anonymous users
        context['user_id'] = None

    # Add any other context data you need

    return render(request, 'home.html', context)
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Authenticate the user
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            # Log the user in
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def request_quote(request):
    if request.method == 'POST':
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            quote_request = form.save(commit=False)
            quote_request.user = request.user
            quote_request.save()
            messages.success(request, 'Your quote request has been submitted successfully!')
            return redirect('quote_list')  # or wherever you want to redirect after submission
    else:
        form = QuoteRequestForm()

    return render(request, 'request_quotes.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a success page
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def admin_dashboard(request):
    # Fetch all projects
    projects = Project.objects.all()
    return render(request, 'admin_dashboard.html', {'projects': projects})


def update_project_status(request, project_id):
    if request.method == 'POST':
        project = Project.objects.get(id=project_id)
        new_status = request.POST.get('status')
        project.status = new_status
        project.save()
        return JsonResponse({'status': 'success', 'new_status': new_status})
    return JsonResponse({'status': 'error'}, status=400)

def project_details(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'project_details.html', {'project': project})


def create_material(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        Material.objects.create(name=name, description=description)
        return redirect('materials_list')
    return render(request, 'create_material.html')


def update_material(request, material_id):
    material = Material.objects.get(id=material_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        material.name = name
        material.description = description
        material.save()
        return redirect('materials_list')
    return render(request, 'update_material.html', {'material': material})


def delete_material(request, material_id):
    material = Material.objects.get(id=material_id)
    material.delete()
    return redirect('materials_list')


def materials_list(request):
    materials = Material.objects.all()
    return render(request, 'materials_list.html', {'materials': materials})