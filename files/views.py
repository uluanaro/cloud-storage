from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def index_view(request):
    return render(request, 'files/index.html')
