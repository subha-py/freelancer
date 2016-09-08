from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.mail import send_mail
import os
# Create your views here.
def view_home(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        message=request.POST.get('message')
        subject='New contact from name : {name}   phone : {phone}'.format(name=name,phone=phone)
        send_mail(subject,message,email,['subha.py@gmail.com'],)
    return render(request,'base.html')

def download_pdf(request,filename):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path=(BASE_DIR+ '/page/static/pdf/')
    fileList=os.listdir(path)
    for afile in fileList:
        if filename in afile:
            with open('{path}/{file}'.format(path=path,file=afile),'r') as pdf:
                response = HttpResponse(pdf.read(),content_type='application/pdf')
                response['Content-Disposition'] = 'inline;filename=some_file.pdf'
                return response
    else:
        return HttpResponse('No file found!')