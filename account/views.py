import csv
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from account.models import CatalystCount
from .forms import QueryBuilderForm, UploadFileForm, UserForm
from django.db import connection
from .resources import CatalystCountResources
from tablib import Dataset
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from rest_framework.views import APIView
from rest_framework.response import Response


def user_list(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'New user added successfully.')
            return redirect('user_list')
    else:
        form = UserForm()
    
    users = User.objects.all()
    return render(request, 'account/users.html', {'users': users, 'form': form})


def delete_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('user_list')


def users(request):
    user_list = User.objects.all()
    return render(request, 'account/users.html', {'users': user_list})

def deleteUser(request, user_id):
    print(user_id, "id")
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return JsonResponse({'success': True})

def upload_data(request):
    if request.method == 'POST':
        new_catalyst = request.FILES['file']
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if not new_catalyst.name.endswith('.csv'):
                messages.info(request, 'Please upload a CSV file.')
                return render(request, 'upload_data.html', {'form': form})

            # Process the uploaded file
            dataset = new_catalyst.read().decode('utf-8').splitlines()
            reader = csv.DictReader(dataset)
            i = 0
            for data in reader:
                print(i)
                CatalystCount.objects.update_or_create(
                    name=data['name'],
                    domain=data['domain'],
                    year_founded = data['year founded'],
                    industry = data['industry'],
                    locality = data['locality'],
                    country = data['country'],
                    linkedin_url = data['linkedin url'],
                    employees_from = data['current employee estimate'],
                    employees_to = data['total employee estimate'],
                )
                if i > 1000:
                    break
                i += 1
            print("out of loop")
            messages.success(request, 'File uploaded and processed successfully.')
            return render(request, 'upload_data.html')
    else:
        form = UploadFileForm()
    return render(request, 'upload_data.html', {'form': form})


class QueryBuilderAPIView(APIView):
    def get(self, request):
        form = QueryBuilderForm(request.GET)
        if form.is_valid():
            queryset = CatalystCount.objects.all()
            if form.cleaned_data['keyword']:
                queryset = queryset.filter(name__icontains=form.cleaned_data['keyword'])
            if form.cleaned_data['industry']:
                queryset = queryset.filter(industry__icontains=form.cleaned_data['industry'])
            if form.cleaned_data['year_founded']:
                queryset = queryset.filter(year_founded=form.cleaned_data['year_founded'])
            if form.cleaned_data['city']:
                queryset = queryset.filter(locality__icontains=form.cleaned_data['city'])
            if form.cleaned_data['state']:
                queryset = queryset.filter(locality__icontains=form.cleaned_data['state'])
            if form.cleaned_data['country']:
                queryset = queryset.filter(country__icontains=form.cleaned_data['country'])
            if form.cleaned_data['employees_from']:
                queryset = queryset.filter(employees_from__gte=form.cleaned_data['employees_from'])
            if form.cleaned_data['employees_to']:
                queryset = queryset.filter(employees_to__lte=form.cleaned_data['employees_to'])
            
            count = queryset.count()
            return Response({'count': count})
        return Response({'error': 'Invalid query'}, status=400)


def query_builder(request):
    return render(request, 'query_builder.html')
