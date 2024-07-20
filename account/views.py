from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from django.db import connection
from .forms import QueryForm

from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from chunked_upload.models import ChunkedUpload

def users(request):
    user_list = User.objects.all()
    return render(request, 'account/users.html', {'users': user_list})


class MyChunkedUploadView(ChunkedUploadView):
    model = ChunkedUpload
    field_name = 'file'

class MyChunkedUploadCompleteView(ChunkedUploadCompleteView):
    model = ChunkedUpload

    def on_completion(self, uploaded_file, request):
        # Do something with the uploaded file.
        pass

    def get_response_data(self, chunked_upload, request):
        return {'message': 'You did it!'}

def upload_data(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            # return redirect('success')
    else:
        form = UploadFileForm()
    return render(request, 'upload_data.html', {'form': form})

def handle_uploaded_file(f):
    with open('uploaded_file.csv', 'wb+') as destination:
        i = 0
        for chunk in f.chunks():
            i+=1
            destination.write(chunk)
            print("\n chunk", i, chunk)


def query_builder(request):
    results = None
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['keyword']
            print("query----", query)
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
    else:
        form = QueryForm()
    return render(request, 'query_builder.html', {'form': form, 'results': results})
