from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializer import finedSerializer
from .forms import *
from .models import *
from .utils import *

class CourseHome(DataMixin, ListView):
    model = Course
    template_name = 'main/index.html'
    context_object_name = 'courses'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items())+list(c_def.items()))

    def get_queryset(self):
        return Course.objects.filter().select_related('cat')

# class  CourseViewSet(viewset.ModelViewSet):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer

class Courses(DataMixin, ListView):
    model = Course
    template_name = 'main/courses.html'
    context_object_name = 'courses'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Курсы")
        return dict(list(context.items())+list(c_def.items()))

    def get_queryset(self):
        return Course.objects.filter().select_related('cat')

# def index(request):
#     courses=Course.objects.all()
#     context ={
#         'courses': courses,
#         'menu': menu,
#         'title': 'Main Page',
#         'cat_selected' : 0,
#     }
#     return render(request, 'main/index.html', context=context)

class ShowCourse(DataMixin, DetailView):
    model = Course
    template_name = 'main/course.html'
    slug_url_kwarg = 'cour_slug'
    context_object_name = 'course'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['Курс'])
        return dict(list(context.items()) + list(c_def.items()))

# def show_course(request, cour_slug):
#     course = get_object_or_404(Course, slug=cour_slug)
#
#     context = {
#         'course': course,
#         'menu': menu,
#         'title': course.title,
#         'cat_selected': course.cat_id,
#     }
#     return render(request, 'main/course.html', context=context)

class CourseCategory(DataMixin, ListView):
    model = Course
    template_name = 'main/courses.html'
    context_object_name = 'courses'
    allow_empty = False
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория -' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Course.objects.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


# def show_category(request, cat_id):
#     courses = Course.objects.filter(cat_id=cat_id)
#
#     if len(courses) == 0:
#         raise handler404()
#
#     context = {
#         'courses': courses,
#         'menu': menu,
#         'title': 'Отображение по уровням ',
#         'cat_selected': cat_id,
#
#     }
#     return render(request, 'main/index.html', context=context)


def handler400(request, exception):
    return render(request, "400.html", status=400)
def handler403(request, exception):
    return (render(request, "403.html", status=403))
def handler404(request, exception):
    return (render(request, "404.html", status=404))
def handler500(request):
    return (render(request, "500.html", status=500))

def about(request):
    contact_list = Course.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/about.html',{'page_obj': page_obj, 'menu': menu, 'title': 'About'})


class AddCourse(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddCourseForm
    template_name = 'main/addcourse.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление курса")
        return dict(list(context.items())+list(c_def.items()))

# def add_course(request):
#     if request.method == 'POST':
#         form = AddCourseForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddCourseForm()
#     return render(request, 'main/addcourse.html', {'form': form, 'menu': menu, 'title': 'Добавление курса'})

def contact(request):
    return HttpResponse('Обратная связь')

# def login(request):
#     return HttpResponse('Авторизация')

class RegisterUser(DataMixin ,CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'main/login.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))
    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'main/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')




class finedAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 2


class finedAPIList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = finedSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = finedAPIListPagination



class finedAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = finedSerializer
    permission_classes = (IsAuthenticated, )
    # authentication_classes = (TokenAuthentication, )


class finedAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = finedSerializer
    permission_classes = (IsAdminOrReadOnly, )