from django.shortcuts import render
from django.http import HttpResponse

from fined.models import Course


menu = ["about", "Log In", "Categories"]

def index(request):
    courses=Course.objects.all()
    context ={
        'courses': courses,
        'menu': menu,
        'title': 'Main Page',
    }
    return render(request, 'main/index.html',context=context)


def categories(request, catid):
    print(request.GET)
    return HttpResponse(f"<h1>Страница по категориям</h1><p>{catid}</p>")

def handler400(request, exception):
    return render(request, "400.html", status=400)
def handler403(request, exception):
    return (render(request, "403.html", status=403))
def handler404(request, exception):
    return (render(request, "404.html", status=404))
def handler500(request):
    return (render(request, "500.html", status=500))
