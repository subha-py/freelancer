from django.shortcuts import render,redirect
from django.http import HttpResponse
import os
# Create your views here.
def view_home(request):
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