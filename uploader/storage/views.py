from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Document
from .forms import DocumentForm, OTPForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.http import HttpResponseBadRequest, HttpResponseServerError
import os
from uploader import settings




@login_required
def upload(request):
    if request.method == 'POST':
        
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.name = request.FILES['document'].name
            document.uploaded_by = request.user
            document.save()
            document.name = document.document.name[10:]
            document.save()
            doc={
                'filename': document.name,
                'id': document.id,
            }
            print(doc)
            return JsonResponse(doc)

   
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
    email = request.POST.get('email')   
    document = Document.objects.get(id=id)
    if request.method == 'POST':
        try:
            user = User.objects.get(email=email)
            if document.shared_with.filter(pk=user.id).exists():
                print("már hozzá van adva")
                return HttpResponse('This file is already shared with this user.')
            else:
                document.shared_with.add(user)
                document.save()
            return HttpResponse('File shared successfully.')
        except User.DoesNotExist:
            return HttpResponse('User does not exist.')
    return HttpResponse('Nothing changed.')

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


def handler404(request, *args, **kwargs):
    return HttpResponseRedirect('/')

def delete_object(request, id):
    obj = get_object_or_404(Document, id=id)
    filename = obj.name
    obj.delete()
    # Delete the file
    try:
        os.remove(os.path.join(settings.BASE_DIR, 'documents', filename))
    except OSError:
        pass
    # Return a JSON response indicating success
    return JsonResponse({'status': 'success', 'message': 'Object deleted successfully.'})



from django.contrib.auth import authenticate, login
from .models import OTP
from django.core.mail import send_mail


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            OTP.objects.filter(user=user).delete()
            otp = OTP(user=user, code=OTP.generate_otp())
            otp.save()
            send_mail(
                'Your OTP code',
                'Your OTP code is {}'.format(otp.code),
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            return redirect('enter_otp', user_id=user.id)
        else:
            # invalid login
            form = ""
    else:
        form = OTPForm()
    return render(request, 'registration/login.html', {'form': form})


from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from .models import OTP
from django.contrib.auth import logout


def enter_otp_view(request, user_id):
    User = get_user_model()
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['code']
            otp = OTP.objects.filter(user=user).first()
            print(otp_code)
            print(otp.code)
            if str(otp.code).lower() == str(otp_code).lower():
                print("validrfads")
                auth_login(request, user)
                otp.delete()
                return redirect('upload')  # replace with the name of your homepage view
    else:
        form = OTPForm()
    return render(request, 'enter_otp.html', {'form': form, 'user_id': user.id})


from django.core.mail import send_mail

def resend_otp(request, user_id):
    User = get_user_model()
    user = User.objects.get(id=user_id)
    otp = OTP.objects.filter(user=user).last()
    if otp:
        otp.code = OTP.generate_otp()
        otp.save()
        # Send the OTP code via email
        send_mail(
            'OTP Resend',
            f'Your new OTP is: {otp.code}',
            'sender@example.com',
            [user.email],
            fail_silently=False,
        )
        return JsonResponse({'message': 'OTP resent successfully'})
    return JsonResponse({'message': 'OTP not found'})



def logout_view(request):
    logout(request)
    return redirect('login') 