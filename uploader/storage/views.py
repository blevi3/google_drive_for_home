from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Document
from .forms import DocumentForm
from django.http import HttpResponse
from django.contrib.auth.models import User


@login_required
def upload(request):
    if request.method == 'POST':
        
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.name = request.FILES['document'].name
            document.uploaded_by = request.user
            document.save()
            print(document.document)
            document.name = document.document.name[10:]
            document.save()
            print(document.name)
            doc={
                document.name,
            }
            return HttpResponse(doc)
   
    else:
        form = DocumentForm()
    documents = Document.objects.filter(uploaded_by=request.user)
    return render(request, 'upload.html', {'documents': documents, 'form': form})

@login_required
def download(request, id):
    document = Document.objects.get(id=id)
    if request.user == document.uploaded_by or request.user in document.shared_with.all():
        response = HttpResponse(document.document, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{document.name}"'
        return response
    else:
        return HttpResponse('You do not have permission to download this file.')

@login_required
def share(request, id):
    print("share")
    email = request.POST.get('email')   
    document = Document.objects.get(id=id)
    print(id)
    if request.method == 'POST':
        
        print(email)
        try:
            user = User.objects.get(email=email)
            new_document = Document.objects.create(
                name=document.name,
                document=document.document,
                uploaded_by=document.uploaded_by,
                )
            new_document.shared_with.add(user)
            new_document.save()
            return HttpResponse('File shared successfully.')
        except User.DoesNotExist:
            return HttpResponse('User does not exist.')
    return render(request, 'upload.html', {'document': document})


def shared_with_you(request):
    shared_documents = Document.objects.filter(shared_with=request.user)
    return render(request, 'shared_with_you.html', {'shared_documents': shared_documents})



from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import os
def upload_chunk(request):
    # Get the chunk data from the request
    file = request.FILES['document']
    chunk_name = request.POST['document'].split('_')[-1]
    file_id = request.POST['file_id']

    # Define the storage directory for this file
    storage_dir = os.path.join('media', 'chunks', file_id)

    # Create the storage directory if it doesn't exist
    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir)

    # Save the chunk to disk
    fs = FileSystemStorage(location=storage_dir)
    fs.save(chunk_name, file)

    # Return a JSON response indicating success
    return JsonResponse({'status': 'success'})
