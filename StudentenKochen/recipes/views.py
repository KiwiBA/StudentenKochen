from django.http import HttpResponse

def myFirstView(request):
    return HttpResponse("Hello world!")
