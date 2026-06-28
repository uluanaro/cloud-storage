from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import services


@login_required
def index_view(request):
    path = request.GET.get('path', "")
    user_id = request.user.id
    folders, files = services.list_files(user_id, path)
    return render(request, 'files/index.html', {
        'folders': folders,
        'files': files,
        'current_path': path
    })

@login_required
def upload_view(request):
    path = request.POST.get('path', "")
    user_id = request.user.id
    file = request.FILES.get('file')
    if not file:
        return redirect(f"/?path={path}")
    services.upload_file(user_id, path, file)
    return redirect(f"/?path={path}")

@login_required
def create_folder_view(request):
    path = request.POST.get('path', "")
    user_id = request.user.id
    folder_name = request.POST.get('folder_name', "")
    if not folder_name:
        return redirect(f"/?path={path}")
    services.create_folder(user_id, path, folder_name)
    return redirect(f"/?path={path}")


@login_required
def delete_view(request):
    path = request.POST.get('path', "")
    user_id = request.user.id
    key = request.POST.get('key', "")
    if not key:
        return redirect(f"/?path={path}")
    services.delete_file(user_id, key)
    return redirect(f"/?path={path}")
