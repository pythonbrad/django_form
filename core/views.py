from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import Form, EntryForm, RecordForm
from .models import Form as MForm, Entry


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('forms')
    else:
        return render(request, 'core/index.html', {
            'title': 'Home'
        })


@login_required
def forms(request):
    return render(request, 'core/forms.html', {
        'title': 'MyForms',
        'forms': request.user.forms.filter()
    })


@login_required
def new_form(request):
    if request.POST:
        form = Form(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            messages.success(request, 'Form created')
            return redirect('forms')
        else:
            pass
    else:
        form = Form()
    return render(request, 'core/new_object.html', {
        'title': 'New Form',
        'form': form,
        'object_name': 'Form',
        'back_url': redirect('forms').url
    })


@login_required
def edit_form(request, pk):
    mform = get_object_or_404(MForm, pk=pk, author=request.user)
    if request.POST:
        form = Form(request.POST, request.FILES, instance=mform)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form updated')
            return redirect('forms')
        else:
            pass
    else:
        form = Form(instance=mform)
    return render(request, 'core/new_object.html', {
        'title': 'Edit Form',
        'form': form,
        'object_name': 'Form',
        'edit': True,
        'back_url': redirect('forms').url
    })


@login_required
def delete_form(request, pk):
    mform = get_object_or_404(MForm, pk=pk, author=request.user)
    if request.POST.get('delete', None):
        mform.delete()
        messages.success(request, 'Form deleted')
        return redirect('forms')
    else:
        pass
    return render(request, 'core/delete_object.html', {
        'title': 'Delete Form',
        'object': mform,
        'back_url': redirect('forms').url
    })


@login_required
def entries(request, pk):
    mform = get_object_or_404(MForm, pk=pk, author=request.user)
    entries = mform.entries.filter()
    return render(request, 'core/data.html', {
        'title': "Form's Entries",
        'entries': entries,
        'form': mform,
        'raw': False
    })


@login_required
def new_entry(request, pk):
    mform = get_object_or_404(MForm, pk=pk, author=request.user)
    if request.POST:
        form = EntryForm(request.POST)
        if form.is_valid():
            form.instance.form = mform
            form.save()
            messages.success(request, 'Entry added')
            return redirect('entries', pk)
        else:
            pass
    else:
        form = EntryForm()
    return render(request, 'core/new_object.html', {
        'title': 'New Entry',
        'form': form,
        'object_name': 'Entry',
        'back_url': redirect('entries', pk).url
    })


@login_required
def edit_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk, form__author=request.user)
    if request.POST:
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entry updated')
            return redirect('entries', entry.form.pk)
        else:
            pass
    else:
        form = EntryForm(instance=entry)
    return render(request, 'core/new_object.html', {
        'title': 'Edit Entry',
        'form': form,
        'object_name': 'Entry',
        'edit': True,
        'back_url': redirect('entries', entry.form.pk).url
    })


@login_required
def delete_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk, form__author=request.user)
    if request.POST.get('delete', None):
        entry.delete()
        messages.success(request, 'Entry deleted')
        return redirect('entries', entry.form.pk)
    else:
        pass
    return render(request, 'core/delete_object.html', {
        'title': 'Delete Form',
        'object': entry,
        'back_url': redirect('entries', entry.form.pk).url
    })


@login_required
def records(request, pk):
    mform = get_object_or_404(MForm, pk=pk, author=request.user)
    entries = mform.entries.filter()
    return render(request, 'core/data.html', {
        'title': "Form's Entries",
        'entries': entries,
        'form': mform,
        'raw': True
    })


def new_record(request, code):
    mform = get_object_or_404(MForm, code=code)
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    if request.POST:
        forms = [
            RecordForm(entry, request.POST)
            for entry in mform.entries.filter()
        ]
        if any([
            form.is_valid()
            for form in forms
        ]):
            for form in forms:
                form.instance.author = user
                form.save()
            return render(request, 'core/success_record.html', {
                'title': mform.name,
                'form': mform,
            })
        else:
            pass
    else:
        forms = [
            RecordForm(entry)
            for entry in mform.entries.filter()
        ]
    return render(request, 'core/new_record.html', {
        'title': mform.name,
        'mform': mform,
        'forms': forms
    })
