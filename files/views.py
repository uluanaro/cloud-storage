from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import services


@login_required
def index_view(request):
    path = request.GET.get('path', "")
    user_id = request.user.id
    folders, files = services.list_files(user_id, path)

    parts = path.split("/")
    current = ""
    breadcrumbs = [("Главная", "")]
    for part in parts:
        if part:
            current += part + "/"
            breadcrumbs.append((part, current))

    return render(request, 'files/index.html', {
        'folders': folders,
        'files': files,
        'current_path': path,
        'breadcrumbs': breadcrumbs
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

@login_required
def download_view(request):
    key = request.GET.get('key', "")
    if not key:
        return redirect("/")
    url = services.get_download_url(key, expires=3600)
    return redirect(url)

@login_required
def search_view(request):
    query = request.GET.get('query', "")
    if not query:
        return redirect("/")
    user_id = request.user.id
    results = services.search_files(user_id, query)
    return render(request, 'files/search.html', {
        'results': results,
        'query': query
    })