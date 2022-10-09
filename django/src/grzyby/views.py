from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Grzyby
from .forms import GrzybyForm

# Create your views here.

@login_required(login_url='/login/')
def index(request):
    grzyby = Grzyby.objects.order_by('-create_time')
    context = {'grzyby': grzyby}
    return render(request, 'grzyby/index.html', context=context)

@login_required(login_url='/login/')
def add(request):
    if request.method == 'GET':
        grzyby = GrzybyForm()
        context = {'form': grzyby}
        return render(request, 'grzyby/add.html', context)
    if request.method == 'POST':
        grzyby = GrzybyForm(request.POST)
        if grzyby.is_valid():
            grzyby = grzyby.save(commit=False)
            grzyby.create_time = timezone.now()
            grzyby.save()
            return redirect('grzyby_index')

@login_required(login_url='/login/')
def update(request, id):
    grzybyData = Grzyby.objects.get(id=id)
    if request.method == 'GET':
        form = GrzybyForm(instance=grzybyData)
        context = {'form': form}
        return render(request, 'news/update.html', context)
    
    if request.method == 'POST':
        updateForm = GrzybyForm(request.POST, instance=grzybyData)
        if updateForm.is_valid():
            updateForm = updateForm.save(commit=False)
            updateForm.last_edit_time = timezone.now()
            updateForm.save()
        return redirect('grzyby_index')

@login_required(login_url='/login/')
@require_http_methods(["GET"])
def delete(request, id):
    grzybyData = get_object_or_404(Grzyby,id=id)
    grzybyData.delete()
    return redirect('grzyby_index')


