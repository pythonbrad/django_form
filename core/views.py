from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def forms(request):
    return render(request, 'core/forms.html', {
        'title': 'My forms'
    })
