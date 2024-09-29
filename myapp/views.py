import csv
import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from catalyst_count.tasks import load_my_file, test_task
from myapp.models import CatalystCount
from myapp.ws_client import send_message_view
from .forms import QueryBuilderForm, UploadFileForm, UserForm
from django.db import connection
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.response import Response
import uuid
from django.contrib.auth.decorators import login_required

@login_required
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


@login_required
def delete_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('user_list')


@login_required
def upload_data(request):
    client_id = uuid.uuid4()
    client_id = str(client_id)
    if request.method == 'POST' :  # and 'csvfile' in request.FILES
        new_catalyst = request.FILES['file']
        client_id = request.POST.get("client_id")
        if not new_catalyst.name.endswith('.csv') or not new_catalyst:
            messages.info(request, 'Please upload a CSV file.')
            return render(request, 'upload_data.html', {'form': form})
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            print("before hit redis")
            load_my_file.delay(uploaded_file.id, client_id)

            messages.success(request, 'File uploaded and processed successfully.')
            return render(request, 'upload_data.html',{'client_id':client_id })
    else:
        form = UploadFileForm()

    return render(request, 'upload_data.html', {'form': form, 'client_id':client_id })


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('/accounts/login')

@login_required
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


@login_required
def query_builder(request):
    return render(request, 'query_builder.html')


def test(request):
    id  = request.GET.get("id")
    send_message_view(id,"this is msg")
    return HttpResponse("Hello, world. You're at the polls index.")